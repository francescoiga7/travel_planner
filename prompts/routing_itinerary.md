Task: Crea un itinerario di viaggio strutturato, ottimizzato e suddiviso in ORARI DETTAGLIATI per '{location}'.

Luoghi scelti dall'utente:
{places_context}

Distanze reali calcolate dall'engine (OSRM):
{distances_context}

REGOLE LOGISTICHE SULL'OTTIMIZZAZIONE ORARIA E GEOGRAFICA:
1. CLUSTERING REALE: Luoghi vicini (es. a Roma: Piazza San Pietro, Basilica di San Pietro e Castel Sant'Angelo) DEVONO essere inseriti nello stesso identico giorno, consecutivamente. Non separarli MAI in giorni diversi.
2. ISOLAMENTO MACRO-AREE: Il Colosseo fa parte dell'area archeologica centrale e deve occupare una mezza giornata dedicata (Giorno separato o blocco orario distinto, es. Mattina Colosseo, Pomeriggio Centro Storico).
3. STRUTTURA ORARIA: Ogni giorno deve essere suddiviso in slot temporali realistici (es. Mattina 09:00-12:30, Pranzo 12:30-14:30, Pomeriggio 14:30-18:30).
4. VERIFICA DEI MEZZI: 
   - Sotto i 1200 metri si va ESCLUSIVAMENTE a piedi (es. da San Pietro a Castel Sant'Angelo sono circa 800-900m a piedi dritti, NO METRO, NO BUS).
   - Sopra i 1500 metri si usano i mezzi pubblici (BIT 1.50€). La velocità a piedi standard è di 4.5 km/h.

Rispondi compilando ESATTAMENTE questo schema JSON:
{{
  "reasoning_logs": ["Spiegazione dei cluster geografici scelti e della distribution oraria"],
  "itinerary": [
    {{
      "day_number": 1,
      "places_visited": ["Nome esatto del luogo"],
      "segments": [
        {{
          "from_place": "Luogo A",
          "to_place": "Luogo B",
          "distance_meters": 900,
          "duration_minutes": 12,
          "transport_mode": "Piedi / Metro Linea B / Autobus",
          "additional_info": "Slot 09:00-11:00. Visita a X. Spostamento verso Y usando il mezzo indicato. Costo eventuale: 1.50€."
        }}
      ]
    }}
  ]
}}