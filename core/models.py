from pydantic import BaseModel, Field

class Place(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    category: str
    rating: int = Field(ge=1, le=5, description="Simulated 1-5 rating based on popularity")

class RouteSegment(BaseModel):
    from_place: str
    to_place: str
    distance_meters: float
    duration_minutes: float
    transport_mode: str
    additional_info: str | None = None  # e.g., "Metro Linea A, 1.50€" or "Volo diretto, 50€"

class ItineraryDay(BaseModel):
    day_number: int
    places_visited: list[Place]
    segments: list[RouteSegment]