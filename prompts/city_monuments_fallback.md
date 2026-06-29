Task: Identifica i 10 monumenti, musei o attrazioni turistiche più famose in assoluto ESCLUSIVAMENTE all'interno o nelle immediate vicinanze della città di '{city_name}'.
Non inserire altre città o regioni distanti. Cerca solo attrazioni proprie di questa specifica città.

Usa ESATTAMENTE questo schema JSON, senza aggiungere spiegazioni o testo prima/dopo:
{{
  "places": [
    {{
      "id": "fallback_{city_name}_1",
      "name": "Nome del Monumento Reale (es. Monas o National Museum)",
      "lat": -6.1754,
      "lon": 106.8272,
      "category": "museum",
      "rating": 5
    }}
  ]
}}