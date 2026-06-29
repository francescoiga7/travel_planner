import streamlit as st

def render_step1_5(places_svc, llm_svc, logger) -> None:
    st.header(f"1.5 Configurazione delle Tappe in {st.session_state.location}")
    
    selected_hubs = st.multiselect(
        "Verifica o modifica gli hub principali del viaggio itinerante:",
        options=list(set(st.session_state.hub_options + ["Aggiungi Località..."])),
        default=[h for h in st.session_state.hub_options if h != "Aggiungi Località..."]
    )
    
    st.markdown("### 🗓️ Ripartizione Giorni e Basi Operative (Hotel dedicati)")
    hotels_dict = {}
    days_dict = {}
    
    for hub in selected_hubs:
        card = st.container(border=True)
        with card:
            st.subheader(f"📍 {hub}")
            col_days, col_hotel = st.columns([1, 2])
            with col_days:
                days_dict[hub] = st.number_input(f"Giorni di permanenza a {hub}", min_value=1, value=2, key=f"days_{hub}")
            with col_hotel:
                hotels_dict[hub] = st.text_input(f"Nome Hotel / Alloggio a {hub} (Consigliato per percorsi ad anello)", key=f"hotel_{hub}")
                
    if st.button("Genera e procedi alla selezione mirata dei Punti di Interesse", use_container_width=True):
        if not selected_hubs:
            st.error("Devi confermare almeno 1 tappa/hub per costruire l'itinerario multi-tappa.")
            return
            
        st.session_state.multi_itinerary_config = {
            "hubs": selected_hubs,
            "hotels": hotels_dict,
            "days": days_dict
        }
        
        with st.spinner("Estrazione e categorizzazione geospaziale di attrazioni e monumenti per ciascuna città..."):
            all_attractions_dict = {}
            for hub in selected_hubs:
                coords = places_svc.get_coordinates(hub)
                hub_attractions = []
                if coords:
                    hub_attractions = places_svc.fetch_attractions(*coords)
                
                if not hub_attractions:
                    logger.info(f"Nessun dato locale trovato via Overpass per '{hub}'. Attivazione del fallback semantico LLM urbano.")
                    hub_attractions = llm_svc.fetch_city_monuments_fallback(hub)
                    
                all_attractions_dict[hub] = hub_attractions
            
            st.session_state.attractions = all_attractions_dict
            st.session_state.step = 2
            st.rerun()