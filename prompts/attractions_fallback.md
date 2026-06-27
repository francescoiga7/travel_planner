Task: Identifica e genera le 10 città, isole o macro-regioni turistiche principali e più famose in assoluto per '{location}'. 
Questi punti fungeranno da tappe principali (hub) per costruire un itinerario.
Fornisci coordinate lat/lon reali o altamente approssimate del centro di ciascuna macro-località.

Usa ESATTAMENTE questo schema JSON:
{{
  "places": [
    {{
      "id": "1",
      "name": "Nome Città o Isola (es. Yogyakarta o Bali)",
      "lat": -7.7956,
      "lon": 110.3695,
      "category": "city",
      "rating": 5
    }}
  ]
}}