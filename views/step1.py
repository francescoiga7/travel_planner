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
    
    # GESTIONE DINAMICA DELLE OPZIONI MULTI-SELECTION (NO HARDCODING)
    if "Nazione" in trip_type:
        # Se l'utente ha inserito una destinazione, interroghiamo dinamicamente l'LLM per avere le macro-tappe suggerite
        if location:
            with st.spinner(f"Generazione dinamica delle tappe principali per {location}..."):
                # Recupera la lista di hub suggeriti in tempo reale per quella specifica nazione
                suggested_options = llm_svc.get_country_hubs(location)
        else:
            suggested_options = []

        st.session_state.pre_selected_cities = st.multiselect(
            f"Quali città o regioni in {location if location else 'questa nazione'} hai già pianificato di toccare? (Lascia vuoto per farle suggerire tutte all'AI)",
            options=suggested_options,
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
            # Se l'utente ha selezionato manualmente delle tappe usiamo quelle, altrimenti usiamo l'intera lista dinamica generata
            if not st.session_state.pre_selected_cities:
                st.session_state.hub_options = suggested_options
            else:
                st.session_state.hub_options = st.session_state.pre_selected_cities
            
            st.session_state.step = 1.5
            st.rerun()
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