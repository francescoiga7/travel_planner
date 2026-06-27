import json
import requests
from pathlib import Path
from core.models import Place, RouteSegment, ItineraryDay
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

class LLMEngine:
    def __init__(self) -> None:
        self.api_url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        self.model = settings.OLLAMA_MODEL
        self.base_dir = Path(__file__).resolve().parent.parent

    def _load_prompt(self, filename: str) -> str:
        """Helper per caricare i prompt esterni in modo sicuro."""
        prompt_path = self.base_dir / "prompts" / filename
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Impossibile caricare il prompt {filename}: {e}")
            raise FileNotFoundError(f"Prompt file missing: {prompt_path}")

    def _generate_chat(self, payload: dict) -> str:
        """Invia il payload ottimizzato direttamente a Ollama."""
        try:
            response = requests.post(self.api_url, json=payload, timeout=180)
            if not response.ok:
                logger.error(f"Errore HTTP API Ollama: {response.status_code} - {response.text}")
                return ""
            return response.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Eccezione di rete verso Ollama: {e}")
            return ""

    def fetch_attractions_fallback(self, location: str) -> list[Place]:
        """Genera attrazioni via LLM caricando il prompt dal file di fallback esterno."""
        try:
            template = self._load_prompt("attractions_fallback.md")
            prompt = template.format(location=location)
        except Exception as e:
            logger.error(f"Errore inizializzazione prompt fallback: {e}")
            return []

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Sei un'API JSON geografica. Rispondi ESCLUSIVAMENTE con l'oggetto JSON richiesto senza troncare."},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0,
                "num_ctx": 4096,
                "num_predict": 4096
            }
        }
        
        raw_response = self._generate_chat(payload)
        if not raw_response:
            return []
            
        try:
            data = json.loads(raw_response)
            places_data = data.get("places", [])
            return [Place(**p) for p in places_data]
        except Exception as e:
            logger.error(f"Errore parsing fallback JSON: {e}. Raw: {raw_response}")
            return []

    def optimize_and_enrich_itinerary(self, location: str, places: list[Place], distances: dict) -> tuple[list[ItineraryDay], list[str]]:
        """Ottimizza l'itinerario caricando il prompt dall'infrastruttura di file esterna."""
        places_context = "\n".join([f"- {p.name} ({p.lat},{p.lon})" for p in places])
        distances_context = "\n".join([f"{k[0]}->{k[1]}: {v['dist']}m, {v['time']}min" for k, v in distances.items()])
        
        try:
            template = self._load_prompt("routing_itinerary.md")
            prompt = template.format(
                location=location,
                places_context=places_context,
                distances_context=distances_context
            )
        except Exception as e:
            return [], [f"Errore inizializzazione prompt routing: {str(e)}"]

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Sei un motore di routing e ottimizzazione logistica. Rispondi solo in formato JSON valido."},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0,
                "num_ctx": 4096,
                "num_predict": 2048
            }
        }
        
        raw_response = self._generate_chat(payload)
        if not raw_response:
            return [], ["Errore: Nessun dato ricevuto da Ollama."]
            
        try:
            data = json.loads(raw_response)
            logs = data.get("reasoning_logs", [])
            itinerary = []
            place_dict = {p.name: p for p in places}
            
            for day in data.get("itinerary", []):
                day_places = [place_dict[name] for name in day.get("places_visited", []) if name in place_dict]
                validated_segments = []
                
                for seg in day.get("segments", []):
                    normalized_seg = {
                        "from_place": seg.get("from_place", ""),
                        "to_place": seg.get("to_place", ""),
                        "distance_meters": float(seg.get("distance_meters", seg.get("distance", seg.get("dist", 0.0)))),
                        "duration_minutes": float(seg.get("duration_minutes", seg.get("duration", seg.get("time", 0.0)))),
                        "transport_mode": seg.get("transport_mode", ""),
                        "additional_info": seg.get("additional_info", "")
                    }
                    validated_segments.append(RouteSegment(**normalized_seg))
                
                itinerary.append(ItineraryDay(
                    day_number=day.get("day_number", 1),
                    places_visited=day_places,
                    segments=validated_segments
                ))
                
            return itinerary, logs
            
        except Exception as e:
            logger.error(f"Errore parsing logistica oraria: {e}. Raw: {raw_response}")
            return [], [f"Errore validazione struttura: {str(e)}"]