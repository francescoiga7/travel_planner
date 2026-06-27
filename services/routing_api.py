import requests
import networkx as nx
import streamlit as st
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import logging

# Sostituisce: from core.logger import logger
logger = logging.getLogger("travel_planner.routing")

class RoutingService:
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def get_osrm_matrix(coordinates: list[tuple[float, float]], profile: str = "foot") -> list[list[float]]:
        """
        Interroga l'API pubblica di OSRM per ottenere la matrice dei tempi di percorrenza (NxN).
        
        Args:
            coordinates: Lista di tuple (lon, lat)
            profile: 'foot' per percorsi pedonali urbani, 'car' per spostamenti stradali
        Returns:
            Matrice bidimensionale NxN con i tempi in secondi.
        """
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
                raise ValueError("Risposta OSRM malformata o vuota.")
                
        except Exception as e:
            logger.error(f"Errore OSRM API: {e}. Avvio del fallback geometrico.")
            return RoutingService._generate_fallback_matrix(coordinates, profile)

    @staticmethod
    def _generate_fallback_matrix(coordinates: list[tuple[float, float]], profile: str) -> list[list[float]]:
        """
        Genera una matrice di fallback basata sulla distanza geodetica (Haversine)
        calcolando una velocità media stimata a seconda del profilo.
        """
        n = len(coordinates)
        matrix = [[0.0] * n for _ in range(n)]
        
        # Velocità stimate in km/h: 4.5 km/h a piedi, 40 km/h in auto (traffico urbano medio)
        speed_kmh = 4.5 if profile == "foot" else 40.0
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    # geopy usa (lat, lon) mentre OSRM usa (lon, lat)
                    coord_i = (coordinates[i][1], coordinates[i][0])
                    coord_j = (coordinates[j][1], coordinates[j][0])
                    
                    dist_km = geodesic(coord_i, coord_j).km
                    # Calcolo del tempo in secondi: (distanza / velocità) * 3600 secondi/ora
                    matrix[i][j] = (dist_km / speed_kmh) * 3600
        return matrix

    @classmethod
    def optimize_poi_route(cls, pois: list[dict], profile: str = "foot", start_idx: int = 0) -> list[dict]:
        """
        Ottimizza l'ordine dei POI utilizzando un algoritmo geospaziale deterministico (TSP).
        Rimuove la componente algoritmica dall'LLM per evitare allucinazioni strutturali.
        
        Args:
            pois: Lista di dizionari, ognuno contenente le chiavi 'lat' e 'lon'
            profile: 'foot' o 'car'
            start_idx: Indice del POI di partenza (es. l'Hotel del giorno)
        Returns:
            Lista di POI riordinata secondo l'ottimizzazione del percorso.
        """
        if len(pois) <= 2:
            return pois

        coordinates = [(poi['lon'], poi['lat']) for poi in pois]
        duration_matrix = cls.get_osrm_matrix(coordinates, profile)
        
        # Costruzione del Grafo completo pesato tramite NetworkX
        G = nx.complete_graph(len(pois))
        for i in range(len(pois)):
            for j in range(len(pois)):
                if i != j:
                    # Il peso dell'arco è il tempo di percorrenza in secondi
                    G[i][j]['weight'] = duration_matrix[i][j]
                    
        try:
            # Risoluzione approssimata del Traveling Salesperson Problem (Algoritmo di Christofides/Heuristics)
            tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
            
            # Rimuoviamo l'ultimo elemento restituito da NetworkX che chiude il ciclo tornando al punto di partenza
            tsp_path_linear = tsp_path[:-1]
            
            # Ruotiamo il vettore degli indici per assicurarci che parta dallo start_idx specificato
            if start_idx in tsp_path_linear:
                start_pos = tsp_path_linear.index(start_idx)
                ordered_indices = tsp_path_linear[start_pos:] + tsp_path_linear[:start_pos]
            else:
                ordered_indices = tsp_path_linear
                
        except Exception as e:
            logger.error(f"Errore durante l'ottimizzazione TSP con NetworkX: {e}. Restituisco ordine originale.")
            ordered_indices = list(range(len(pois)))
            
        return [pois[idx] for idx in ordered_indices]

    @staticmethod
    @st.cache_data(ttl=86400)
    def get_macro_transit_info(origin_name: str, destination_name: str) -> dict:
        """
        Simula le funzionalità macro di Rome2Rio/Google Maps calcolando le rotte inter-city
        e stimando costi e tempi di percorrenza logistici a seconda della distanza reale.
        
        Args:
            origin_name: Nome della città di partenza (es. "Yogyakarta")
            destination_name: Nome della città di arrivo (es. "Bali")
        Returns:
            Dizionario con distanza in km e opzioni di trasporto ipotizzate.
        """
        geolocator = Nominatim(user_agent="travel_planner_engine_francesco_2026")
        
        try:
            loc_a = geolocator.geocode(origin_name, timeout=10)
            loc_b = geolocator.geocode(destination_name, timeout=10)
            
            if not loc_a or not loc_b:
                logger.warning(f"Geocoding fallito per una delle seguenti località: {origin_name} o {destination_name}")
                return {"distance_km": 0, "options": [], "status": "Geocoding failed"}
                
            dist_km = geodesic((loc_a.latitude, loc_a.longitude), (loc_b.latitude, loc_b.longitude)).km
            options = []
            
            # Logica Euristica di instradamento Macro
            if dist_km > 350:
                # Opzione Aerea (Es. Voli Indonesia / Messico tra hub lontani)
                options.append({
                    "mode": "Volo Interno",
                    "duration": f"{round(dist_km / 650 + 2, 1)} ore (incluso check-in)",
                    "price_estimate": f"€{round(dist_km * 0.10 + 25, 2)}",
                    "details": f"Connessione aerea raccomandata tra gli aeroporti principali più vicini."
                })
            
            if dist_km < 600:
                # Opzione Ferroviaria o Bus a lungo raggio (Es. Tratte interne o nazionali)
                options.append({
                    "mode": "Treno Alta Velocità / Bus Espresso",
                    "duration": f"{round(dist_km / 85 + 0.5, 1)} ore",
                    "price_estimate": f"€{round(dist_km * 0.05 + 8, 2)}",
                    "details": "Verificare la disponibilità di ferrovie statali o linee bus di prima classe."
                })
                
            if dist_km < 150:
                # Opzione Driver Privato o Taxi di linea
                options.append({
                    "mode": "Driver Privato / Taxi",
                    "duration": f"{round(dist_km / 60, 1)} ore",
                    "price_estimate": f"€{round(dist_km * 0.45 + 10, 2)}",
                    "details": "Consigliato per massimizzare la flessibilità o se si viaggia in gruppo."
                })

            return {
                "distance_km": round(dist_km, 2),
                "options": options,
                "status": "Success"
            }
            
        except Exception as e:
            logger.error(f"Errore nel calcolo del macro transit info: {e}")
            return {"distance_km": 0, "options": [], "status": f"Error: {str(e)}"}
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def get_walking_route(p1: dict, p2: dict) -> tuple[float, float]:
        """
        Calcola la distanza (in metri) e la durata (in secondi) a piedi tra due punti.
        Accetta dizionari o oggetti che hanno le chiavi/attributi 'lon' e 'lat'.
        
        Returns:
            tuple: (distanza_metri, durata_secondi)
        """
        # Estrazione flessibile sia se p1/p2 sono dizionari, sia se sono oggetti Pydantic
        lon1 = p1.get('lon') if isinstance(p1, dict) else getattr(p1, 'lon', None)
        lat1 = p1.get('lat') if isinstance(p1, dict) else getattr(p1, 'lat', None)
        lon2 = p2.get('lon') if isinstance(p2, dict) else getattr(p2, 'lon', None)
        lat2 = p2.get('lat') if isinstance(p2, dict) else getattr(p2, 'lat', None)

        if None in [lon1, lat1, lon2, lat2]:
            logger.error(f"Coordinate non valide per get_walking_route: p1={p1}, p2={p2}")
            return 0.0, 0.0

        url = f"http://router.project-osrm.org/route/v1/foot/{lon1},{lat1};{lon2},{lat2}?overview=false"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                distance = route["distance"]  # in metri
                duration = route["duration"]  # in secondi
                return distance, duration
            else:
                raise ValueError("Nessuna rotta trovata da OSRM.")
                
        except Exception as e:
            logger.error(f"Errore get_walking_route OSRM: {e}. Fallback geometrico.")
            # Fallback immediato con geopy (Velocità stimata 4.5 km/h -> 1.25 m/s)
            dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
            dist_m = dist_km * 1000
            duration_s = dist_m / 1.25
            return dist_m, duration_s