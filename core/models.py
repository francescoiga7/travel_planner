from pydantic import BaseModel, Field

class Place(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    category: str
    rating: int = Field(ge=1, le=5, description="Simulated 1-5 rating based on popularity")
    visit_duration_minutes: int = 60  # <-- NUOVO: Tempo medio di permanenza stimato (default 1 ora)

class RouteSegment(BaseModel):
    from_place: str
    to_place: str
    distance_meters: float
    duration_minutes: float
    transport_mode: str
    arrival_time: str | None = None  # <-- NUOVO: es. "09:15"
    departure_time: str | None = None  # <-- NUOVO: es. "11:15" dopo la visita
    additional_info: str | None = None

class ItineraryDay(BaseModel):
    day_number: int
    places_visited: list[Place]
    segments: list[RouteSegment]