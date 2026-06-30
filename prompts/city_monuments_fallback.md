Task: Identify the 10 most famous monuments, museums, or tourist attractions EXCLUSIVELY within the city of '{city_name}'.

CRITICAL INSTRUCTION: Provide the "name" of the monument in Italian (or English if Italian is unavailable). DO NOT use native scripts (e.g., Japanese Kanji, Arabic, etc.). You must respond ONLY with a valid JSON object.

Target JSON Schema:
{
  "places": [
    {
      "id": "fallback_city_1",
      "name": "Nome in Italiano (es. Tempio Senso-ji, non 金龍山浅草寺)",
      "lat": 35.7148,
      "lon": 139.7967,
      "category": "monument",
      "rating": 5
    }
  ]
}