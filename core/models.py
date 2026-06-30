from pydantic import BaseModel, Field, ConfigDict

class Place(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    lat: float
    lon: float
    category: str
    rating: int = Field(ge=0, le=5, description="Simulated 1-5 rating based on popularity")
    visit_duration_minutes: int = 60  

class RouteSegment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    from_place: str
    to_place: str
    distance_meters: float
    duration_minutes: float
    transport_mode: str
    arrival_time: str | None = None  
    departure_time: str | None = None  
    additional_info: str | None = None

class ItineraryDay(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    day_number: int
    places_visited: list[Place] = Field(default_factory=list)
    segments: list[RouteSegment] = Field(default_factory=list)