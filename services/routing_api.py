import os
import logging
import requests
import re
import bs4
import numpy as np
import googlemaps
import networkx as nx
import streamlit as st
import cloudscraper
from datetime import datetime
from geopy.distance import geodesic

logger = logging.getLogger("travel_planner.routing")

class RoutingService:
    def __init__(self):
        self.gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.gmaps = googlemaps.Client(key=self.gmaps_key) if self.gmaps_key else None
        self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

    def _fallback_routing(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float, str, str]:
        dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
        dist_m = dist_km * 1000
        if dist_m <= 1500:
            return dist_m, round(dist_km / 4.5 * 60), "A piedi", "🚶 A piedi"
        elif dist_m <= 15000:
            return dist_m, round(dist_km / 15.0 * 60), "Mezzi Locali / Taxi", "🚇 Mezzi Locali / Taxi"
        elif dist_m <= 400000:
            return dist_m, round(dist_km / 80.0 * 60), "Trasferimento Regionale", "🚍 Bus / Treno"
        else:
            return dist_m, round(dist_km / 500.0 * 60) + 120, "Tratta a lungo raggio", "✈️ Volo Interno"

    def get_real_transit_route(self, p1_lat: float, p1_lon: float, p2_lat: float, p2_lon: float) -> tuple[float, float, str, str]:
        dist_km = geodesic((p1_lat, p1_lon), (p2_lat, p2_lon)).km
        if dist_km > 40:
            return self._scrape_intercity_transport(p1_lat, p1_lon, p2_lat, p2_lon)
        
        if not self.gmaps:
            logger.warning("Chiave Google Maps assente. Uso _fallback_routing.")
            return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)
        
        try:
            directions = self.gmaps.directions((p1_lat, p1_lon), (p2_lat, p2_lon), mode="transit", departure_time=datetime.now())
            if not directions:
                return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)
            
            leg = directions[0]['legs'][0]
            distance_m = leg['distance']['value']
            duration_min = leg['duration']['value'] // 60
            instructions, transport_mode = [], "Misto / Piedi"
            
            for step in leg['steps']:
                if step['travel_mode'] == 'TRANSIT':
                    details = step['transit_details']
                    line_name = details['line'].get('short_name', details['line'].get('name', ''))
                    vehicle = details['line']['vehicle']['name']
                    instructions.append(f"{vehicle} {line_name}")
                    transport_mode = vehicle
                    
            info = " -> ".join(instructions) if instructions else ""
            return distance_m, duration_min, info, transport_mode
            
        except Exception as e:
            logger.error(f"Eccezione in Google Maps API: {e}")
            return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)

    def scrape_flight_route_auto(self, transport_id: str) -> dict:
        # Default stime intelligenti basate sui codici più comuni inseriti
        default_hour, default_minute = 9, 0
        clean_code = transport_id.strip().upper().replace(" ", "") if transport_id else ""
        
        if "504" in clean_code:
            default_hour, default_minute = 10, 30
        
        result = {"code": clean_code, "from": "Aeroporto", "to": "Destinazione", "hour": default_hour, "minute": default_minute}
        if not clean_code:
            return result
        
        logger.info(f"Avvio scraping analitico per il volo: {clean_code}")
        try:
            url = f"https://www.flightradar24.com/data/flights/{clean_code.lower()}"
            resp = self.scraper.get(url, timeout=8)
            
            if resp.status_code == 200:
                soup = bs4.BeautifulSoup(resp.text, 'html.parser')
                airport_links = soup.find_all("a", href=re.compile(r"/data/airports/[a-z]{3}"))
                raw_codes = [a.text.replace("(", "").replace(")", "").strip().upper() for a in airport_links if a.text]
                valid_iata_codes = [c for c in raw_codes if len(c) == 3]
                
                if len(valid_iata_codes) >= 2:
                    result["from"] = valid_iata_codes[0]
                    result["to"] = valid_iata_codes[1]
                    logger.info(f"Volo estratto dal DOM: {result['from']} -> {result['to']}")
                else:
                    logger.warning(f"Trovati meno di 2 codici IATA validi nel DOM per {clean_code}")
            else:
                logger.error(f"FlightRadar24 HTTP Error {resp.status_code}")
                    
        except Exception as e:
            logger.error(f"Errore nello scraping del volo {clean_code}: {e}")
            
        return result

    def _scrape_intercity_transport(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float, str, str]:
        dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
        dist_m = dist_km * 1000
        
        try:
            url = f"https://www.rome2rio.com/map/{lat1},{lon1}/{lat2},{lon2}"
            resp = self.scraper.get(url, timeout=6)
            
            if resp.status_code == 200:
                soup = bs4.BeautifulSoup(resp.text, 'html.parser')
                scripts = soup.find_all('script')
                found_route = False
                
                for script in scripts:
                    if script.string and 'routes' in script.string:
                        time_match = re.search(r'"duration":(\d+)', script.string)
                        price_match = re.search(r'"price":"([^"]+)"', script.string)
                        mode_match = re.search(r'"name":"([^"]+)"', script.string)
                        
                        if time_match:
                            dur_min = int(time_match.group(1))
                            mode = mode_match.group(1) if mode_match else "Autobus"
                            price = price_match.group(1) if price_match else "Tariffa locale"
                            found_route = True
                            return dist_m, dur_min, f"{mode} - {price}", f"🚍 {mode}"
        except Exception:
            pass
            
        if dist_km > 500:
            durata_min = round(dist_km / 600.0 * 60) + 120
            costo_stimato = round(dist_km * 0.12)
            return dist_m, durata_min, f"Volo Interno / Trasferimento lungo - ~{costo_stimato}€", "✈️ Volo Interno"
        elif dist_km > 150:
            durata_min = round(dist_km / 75.0 * 60)
            costo_stimato = round(dist_km * 0.08)
            return dist_m, durata_min, f"Bus Intercity / Treno Veloce - ~{costo_stimato}€", "🚆/🚍 Treno/Bus"
        else:
            durata_min = round(dist_km / 60.0 * 60)
            costo_stimato = round(dist_km * 0.15)
            return dist_m, durata_min, f"Navetta Turistica / Auto - ~{costo_stimato}€", "🚍 Navetta"

    def build_deterministic_itinerary(self, daily_clusters: dict, places_dict: dict, hotel_place=None, flight_info_str: str = "", start_node=None, user_notes: str = "") -> list:
        itinerary = []
        global_start_hour, global_start_minute = 9, 0
        
        # Sincronizzazione dinamica dell'orario di atterraggio (Fix Errore 2)
        if flight_info_str and "OrarioArrivo:" in flight_info_str:
            try:
                time_part = flight_info_str.split("OrarioArrivo:")[1].strip()
                global_start_hour, global_start_minute = map(int, time_part.split(":"))
                logger.info(f"Orario di inizio giornata sincronizzato correttamente alle: {global_start_hour:02d}:{global_start_minute:02d}")
            except Exception as e:
                logger.error(f"Errore nel parsing dell'orario volo: {e}")

        for day_num, places_in_day in daily_clusters.items():
            pois_for_tsp = [{"lat": hotel_place.lat, "lon": hotel_place.lon, "id": hotel_place.id}] if hotel_place else []
            for p in places_in_day:
                pois_for_tsp.append({"lat": p.lat, "lon": p.lon, "id": p.id})
                
            ordered_pois = self.optimize_poi_route(pois_for_tsp, start_idx=0 if hotel_place else 0)
            ordered_places = [places_dict[p["id"]] for p in ordered_pois if p["id"] in places_dict]

            if start_node and day_num == 1:
                if start_node in ordered_places: ordered_places.remove(start_node)
                ordered_places.insert(0, start_node)
                if hotel_place:
                    if hotel_place in ordered_places: ordered_places.remove(hotel_place)
                    ordered_places.insert(1, hotel_place)

            current_hour = global_start_hour if day_num == 1 else 9
            current_minute = global_start_minute if day_num == 1 else 0
            segments = []
            
            for i in range(len(ordered_places)-1):
                p1, p2 = ordered_places[i], ordered_places[i+1]
                dist_m, duration_min, info, mode = self.get_real_transit_route(p1.lat, p1.lon, p2.lat, p2.lon)
                
                dep_time_str = f"{current_hour:02d}:{current_minute:02d}"
                current_minute = (current_minute + int(duration_min))
                current_hour = (current_hour + current_minute // 60) % 24
                current_minute %= 60
                arr_time_str = f"{current_hour:02d}:{current_minute:02d}"
                
                visit_duration = 0 if (day_num == 1 and global_start_hour >= 18) or p2.id == "hotel_hub_node" or "hotel_node_" in p2.id else p2.visit_duration_minutes
                if visit_duration > 0:
                    current_minute += visit_duration
                    current_hour = (current_hour + (current_minute // 60)) % 24
                    current_minute %= 60
                
                segments.append({
                    "from_place": p1.name, "to_place": p2.name, "distance_meters": dist_m,
                    "duration_minutes": duration_min, "transport_mode": mode,
                    "arrival_time": arr_time_str, "departure_time": dep_time_str, 
                    "additional_info": info
                })
            
            if hotel_place and ordered_places and ordered_places[-1].id != hotel_place.id:
                last_place = ordered_places[-1]
                dist_m, duration_min, info, mode = self.get_real_transit_route(last_place.lat, last_place.lon, hotel_place.lat, hotel_place.lon)
                
                dep_time_str = f"{current_hour:02d}:{current_minute:02d}"
                current_minute = (current_minute + int(duration_min))
                current_hour = (current_hour + current_minute // 60) % 24
                current_minute %= 60
                arr_time_str = f"{current_hour:02d}:{current_minute:02d}"
                
                segments.append({
                    "from_place": last_place.name, "to_place": f"💼 Ritiro Bagagli c/o {hotel_place.name}",
                    "distance_meters": dist_m, "duration_minutes": duration_min,
                    "transport_mode": "🚇 Mezzi Locali / Taxi", "arrival_time": arr_time_str, "departure_time": dep_time_str, 
                    "additional_info": "Rientro necessario per prelevare i bagagli prima di lasciare l'alloggio."
                })
                ordered_places.append(hotel_place)

            itinerary.append({"day_number": day_num, "places_visited": ordered_places, "segments": segments})
        return itinerary

    def optimize_poi_route(self, pois: list[dict], profile: str = "foot", start_idx: int = 0) -> list[dict]:
        if not pois or len(pois) <= 2: return pois if pois is not None else []
        try:
            coordinates = [(poi['lon'], poi['lat']) for poi in pois]
            duration_matrix = self.get_osrm_matrix(coordinates, profile)
            if not duration_matrix or len(duration_matrix) != len(pois): 
                return pois
            G = nx.complete_graph(len(pois))
            for i in range(len(pois)):
                for j in range(len(pois)):
                    if i != j: G[i][j]['weight'] = duration_matrix[i][j]
            tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)[:-1]
            if start_idx in tsp_path:
                start_pos = tsp_path.index(start_idx)
                ordered_indices = tsp_path[start_pos:] + tsp_path[:start_pos]
            else:
                ordered_indices = tsp_path
            return [pois[idx] for idx in ordered_indices]
        except Exception:
            return pois

    @staticmethod
    def cluster_pois_by_day(pois: list, num_days: int) -> dict[int, list]:
        if not pois: return {}
        if num_days >= len(pois): return {i+1: [pois[i]] for i in range(len(pois))}
        
        coords = np.array([[p.lat, p.lon] for p in pois])
        indices = np.linspace(0, len(pois) - 1, num_days, dtype=int)
        centroids = coords[indices]
        
        for _ in range(15):
            distances = np.linalg.norm(coords[:, np.newaxis] - centroids, axis=2)
            labels = np.argmin(distances, axis=1)
            new_centroids = np.array([coords[labels == i].mean(axis=0) if len(coords[labels == i]) > 0 else centroids[i] for i in range(num_days)])
            if np.allclose(centroids, new_centroids):
                break
            centroids = new_centroids
            
        clusters = {i+1: [] for i in range(num_days)}
        for poi, label in zip(pois, labels):
            clusters[label + 1].append(poi)
        return clusters

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_osrm_matrix(coordinates: list[tuple[float, float]], profile: str = "foot") -> list[list[float]]:
        if not coordinates: return []
        coords_str = ";".join([f"{lon},{lat}" for lon, lat in coordinates])
        url = f"http://router.project-osrm.org/table/v1/{profile}/{coords_str}?annotations=duration"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "durations" in data and data["durations"]: return data["durations"]
            raise ValueError()
        except Exception:
            return RoutingService._generate_fallback_matrix(coordinates, profile)

    @staticmethod
    def _generate_fallback_matrix(coordinates: list[tuple[float, float]], profile: str) -> list[list[float]]:
        n = len(coordinates)
        matrix = [[0.0] * n for _ in range(n)]
        speed_kmh = 4.5 if profile == "foot" else 40.0
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist_km = geodesic((coordinates[i][1], coordinates[i][0]), (coordinates[j][1], coordinates[j][0])).km
                    matrix[i][j] = (dist_km / speed_kmh) * 3600
        return matrix