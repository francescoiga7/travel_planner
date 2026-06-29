import streamlit as st
from datetime import datetime, timedelta
from core.models import Place

def render_step1(places_svc, llm_svc) -> None:
    st.header("1. Scegli la destinazione e i dettagli del soggiorno")
    
    trip_type = st.radio("Tipo di destinazione", ["Città Singola (es: Roma)", "Nazione / Multi-tappa (es: Indonesia)"])
    location = st.text_input("Inserisci la destinazione", st.session_state.location)
    
    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input("Data di Partenza", datetime.today())
    with col_end:
        end_date = st.date_input("Data di Ritorno", datetime.today() + timedelta(days=3))
        
    st.session_state.num_days = (end_date - start_date).days + 1
    
    st.markdown("### Dettagli Logistici Avanzati (Opzionali)")
    st.session_state.flight_info = st.text_input(
        "Specifiche Voli / Orari (es: Arrivo a Yogyakarta il 12/08 ore 10:00, volo di ritorno da Bali il 25/08)",
        value=st.session_state.flight_info
    )
    
    if "Nazione" in trip_type:
        st.session_state.pre_selected_cities = st.multiselect(
            "Quali città o regioni hai già pianificato di toccare? (Lascia vuoto per farle suggerire all'AI)",
            options=["Jakarta", "Yogyakarta", "Ubud (Bali)", "Lombok", "Isole Komodo", "Città del Messico", "Cancún", "Oaxaca", "Merida", "Tulum"],
            default=[]
        )
        hotel_input = ""
    else:
        hotel_input = st.text_input("Hotel Prenotato (es: Hotel Artemide Roma, o un indirizzo specifico)", st.session_state.hotel_name)
    
    if st.button("Avanti", use_container_width=True):
        if not location:
            st.error("Inserisci la destinazione principale per procedere!")
            return
            
        st.session_state.location = location
        st.session_state.hotel_name = hotel_input
        
        if "Nazione" in trip_type:
            if not st.session_state.pre_selected_cities:
                with st.spinner(f"Ricerca dei principali hub turistici in {location}..."):
                    st.session_state.hub_options = llm_svc.get_country_hubs(location)
            else:
                st.session_state.hub_options = st.session_state.pre_selected_cities
            
            st.session_state.step = 1.5
            st.author_rerun = st.rerun()
        else:
            if not hotel_input:
                st.error("Inserisci l'hotel per ottimizzare i percorsi urbani ad anello!")
                return
            
            with st.spinner("Geolocalizzazione dell'Hotel e analisi destinazione..."):
                hotel_coords = places_svc.get_coordinates(hotel_input)
                if hotel_coords:
                    st.session_state.hotel_place = Place(
                        id="hotel_hub_node",
                        name=f"🏨 {hotel_input}",
                        lat=hotel_coords[0],
                        lon=hotel_coords[1],
                        category="hotel",
                        rating=5
                    )
                else:
                    st.warning("Impossibile trovare la posizione esatta dell'hotel. Verrà usato il centro città come base geometrica.")
            
            with st.spinner("Scaricamento attrazioni locali e calcolo indici di fama..."):
                coords = places_svc.get_coordinates(location)
                if coords:
                    st.session_state.attractions = places_svc.fetch_attractions(*coords)
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Impossibile geolocalizzare la città inserita. Verifica il nome.")