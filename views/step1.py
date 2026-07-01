import streamlit as st
from datetime import datetime, timedelta
from core.models import Place
from core.config_map import get_country_data

def render_step1(places_svc, llm_svc) -> None:
    st.header("1. Scegli la destinazione e i dettagli del soggiorno")
    
    trip_type = st.radio("Tipo di destinazione", ["Città Singola (es: Roma)", "Nazione / Multi-tappa (es: Indonesia)"])
    location = st.text_input("Inserisci la destinazione", st.session_state.get("location", ""))
    
    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input("Data di Partenza", datetime.today())
    with col_end:
        end_date = st.date_input("Data di Ritorno", datetime.today() + timedelta(days=3))
        
    st.session_state.num_days = (end_date - start_date).days + 1
    st.session_state["start_date"] = start_date.strftime("%Y/%m/%d")
    
    st.markdown("### ✈️ Inserimento Codici Volo / Scali Principali")
    st.info("🤖 **Estrazione Automatica Attiva:** Inserisci solo il codice del volo (es. AM071, IB6401). Il sistema recupererà aeroporti e orari reali via scraping gratuito.")
    
    if "main_flights" not in st.session_state:
        st.session_state.main_flights = [{"code": ""}]
        
    flights_container = st.container()
    updated_flights = []
    
    with flights_container:
        for i, f_data in enumerate(st.session_state.main_flights):
            code = st.text_input(f"Codice Volo / Scalo #{i+1} (es: AM071)", value=f_data["code"], key=f"f_code_{i}")
            updated_flights.append({"code": code})
            
    if st.button("➕ Aggiungi Scalo Successivo"):
        st.session_state.main_flights = updated_flights + [{"code": ""}]
        st.rerun()
        
    st.session_state.main_flights = updated_flights
    
    if updated_flights and updated_flights[0]["code"]:
        st.session_state.transport_id = updated_flights[0]["code"]
        st.session_state.flight_info = f"Ricerca info per: {updated_flights[0]['code']}"
    else:
        st.session_state.transport_id = ""
        st.session_state.flight_info = ""

    if "Nazione" in trip_type:
        if "cached_hubs" not in st.session_state:
            st.session_state.cached_hubs = []
        if "last_searched_country" not in st.session_state:
            st.session_state.last_searched_country = ""

        if location and location.strip().lower() != st.session_state.last_searched_country.strip().lower():
            cleaned_location = location.strip().lower()
            map_data = get_country_data(cleaned_location)
            if map_data:
                st.session_state.cached_hubs = map_data["default_hubs"]
                st.session_state.last_searched_country = cleaned_location
            else:
                with st.spinner(f"Generazione dinamica AI delle tappe principali per {location}..."):
                    st.session_state.cached_hubs = llm_svc.get_country_hubs(location)
                    st.session_state.last_searched_country = cleaned_location
        elif not location:
            st.session_state.cached_hubs = []
            st.session_state.last_searched_country = ""

        st.session_state.pre_selected_cities = st.multiselect(
            f"Quali città o regioni in {location if location else 'questa nazione'} vuoi toccare?",
            options=st.session_state.cached_hubs,
            default=[]
        )
        hotel_input = ""
    else:
        hotel_input = st.text_input("Hotel Prenotato", st.session_state.get("hotel_name", ""))
    
    if st.button("Avanti", use_container_width=True):
        if not location:
            st.error("Inserisci la destinazione principale per procedere!")
            return
        st.session_state.location = location
        st.session_state.hotel_name = hotel_input
        if "Nazione" in trip_type:
            st.session_state.hub_options = st.session_state.pre_selected_cities if st.session_state.pre_selected_cities else st.session_state.cached_hubs
            st.session_state.step = 2
            st.rerun()
        else:
            if not hotel_input:
                st.error("Inserisci l'hotel per ottimizzare i percorsi urbani!")
                return
            with st.spinner("Analisi destinazione..."):
                hotel_coords = places_svc.get_coordinates(hotel_input)
                if hotel_coords:
                    st.session_state.hotel_place = Place(id="hotel_hub_node", name=f"🏨 {hotel_input}", lat=hotel_coords[0], lon=hotel_coords[1], category="hotel", rating=5)
                coords = places_svc.get_coordinates(location)
                if coords:
                    st.session_state.attractions = places_svc.fetch_attractions(*coords)
                    st.session_state.step = 3
                    st.rerun()