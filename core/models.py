from pydantic import BaseModel, Field, ConfigDict # <-- Aggiungi ConfigDict

class Place(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    category: str
    rating: int = Field(ge=1, le=5, description="Simulated 1-5 rating based on popularity")
    visit_duration_minutes: int = 60  

class RouteSegment(BaseModel):
    from_place: str
    to_place: str
    distance_meters: float
    duration_minutes: float
    transport_mode: str
    arrival_time: str | None = None  
    departure_time: str | None = None  
    additional_info: str | None = None

class ItineraryDay(BaseModel):
    # FIX CRITICO: Dice a Pydantic di accettare l'istanza di Place anche se 
    # deriva da un contesto di caricamento/reload differente (Streamlit Rerun)
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    day_number: int
    places_visited: list[Place]
    segments: list[RouteSegment]