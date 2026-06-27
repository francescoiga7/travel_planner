import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3:8b")
    OVERPASS_URL: str = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
    OSRM_BASE_URL: str = os.getenv("OSRM_BASE_URL", "http://router.project-osrm.org")
    USER_AGENT: str = os.getenv("NOMINATIM_USER_AGENT", "TravelPlanner_App")

settings = Settings()