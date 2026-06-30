Task: Identify the 10 most famous monuments or tourist attractions strictly inside the city of '{city_name}'.

CRITICAL INSTRUCTIONS FOR LINGUISTIC CLEANING:
1. "name": Must be ONLY the concise name of the place, translated into ITALIAN or short ENGLISH (e.g., use "Zocalo" or "Cattedrale di Città del Messico", NOT "Catedral Metropolitana de la Asunción de la Santísima Virgen María a los Cielos").
2. DO NOT include descriptions, addresses, or commentary inside the name field. Maximum 5 words per name.
3. Respond ONLY with a valid compact JSON object matching the schema below. No markdown formatting, no commentary.

Target JSON Schema:
{
  "places": [
    {
      "id": "fallback_city_1",
      "name": "Concise Name (e.g., Centro Storico)",
      "lat": 0.0,
      "lon": 0.0,
      "category": "monument",
      "rating": 5
    }
  ]
}