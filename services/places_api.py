import requests
from geopy.geocoders import Nominatim
from core.models import Place
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

import streamlit as st
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class OverpassTimeoutError(Exception):
    pass

# Cacha i risultati per evitare di colpire Overpass due volte per la stessa città
@st.cache_data(ttl=86400) # Cache per 24 ore
# Se riceviamo un 504, riprova fino a 4 volte aspettando 2, 4, 8 secondi.
@retry(
    stop=stop_after_attempt(4), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OverpassTimeoutError)
)
def fetch_pois(query: str):
    url = "http://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={'data': query}, timeout=25)
        
        if response.status_code == 504:
            raise OverpassTimeoutError("Overpass HTTP 504: Server too busy")
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        raise OverpassTimeoutError("Overpass Timeout: Request took too long")

class PlacesService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent=settings.USER_AGENT)

    def get_coordinates(self, location_name: str) -> tuple[float, float] | None:
        """Fetch lat/lon for a given city or country."""
        try:
            location = self.geolocator.geocode(location_name)
            if location:
                return location.latitude, location.longitude
            return None
        except Exception as e:
            logger.error(f"Geocoding error for {location_name}: {e}")
            return None

    def fetch_attractions(self, lat: float, lon: float, radius: int = 2500) -> list[Place]:
        """
        Uses Overpass API (OpenStreetMap) to fetch real attractions.
        Includes a custom scoring algorithm to prioritize famous landmarks.
        """
        # FIX 1: Usiamo 'nwr' (node, way, relation) invece di solo 'node' 
        # per catturare grandi monumenti come il Colosseo o intere piazze.
        # Aggiunto anche il tag archeologico.
        query = f"""
        [out:json][timeout:30];
        (
          nwr["tourism"="attraction"](around:{radius},{lat},{lon});
          nwr["historic"="monument"](around:{radius},{lat},{lon});
          nwr["historic"="archaeological_site"](around:{radius},{lat},{lon});
          nwr["tourism"="museum"](around:{radius},{lat},{lon});
        );
        out center;
        """
        
        headers = {
            "User-Agent": settings.USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        
        try:
            response = requests.post(
                settings.OVERPASS_URL, 
                data=query.encode('utf-8'), 
                headers=headers,
                timeout=35
            )
            response.raise_for_status()
            elements = response.json().get('elements', [])
            
            places_with_score = []
            
            for el in elements:
                tags = el.get('tags', {})
                name = tags.get('name')
                
                # Scartiamo elementi senza nome
                if not name:
                    continue
                
                # FIX 2: Algoritmo di "Fama" basato sulla ricchezza dei metadati.
                # I monumenti famosi hanno sempre i link a wikipedia/wikidata e decine di tag.
                score = len(tags)
                if 'wikipedia' in tags: 
                    score += 20
                if 'wikidata' in tags: 
                    score += 10
                    
                # Simuliamo un rating da 3 a 5 stelle basato sullo score
                rating = min(5, max(3, int(score / 15) + 3))
                
                # Se è una way/relation, le coordinate sono in 'center', altrimenti in 'lat'/'lon'
                p_lat = el.get('lat', el.get('center', {}).get('lat'))
                p_lon = el.get('lon', el.get('center', {}).get('lon'))
                
                if not p_lat or not p_lon:
                    continue

                category = tags.get('tourism', tags.get('historic', 'attraction'))

                place = Place(
                    id=str(el['id']),
                    name=name,
                    lat=p_lat,
                    lon=p_lon,
                    category=category,
                    rating=rating
                )
                
                places_with_score.append({"place": place, "score": score})
            
            # Ordiniamo i risultati dal più famoso (score più alto) al meno famoso
            places_with_score.sort(key=lambda x: x["score"], reverse=True)
            
            # Deduplichiamo mantenendo l'ordine di importanza e prendiamo i primi 20
            seen_names = set()
            top_places = []
            
            for item in places_with_score:
                p_name = item["place"].name
                if p_name not in seen_names:
                    seen_names.add(p_name)
                    top_places.append(item["place"])
                
                if len(top_places) == 20:
                    break
                    
            return top_places
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Overpass API HTTP error: {e.response.status_code} - {e.response.text}")
            return []
        except requests.exceptions.Timeout:
            logger.error("Overpass API request timed out.")
            return []
        except Exception as e:
            logger.error(f"Overpass API error: {e}")
            return []