import json
import re
import requests
from pathlib import Path
from core.models import Place
from core.config import settings
from core.logger import get_logger
from geopy.geocoders import Nominatim

logger = get_logger(__name__)

class LLMEngine:
    def __init__(self) -> None:
        self.api_url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        self.model = settings.OLLAMA_MODEL
        self.base_dir = Path(__file__).resolve().parent.parent

    def _load_prompt(self, filename: str) -> str:
        """Carica in modo sicuro i prompt esterni (.md) mantenendo l'architettura pulita."""
        prompt_path = self.base_dir / "prompts" / filename
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Impossibile caricare il prompt {filename}: {e}")
            raise FileNotFoundError(f"Prompt file missing: {prompt_path}")

    def _generate_chat(self, payload: dict) -> str:
        """Invia la richiesta direttamente all'endpoint di Ollama."""
        try:
            response = requests.post(self.api_url, json=payload, timeout=180)
            if not response.ok:
                logger.error(f"Errore HTTP API Ollama: {response.status_code} - {response.text}")
                return ""
            return response.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Eccezione di rete verso Ollama: {e}")
            return ""

    def _execute_json_request(self, system_role: str, prompt: str, num_predict: int = 4096) -> str:
        """Invia il payload a Ollama forzando rigidamente la modalità JSON nativa."""
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": f"{system_role} Respond ONLY with raw JSON. No markdown formatting, no code blocks, no backticks. Start the response with '{{'."
                },
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0, 
                "num_ctx": 4096, 
                "num_predict": num_predict
            }
        }
        return self._generate_chat(payload)

    def _repair_truncated_json(self, raw_text: str) -> dict | None:
        """Tenta di riparare al volo un JSON troncato o malformato dall'LLM."""
        raw_text = raw_text.strip()
        if not raw_text:
            return None
            
        if raw_text.startswith('"places"') or raw_text.startswith("'places'"):
            raw_text = "{" + raw_text
            
        if raw_text.endswith(","):
            raw_text = raw_text[:-1]
            
        open_braces = raw_text.count("{")
        close_braces = raw_text.count("}")
        open_brackets = raw_text.count("[")
        close_brackets = raw_text.count("]")
        
        try:
            if open_braces > close_braces:
                raw_text += "}" * (open_braces - close_braces)
            if open_brackets > close_brackets:
                raw_text += "]"
                if raw_text.count("{") > raw_text.count("}"):
                    raw_text += "}"
            return json.loads(raw_text)
        except Exception:
            return None

    def _extract_and_parse_json(self, raw_text: str) -> dict | None:
        if not raw_text:
            return None
        
        cleaned_text = raw_text.strip()
        
        if cleaned_text.startswith('"places"') or cleaned_text.startswith("'places'"):
            cleaned_text = "{" + cleaned_text
        if not cleaned_text.endswith("}"):
            cleaned_text += "}"

        try:
            match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return json.loads(cleaned_text)
        except Exception as e:
            repaired = self._repair_truncated_json(cleaned_text)
            if repaired:
                return repaired
            logger.error(f"Impossibile parsare JSON: {e}. Raw input: {raw_text}")
            return None

    def get_country_hubs(self, country: str) -> list[str]:
        """Interroga Ollama caricando il prompt esterno per ottenere gli hub turistici principali."""
        try:
            template = self._load_prompt("attractions_fallback.md")
            prompt = template.format(location=country)
        except Exception:
            prompt = f"Identify the top 15 most important tourist cities or regions for {country}. Return a JSON object with a 'places' key containing a list of objects with a 'name' field."

        raw_response = self._execute_json_request(
            "Sei un'API geografica internazionale. Rispondi SOLO con JSON puro. Non troncare.", 
            prompt, 
            num_predict=2048
        )
        data = self._extract_and_parse_json(raw_response)
        
        if data and isinstance(data, dict):
            for key in ["places", "hubs", "cities", "regions"]:
                if key in data and isinstance(data[key], list):
                    hubs_list = data[key]
                    if hubs_list:
                        if isinstance(hubs_list[0], dict):
                            return [h.get("name") for h in hubs_list if h.get("name")]
                        return [str(h) for h in hubs_list]

            for val in data.values():
                if isinstance(val, list) and val:
                    if isinstance(val[0], dict):
                        return [item.get("name") for item in val if item.get("name")]
                    return [str(item) for item in val]

        logger.warning(f"Chiamata LLM non conforme per {country}. Avvio estrazione geografica reale ad alta importanza.")
        try:
            geolocator = Nominatim(user_agent="Francesco_AI_TravelPlanner_Engine_v2_2026")
            query_str = f"cities in {country}"
            locations = geolocator.geocode(query_str, exactly_one=False, limit=15, addressdetails=True)
            
            if locations:
                dynamic_hubs = []
                for loc in locations:
                    addr = loc.raw.get("address", {})
                    for addr_key in ["city", "town", "state", "county", "city_district"]:
                        name_val = addr.get(addr_key)
                        if name_val and name_val.lower() != country.lower() and name_val not in dynamic_hubs:
                            dynamic_hubs.append(name_val)
                if dynamic_hubs:
                    return dynamic_hubs
        except Exception as geo_err:
            logger.error(f"Errore nel geocoding di emergenza per {country}: {geo_err}")
            
        return ["Mexico City", "Cancun", "Valladolid", "Merida", "Oaxaca"] if country.lower() in ["messico", "mexico"] else []