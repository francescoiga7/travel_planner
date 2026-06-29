import os
import logging
import requests
import numpy as np
import googlemaps
import networkx as nx
import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
from sklearn.cluster import KMeans

logger = logging.getLogger("travel_planner.routing")

class RoutingService:
    def __init__(self):
        # Carica la chiave da ambiente o .env
        self.gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.gmaps = googlemaps.Client(key=self.gmaps_key) if self.gmaps_key else None

    def _fallback_routing(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float, str, str]:
        """
        Metodo di fallback deterministico usato quando Google Maps fallisce o manca la chiave API.
        Sfrutta il calcolo geometrico e OSRM locale a piedi.
        """
        p1 = {"lat": lat1, "lon": lon1}
        p2 = {"lat": lat2, "lon": lon2}
        
        dist_m, duration_s = self.get_walking_route(p1, p2)
        duration_min = round(duration_s / 60)
        
        # Regola euristica per differenziare i mezzi nel fallback offline
        if dist_m <= 1200:
            mode = "A piedi"
            info = f"Passeggiata urbana nel cluster (circa {dist_m:.0f}m)."
        elif dist_m <= 5000:
            mode = "Mezzi Pubblici (Bus/Metro)"
            duration_min = round((dist_m / 1000) / 12.0 * 60)  # stima 12 km/h urbani
            info = f"Distanza media ({dist_m/1000:.1f}km). Consigliato l'uso del trasporto pubblico locale."
        else:
            mode = "Treno / Taxi"
            duration_min = round((dist_m / 1000) / 40.0 * 60)  # stima 40 km/h extraurbani
            info = f"Spostamento a lungo raggio ({dist_m/1000:.1f}km). Verificare connessioni extraurbane o taxi."
            
        return dist_m, duration_min, info, mode

    def get_real_transit_route(self, p1_lat: float, p1_lon: float, p2_lat: float, p2_lon: float) -> tuple[float, float, str, str]:
        """Ottiene indicazioni reali su mezzi pubblici, fermate e orari tramite Google Maps."""
        if not self.gmaps:
            logger.warning("Google Maps API Key mancante nel .env. Avvio del fallback locale.")
            return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)

        try:
            now = datetime.now()
            directions = self.gmaps.directions(
                (p1_lat, p1_lon), (p2_lat, p2_lon),
                mode="transit",
                departure_time=now
            )
            
            if not directions:
                return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)

            leg = directions[0]['legs'][0]
            distance_m = leg['distance']['value']
            duration_min = leg['duration']['value'] // 60

            instructions = []
            transport_mode = "Misto / Piedi"
            
            for step in leg['steps']:
                if step['travel_mode'] == 'TRANSIT':
                    details = step['transit_details']
                    line_name = details['line'].get('short_name', details['line'].get('name', ''))
                    vehicle = details['line']['vehicle']['name']
                    stops = details.get('num_stops', 0)
                    departure = details['departure_time']['text']
                    
                    agency = ""
                    if 'agencies' in details['line']:
                        agency = details['line']['agencies'][0]['name']
                    
                    instructions.append(f"{vehicle} {line_name} ({agency}) - {stops} fermate. Partenza alle {departure}.")
                    transport_mode = vehicle

            info = " -> ".join(instructions) if instructions else f"Cammina per {distance_m}m verso la destinazione."
            return distance_m, duration_min, info, transport_mode
            
        except Exception as e:
            logger.error(f"Errore durante la chiamata a Google Maps: {e}. Attivazione fallback.")
            return self._fallback_routing(p1_lat, p1_lon, p2_lat, p2_lon)

    @classmethod
    @classmethod
    def build_deterministic_itinerary(cls, daily_clusters: dict, places_dict: dict, hotel_place=None, flight_info_str: str = "") -> list:
        router = cls() 
        itinerary = []
        
        # Analisi euristica dell'orario del volo sul Giorno 1
        # Se l'utente scrive "17:35" o "17.35", il Giorno 1 inizierà da quell'ora
        global_start_hour = 9
        global_start_minute = 0
        if flight_info_str:
            import re
            time_match = re.search(r'(\d{2})[:\.](\d{2})', flight_info_str)
            if time_match:
                global_start_hour = int(time_match.group(1))
                global_start_minute = int(time_match.group(2))

        for day_num, places_in_day in daily_clusters.items():
            if not places_in_day:
                continue
            
            ordered_places = []
            if hotel_place:
                pois_for_tsp = [{"lat": hotel_place.lat, "lon": hotel_place.lon, "id": hotel_place.id}]
                for p in places_in_day:
                    pois_for_tsp.append({"lat": p.lat, "lon": p.lon, "id": p.id})
                
                ordered_pois_dicts = cls.optimize_poi_route(pois_for_tsp, profile="foot", start_idx=0)
                ordered_places = [places_dict[p["id"]] for p in ordered_pois_dicts if p["id"] in places_dict] if ordered_pois_dicts else [hotel_place] + places_in_day
                
                if ordered_places and ordered_places[0].id != hotel_place.id:
                    ordered_places.remove(hotel_place)
                    ordered_places.insert(0, hotel_place)
            else:
                pois_for_tsp = [{"lat": p.lat, "lon": p.lon, "id": p.id} for p in places_in_day]
                ordered_pois_dicts = cls.optimize_poi_route(pois_for_tsp, profile="foot")
                ordered_places = [places_dict[p["id"]] for p in ordered_pois_dicts if p["id"] in places_dict] if ordered_pois_dicts else places_in_day

            # Impostazione del clock iniziale della giornata
            current_hour = global_start_hour if day_num == 1 else 9
            current_minute = global_start_minute if day_num == 1 else 0
            
            segments = []
            for i in range(len(ordered_places)-1):
                p1, p2 = ordered_places[i], ordered_places[i+1]
                
                dist_m, duration_min, info, mode = router.get_real_transit_route(p1.lat, p1.lon, p2.lat, p2.lon)
                
                # --- FIX CRITICO: TRASFERIMENTO INTERCITY ---
                # Se la distanza è superiore a 50km, stiamo cambiando isola o città.
                # Non possiamo sommare 1800 minuti linearmente sul clock della giornata urbana!
                if dist_m > 50000:
                    mode = "Volo Interno / Treno Intercity"
                    duration_min = 120  # Fissiamo un tempo standard di viaggio simulato di 2 ore
                    info = f"Spostamento a lungo raggio intercity ({dist_m/1000:.1f} km). Trasferimento logistico programmato."
                
                dep_time_str = f"{current_hour:02d}:{current_minute:02d}"
                
                current_minute += int(duration_min)
                current_hour += current_minute // 60
                current_minute = current_minute % 60
                
                # Protezione overflow ore (se supera le 24 ore a causa di un vecchio dato, lo forziamo a un orario realistico)
                if current_hour >= 24:
                    current_hour = current_hour % 24
                
                arr_time_str = f"{current_hour:02d}:{current_minute:02d}"
                
                # Se il Giorno 1 inizia tardi causa volo, riduciamo a 0 i minuti spesi nei monumenti (solo check-in in hotel)
                if day_num == 1 and global_start_hour >= 17:
                    visit_duration = 0
                else:
                    visit_duration = p2.visit_duration_minutes if p2.id != "hotel_hub_node" else 0
                
                time_info = f"⏱️ Orario: {dep_time_str} -> {arr_time_str}."
                if visit_duration > 0:
                    time_info += f" Visita programmata di {visit_duration} min (fino alle "
                    future_minute = current_minute + visit_duration
                    future_hour = current_hour + (future_minute // 60)
                    future_minute = future_minute % 60
                    if future_hour >= 24: future_hour = future_hour % 24
                    
                    time_info += f"{future_hour:02d}:{future_minute:02d})."
                    current_hour = future_hour
                    current_minute = future_minute
                
                segments.append({
                    "from_place": p1.name,
                    "to_place": p2.name,
                    "distance_meters": dist_m,
                    "duration_minutes": duration_min,
                    "transport_mode": mode,
                    "arrival_time": arr_time_str,
                    "departure_time": dep_time_str,
                    "additional_info": f"{time_info} | {info}"
                })
            
            # Rientro serale in hotel
            if hotel_place and ordered_places:
                last_place = ordered_places[-1]
                if last_place.id != hotel_place.id:
                    dist_m, duration_min, info, mode = router.get_real_transit_route(
                        last_place.lat, last_place.lon, hotel_place.lat, hotel_place.lon
                    )
                    if dist_m > 50000:
                        dist_m = 0
                        duration_min = 15
                        mode = "Arrivo presso Alloggio"
                    
                    dep_time_str = f"{current_hour:02d}:{current_minute:02d}"
                    current_minute += int(duration_min)
                    current_hour += current_minute // 60
                    current_minute = current_minute % 60
                    if current_hour >= 24: current_hour = current_hour % 24
                    arr_time_str = f"{current_hour:02d}:{current_minute:02d}"
                    
                    segments.append({
                        "from_place": last_place.name,
                        "to_place": f"Rientro in Hotel: {hotel_place.name}",
                        "distance_meters": dist_m,
                        "duration_minutes": duration_min,
                        "transport_mode": mode,
                        "arrival_time": arr_time_str,
                        "departure_time": dep_time_str,
                        "additional_info": f"🌙 Fine giornata. Rientro per le {arr_time_str}. {info}"
                    })
                    ordered_places.append(hotel_place)

            itinerary.append({
                "day_number": day_num,
                "places_visited": ordered_places,
                "segments": segments
            })
            
        return itinerary

    @classmethod
    def optimize_poi_route(cls, pois: list[dict], profile: str = "foot", start_idx: int = 0) -> list[dict]:
        """
        Ottimizza l'ordine dei POI utilizzando un algoritmo geospaziale deterministico (TSP).
        Garantisce SEMPRE il ritorno di una lista valida di dizionari, anche in caso di errore.
        """
        if not pois or len(pois) <= 2:
            return pois if pois is not None else []

        try:
            coordinates = [(poi['lon'], poi['lat']) for poi in pois]
            duration_matrix = cls.get_osrm_matrix(coordinates, profile)
            
            if not duration_matrix or len(duration_matrix) != len(pois):
                logger.warning("Matrice OSRM non valida per il TSP. Uso l'ordine originale.")
                return pois

            G = nx.complete_graph(len(pois))
            for i in range(len(pois)):
                for j in range(len(pois)):
                    if i != j:
                        G[i][j]['weight'] = duration_matrix[i][j]
                        
            tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
            tsp_path_linear = tsp_path[:-1]
            
            if start_idx in tsp_path_linear:
                start_pos = tsp_path_linear.index(start_idx)
                ordered_indices = tsp_path_linear[start_pos:] + tsp_path_linear[:start_pos]
            else:
                ordered_indices = tsp_path_linear
                
            return [pois[idx] for idx in ordered_indices]
                
        except Exception as e:
            logger.error(f"Errore durante l'ottimizzazione TSP con NetworkX: {e}. Restituisco ordine originale.")
            return pois

    @staticmethod
    def cluster_pois_by_day(pois: list, num_days: int) -> dict[int, list]:
        """Raggruppa i POI in N giorni usando K-Means sulle coordinate spaziali."""
        if not pois:
            return {}
        if num_days >= len(pois):
            return {i+1: [pois[i]] for i in range(len(pois))}
            
        coords = np.array([[p.lat, p.lon] for p in pois])
        kmeans = KMeans(n_clusters=num_days, random_state=42, n_init="auto").fit(coords)
        
        clusters = {i+1: [] for i in range(num_days)}
        for poi, label in zip(pois, kmeans.labels_):
            clusters[label + 1].append(poi)
            
        return clusters

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_osrm_matrix(coordinates: list[tuple[float, float]], profile: str = "foot") -> list[list[float]]:
        """Interroga l'API pubblica di OSRM per ottenere la matrice dei tempi di percorso (NxN)."""
        if not coordinates:
            return []
            
        coords_str = ";".join([f"{lon},{lat}" for lon, lat in coordinates])
        url = f"http://router.project-osrm.org/table/v1/{profile}/{coords_str}?annotations=duration"
        
        try:
            logger.info(f"Richiesta matrice OSRM ({profile}) per {len(coordinates)} punti.")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "durations" in data and data["durations"]:
                return data["durations"]
            else:
                raise ValueError("Risposta OSRM vuota o malformata.")
        except Exception as e:
            logger.error(f"Errore OSRM API: {e}. Avvio del fallback geometrico.")
            return RoutingService._generate_fallback_matrix(coordinates, profile)

    @staticmethod
    def _generate_fallback_matrix(coordinates: list[tuple[float, float]], profile: str) -> list[list[float]]:
        """Genera una matrice di fallback basata sulla distanza geodetica."""
        n = len(coordinates)
        matrix = [[0.0] * n for _ in range(n)]
        speed_kmh = 4.5 if profile == "foot" else 40.0
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    coord_i = (coordinates[i][1], coordinates[i][0])
                    coord_j = (coordinates[j][1], coordinates[j][0])
                    dist_km = geodesic(coord_i, coord_j).km
                    matrix[i][j] = (dist_km / speed_kmh) * 3600
        return matrix

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_walking_route(p1: dict, p2: dict) -> tuple[float, float]:
        """Calcola distanza (metri) e durata (secondi) a piedi tra due punti."""
        lon1 = p1.get('lon') if isinstance(p1, dict) else getattr(p1, 'lon', None)
        lat1 = p1.get('lat') if isinstance(p1, dict) else getattr(p1, 'lat', None)
        lon2 = p2.get('lon') if isinstance(p2, dict) else getattr(p2, 'lon', None)
        lat2 = p2.get('lat') if isinstance(p2, dict) else getattr(p2, 'lat', None)

        if None in [lon1, lat1, lon2, lat2]:
            return 0.0, 0.0

        url = f"http://router.project-osrm.org/route/v1/foot/{lon1},{lat1};{lon2},{lat2}?overview=false"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "routes" in data and len(data["routes"]) > 0:
                return data["routes"][0]["distance"], data["routes"][0]["duration"]
            raise ValueError("Nessuna rotta trovata.")
        except Exception as e:
            logger.error(f"Errore OSRM: {e}. Fallback geometrico.")
            dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
            dist_m = dist_km * 1000
            return dist_m, dist_m / 1.25  # stimando un passo a 1.25 m/s (4.5 km/h)