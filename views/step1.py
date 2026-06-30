import streamlit as st
from datetime import datetime, timedelta
from core.models import Place
from core.config_map import get_country_data

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
    
    # Salviamo la data di partenza in session_state sotto forma di stringa per usarla nei check-in dello Step 4
    st.session_state["start_date"] = start_date.strftime("%Y/%m/%d")
    
    st.markdown("### Dettagli Logistici Avanzati (Opzionali)")
    st.session_state.flight_info = st.text_input(
        "Specifiche Voli / Orari (es: Arrivo a Yogyakarta il 12/08 ore 10:00, volo di ritorno da Bali il 25/08)",
        value=st.session_state.flight_info
    )
    
    # GESTIONE DETERMINISTICA VIA CONFIG_MAP ED EVITAMENTO DEL CARICAMENTO INFINITO
    if "Nazione" in trip_type:
        if "cached_hubs" not in st.session_state:
            st.session_state.cached_hubs = []
        if "last_searched_country" not in st.session_state:
            st.session_state.last_searched_country = ""

        # L'estrazione viene eseguita solo se l'utente cambia effettivamente il nome della nazione
        if location and location.strip().lower() != st.session_state.last_searched_country.strip().lower():
            cleaned_location = location.strip().lower()
            
            # 1. CONTROLLO CONFIGMAP DI DIRETTO RIFERIMENTO (Istantaneo)
            map_data = get_country_data(cleaned_location)
            
            if map_data:
                st.session_state.cached_hubs = map_data["default_hubs"]
                st.session_state.last_searched_country = cleaned_location
            else:
                # 2. FALLBACK SEMANTICO LOCAL LLM (Solo se la nazione è sconosciuta nel file .py)
                with st.spinner(f"Generazione dinamica AI delle tappe principali per {location}..."):
                    st.session_state.cached_hubs = llm_svc.get_country_hubs(location)
                    st.session_state.last_searched_country = cleaned_location
                    
        elif not location:
            st.session_state.cached_hubs = []
            st.session_state.last_searched_country = ""

        st.session_state.pre_selected_cities = st.multiselect(
            f"Quali città o regioni in {location if location else 'questa nazione'} hai già pianificato di toccare? (Lascia vuoto per farle suggerire tutte)",
            options=st.session_state.cached_hubs,
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
                st.session_state.hub_options = st.session_state.cached_hubs
            else:
                st.session_state.hub_options = st.session_state.pre_selected_cities
            
            # Se multi-tappa, passa allo Step 2 (Configurazione alloggi/giorni per ciascun hub)
            st.session_state.step = 2
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
                    # Se città singola, salta lo Step 2 e va direttamente allo Step 3 (Selezione attrazioni)
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error("Impossibile geolocalizzare la città inserita. Verifica il nome.")