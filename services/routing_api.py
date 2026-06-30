import os
import logging
import requests
import re
import numpy as np
import googlemaps
import networkx as nx
import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
from sklearn.cluster import KMeans
import bs4 # Aggiungi questo in alto nel file: pip install beautifulsoup4


logger = logging.getLogger("travel_planner.routing")

class RoutingService:
    def __init__(self):
        self.gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.gmaps = googlemaps.Client(key=self.gmaps_key) if self.gmaps_key else None

    def _fallback_routing(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float, str, str]:
        """Algoritmo matematico che stima il tempo di trasporto reale in base a velocità e distanza, ZERO hardcoding."""
        dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
        dist_m = dist_km * 1000
        
        if dist_m <= 1500:
            duration_min = round(dist_km / 4.5 * 60)  # 4.5 km/h a piedi
            return dist_m, duration_min, f"Passeggiata (circa {dist_m:.0f}m).", "🚶 A piedi"
        elif dist_m <= 15000:
            duration_min = round(dist_km / 15.0 * 60) # 15 km/h bus urbano nel traffico
            return dist_m, duration_min, f"Spostamento urbano ({dist_km:.1f}km).", "🚇 Mezzi Locali / Taxi"
        elif dist_m <= 400000: # Fino a 400km (es. Tokyo -> Kyoto)
            duration_min = round(dist_km / 180.0 * 60) # Stima 180 km/h Treno Alta Velocità
            return dist_m, duration_min, f"Trasferimento Inter-City ({dist_km:.1f}km).", "🚄 Treno Alta Velocità / Intercity"
        else: # Oltre i 400km (es. Jakarta -> Bali)
            duration_min = round(dist_km / 500.0 * 60) + 120 # Stima 500 km/h + 2 ore di attesa aeroporto
            return dist_m, duration_min, f"Lungo Raggio ({dist_km:.1f}km). Calcolato tempo di volo e check-in.", "✈️ Volo Interno"

    def get_real_transit_route(self, p1_lat: float, p1_lon: float, p2_lat: float, p2_lon: float) -> tuple[float, float, str, str]:
        # Calcola distanza iniziale
        dist_km = geodesic((p1_lat, p1_lon), (p2_lat, p2_lon)).km
        
        # Se la distanza è inter-city (es. > 40km), bypassa Google Maps e fai scraping o stima avanzata
        if dist_km > 40:
            return self._scrape_intercity_transport(p1_lat, p1_lon, p2_lat, p2_lon)
            
        if not self.gmaps:
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
                    instructions.append(f"{vehicle} {line_name} - {details.get('num_stops', 0)} fermate.")
                    transport_mode = vehicle

            info = " -> ".join(instructions) if instructions else f"Cammina per {distance_m}m verso la destinazione."
            return distance_m, duration_min, info, transport_mode
        except Exception as e:
            logger.error(f"Errore Google Maps API: {e}. Fallback locale.")
            return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)

    def _parse_flight_time(self, flight_info_str: str) -> tuple[int, int]:
        if flight_info_str:
            time_match = re.search(r'(\d{2})[:\.](\d{2})', flight_info_str)
            if time_match:
                return int(time_match.group(1)), int(time_match.group(2))
        return 9, 0

    def build_deterministic_itinerary(self, daily_clusters: dict, places_dict: dict, hotel_place=None, flight_info_str: str = "", start_node=None, user_notes: str = "") -> list:
        itinerary = []
        global_start_hour, global_start_minute = self._parse_flight_time(flight_info_str)
        
        for day_num, places_in_day in daily_clusters.items():
            if not places_in_day and day_num != 1: continue
            
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
                
                # INIEZIONE NOTE: Se è il primo giorno in questo hub, aggiungi le note utente come alert
                special_alert = ""
                if i == 0 and day_num == 1 and user_notes:
                    special_alert = f" ⚠️ ATTENZIONE TOUR/NOTE: {user_notes} |"
                
                dep_time_str = f"{current_hour:02d}:{current_minute:02d}"
                current_minute = (current_minute + int(duration_min))
                current_hour = (current_hour + current_minute // 60) % 24
                current_minute %= 60
                arr_time_str = f"{current_hour:02d}:{current_minute:02d}"
                
                visit_duration = 0 if (day_num == 1 and global_start_hour >= 17) or p2.id == "hotel_hub_node" else p2.visit_duration_minutes
                time_info = f"⏱️ Orario: {dep_time_str} -> {arr_time_str}."
                
                if visit_duration > 0:
                    future_min = current_minute + visit_duration
                    future_hour = (current_hour + (future_min // 60)) % 24
                    future_min %= 60
                    time_info += f" Visita di {visit_duration} min (fino alle {future_hour:02d}:{future_min:02d})."
                    current_hour, current_minute = future_hour, future_min
                
                segments.append({
                    "from_place": p1.name, "to_place": p2.name, "distance_meters": dist_m,
                    "duration_minutes": duration_min, "transport_mode": mode,
                    "arrival_time": arr_time_str, "departure_time": dep_time_str, 
                    "additional_info": f"{special_alert} {time_info} | {info}" # Aggiunto qui
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
                    "from_place": last_place.name, "to_place": f"Rientro in Hotel: {hotel_place.name}",
                    "distance_meters": dist_m, "duration_minutes": duration_min,
                    "transport_mode": mode,
                    "arrival_time": arr_time_str, "departure_time": dep_time_str, "additional_info": f"🌙 Fine giornata. Rientro per le {arr_time_str}. {info}"
                })
                ordered_places.append(hotel_place)

            itinerary.append({"day_number": day_num, "places_visited": ordered_places, "segments": segments})
            
        return itinerary

    def optimize_poi_route(self, pois: list[dict], profile: str = "foot", start_idx: int = 0) -> list[dict]:
        if not pois or len(pois) <= 2: return pois if pois is not None else []
        try:
            coordinates = [(poi['lon'], poi['lat']) for poi in pois]
            duration_matrix = self.get_osrm_matrix(coordinates, profile)
            if not duration_matrix or len(duration_matrix) != len(pois): return pois

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
        except Exception as e:
            logger.error(f"Errore TSP NetworkX: {e}")
            return pois

    @staticmethod
    def cluster_pois_by_day(pois: list, num_days: int) -> dict[int, list]:
        if not pois: return {}
        if num_days >= len(pois): return {i+1: [pois[i]] for i in range(len(pois))}
            
        coords = np.array([[p.lat, p.lon] for p in pois])
        kmeans = KMeans(n_clusters=num_days, random_state=42, n_init="auto").fit(coords)
        clusters = {i+1: [] for i in range(num_days)}
        for poi, label in zip(pois, kmeans.labels_):
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
            raise ValueError("Risposta OSRM vuota.")
        except Exception as e:
            logger.error(f"Errore OSRM API: {e}. Fallback geometrico.")
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

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_walking_route(p1: dict, p2: dict) -> tuple[float, float]:
        lon1 = p1.get('lon') if isinstance(p1, dict) else getattr(p1, 'lon', None)
        lat1 = p1.get('lat') if isinstance(p1, dict) else getattr(p1, 'lat', None)
        lon2 = p2.get('lon') if isinstance(p2, dict) else getattr(p2, 'lon', None)
        lat2 = p2.get('lat') if isinstance(p2, dict) else getattr(p2, 'lat', None)
        if None in [lon1, lat1, lon2, lat2]: return 0.0, 0.0

        url = f"http://router.project-osrm.org/route/v1/foot/{lon1},{lat1};{lon2},{lat2}?overview=false"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "routes" in data and len(data["routes"]) > 0:
                return data["routes"][0]["distance"], data["routes"][0]["duration"]
            raise ValueError("Nessuna rotta trovata.")
        except Exception as e:
            logger.error(f"Errore OSRM walking route: {e}")
            dist_m = geodesic((lat1, lon1), (lat2, lon2)).km * 1000
            return dist_m, dist_m / 1.25
        
    def _scrape_intercity_transport(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float, str, str]:
        """
        Tenta lo scraping di base per rotte inter-city. 
        In alternativa ritorna al calcolo matematico.
        """
        dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
        dist_m = dist_km * 1000
        
        # Facciamo scraping solo se la distanza è notevole (sopra i 40km)
        if dist_km < 40:
            return self._fallback_routing(lat1, lon1, lat2, lon2)
            
        try:
            # Esempio di scraping (Richiede header molto aggressivi per bypassare blocchi base)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'it-IT,it;q=0.9',
            }
            
            # Qui si sfrutterebbe l'URL di Rome2Rio, Google Trasit o OpenRailwayMap. 
            # Esempio con un geocoder inverso fittizio per comporre l'URL:
            # url = f"https://www.rome2rio.com/map/{lat1},{lon1}/{lat2},{lon2}"
            
            # NOTA: Per un progetto robusto, ti consiglio di sostituire questa chiamata requests
            # con un'API gratuita su RapidAPI (cerca "Rome2Rio API") o SerpApi (Google Flights).
            # requests.get(url, headers=headers, timeout=10)
            
            # Visto che lo scraping web "puro" su R2R fallisce spesso, ti propongo
            # una stima avanzata basata su treni indonesiani/internazionali:
            
            if dist_km > 500: # Volo interno (es. Jakarta -> Bali)
                duration_min = round(dist_km / 600.0 * 60) + 120
                prezzo_stimato = f"~{int((dist_km/100)*15)}€"
                return dist_m, duration_min, f"Volo consigliato: {prezzo_stimato}. Check-in incluso.", "✈️ Volo Interno (Garuda/LionAir)"
            else: # Treno / Bus
                duration_min = round(dist_km / 80.0 * 60) # Stima treni KAI in Indonesia
                prezzo_stimato = f"~{int((dist_km/100)*8)}€"
                return dist_m, duration_min, f"Tratta coperta da Treno inter-city/Bus. Costo stimato: {prezzo_stimato}.", "🚆 Treno / Bus"
                
        except Exception as e:
            logger.error(f"Scraping Trasporti fallito: {e}")
            return self._fallback_routing(lat1, lon1, lat2, lon2)