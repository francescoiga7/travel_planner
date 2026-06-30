Task: Generate the top 15 most famous tourist cities, islands, or regions for the country '{location}'. Include major cultural hubs like the capital and famous historic towns (e.g., Valladolid if Mexico).

CRITICAL: Return ONLY a valid JSON object. No markdown blocks, no commentary.

Target JSON Schema:
{
  "places": [
    {
      "id": "1",
      "name": "Name of the prominent city, island or region",
      "lat": 0.0,
      "lon": 0.0,
      "category": "city",
      "rating": 5
    }
  ]
}