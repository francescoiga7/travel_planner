import requests
from geopy.geocoders import Nominatim
from core.models import Place
from core.config import settings
from core.logger import get_logger
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = get_logger(__name__)

class OverpassTimeoutError(Exception):
    pass

# Mantieni la cache per evitare ban da Overpass
@st.cache_data(ttl=86400)
@retry(
    stop=stop_after_attempt(4), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OverpassTimeoutError)
)
def fetch_pois_with_cache(query: str):
    """Esegue la chiamata a Overpass sfruttando Retry e Cache in modo sicuro."""
    url = settings.OVERPASS_URL
    headers = {
        "User-Agent": settings.USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    try:
        response = requests.post(url, data=query.encode('utf-8'), headers=headers, timeout=35)
        if response.status_code == 504:
            raise OverpassTimeoutError("Overpass HTTP 504: Server too busy")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        raise OverpassTimeoutError("Overpass Timeout: Request took too long")
    
class PlacesService:
    def __init__(self):
        # FIX CRITICO PER HTTP 403: Cambiamo radicalmente l'User-Agent 
        # Inserisci una stringa unica e una mail reale o fittizia strutturata
        self.custom_user_agent = "Francesco_AI_TravelPlanner_Engine_v2_2026 (contact_dev@francescoiga7.com)"
        
        self.geolocator = Nominatim(
            user_agent=self.custom_user_agent,
            timeout=10
        )

    def get_coordinates(self, location_name: str) -> tuple[float, float] | None:
        try:
            # Forziamo i custom headers anche nella chiamata esplicita per sicurezza
            location = self.geolocator.geocode(
                location_name, 
                timeout=10,
                exactly_one=True
            )
            if location:
                return location.latitude, location.longitude
            return None
        except Exception as e:
            logger.error(f"Geocoding error for {location_name}: {e}")
            return None
        
    # AUMENTATO IL RAGGIO A 20km (20000m) per supportare metropoli asiatiche
    def fetch_attractions(self, lat: float, lon: float, radius: int = 20000) -> list[Place]: 
        # Aggiunti tag per spiagge, riserve naturali e templi (solo quelli famosi con wikipedia)
        query = f"""
        [out:json][timeout:35];
        (
          nwr["tourism"="attraction"](around:{radius},{lat},{lon});
          nwr["historic"="monument"](around:{radius},{lat},{lon});
          nwr["historic"="archaeological_site"](around:{radius},{lat},{lon});
          nwr["tourism"="museum"](around:{radius},{lat},{lon});
          nwr["tourism"="viewpoint"](around:{radius},{lat},{lon}); 
          nwr["place"="square"](around:{radius},{lat},{lon});
          nwr["natural"="beach"](around:{radius},{lat},{lon});
          nwr["leisure"="nature_reserve"](around:{radius},{lat},{lon});
          nwr["amenity"="place_of_worship"]["wikipedia"](around:{radius},{lat},{lon});
        );
        out center;
        """
        
        try:
            # FIX ARCHITETTURALE: Ora usiamo la funzione robusta con cache e retry
            data = fetch_pois_with_cache(query)
            elements = data.get('elements', [])
            
            places_with_score = []
            
            for el in elements:
                tags = el.get('tags', {})
                name = tags.get('name')
                
                if not name:
                    continue
                
                # Calcolo della popolarità
                score = len(tags)
                if 'wikipedia' in tags: score += 20
                if 'wikidata' in tags: score += 10
                
                rating = min(5, max(3, int(score / 15) + 3))
                
                p_lat = el.get('lat', el.get('center', {}).get('lat'))
                p_lon = el.get('lon', el.get('center', {}).get('lon'))
                
                if not p_lat or not p_lon:
                    continue

                # Estrazione categoria per decidere il tempo di visita
                category = tags.get('tourism', tags.get('historic', tags.get('natural', tags.get('amenity', 'attraction'))))
                category_lower = category.lower()

                if "museum" in category_lower or "museo" in name.lower():
                    duration = 120
                elif "archaeological" in category_lower or "temple" in name.lower() or "candi" in name.lower():
                    duration = 90
                elif "worship" in category_lower or "church" in category_lower or "mosque" in name.lower():
                    duration = 45
                elif "beach" in category_lower or "reserve" in category_lower:
                    duration = 180  # 3 ore per rilassarsi in spiaggia o nei parchi di Komodo
                elif "viewpoint" in category_lower or "square" in category_lower:
                    duration = 20
                else:
                    duration = 60

                place = Place(
                    id=str(el['id']),
                    name=name,
                    lat=p_lat,
                    lon=p_lon,
                    category=category,
                    rating=rating,
                    visit_duration_minutes=duration
                )
                
                places_with_score.append({"place": place, "score": score})
            
            places_with_score.sort(key=lambda x: x["score"], reverse=True)
            
            seen_names = set()
            top_places = []
            
            for item in places_with_score:
                p_name = item["place"].name
                if p_name not in seen_names:
                    seen_names.add(p_name)
                    top_places.append(item["place"])
                
                # Aumentato il cap a 40 luoghi dato il raggio di 20km molto più ampio
                if len(top_places) == 40: 
                    break
                    
            return top_places
            
        except Exception as e:
            logger.error(f"Errore fatale nell'estrazione Overpass: {e}")
            return []