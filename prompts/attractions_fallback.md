Task: Identify and generate the top 10 most famous and popular cities, islands, or macroeconomic tourist regions for the country '{location}'. These locations will act as primary hubs for building a travel itinerary. Provide real or highly approximated geographic latitude and longitude coordinates for the center of each macro-location.

You MUST respond with a valid JSON object matching this schema exactly. Do not include any conversational text, markdown code blocks (like ```json), or commentary.

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