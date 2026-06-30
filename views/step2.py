import streamlit as st
import re

def render_step2(places_svc, llm_svc, logger) -> None:
    st.header(f"1.5 Configurazione delle Tappe in {st.session_state.location}")
    
    selected_hubs = st.multiselect(
        "Verifica o modifica gli hub principali del viaggio itinerante:",
        options=list(set(st.session_state.hub_options + ["Aggiungi Località..."])),
        default=[h for h in st.session_state.hub_options if h != "Aggiungi Località..."]
    )
    
    st.markdown("### 🗓️ Ripartizione Giorni e Basi Operative (Hotel dedicati)")
    hotels_dict = {}
    days_dict = {}
    notes_dict = {} 
    
    for hub in selected_hubs:
        card = st.container(border=True)
        with card:
            st.subheader(f"📍 {hub}")
            col_days, col_hotel = st.columns([1, 2])
            with col_days:
                days_dict[hub] = st.number_input(f"Giorni di permanenza a {hub}", min_value=1, value=2, key=f"days_{hub}")
            with col_hotel:
                hotels_dict[hub] = st.text_input(f"Nome Hotel a {hub}", key=f"hotel_{hub}")
            notes_dict[hub] = st.text_area(f"Info extra, Voli o Tour per {hub} (es. Escursione guidata al Monte Bromo o Chichén Itzá)", key=f"notes_{hub}")
                
    if st.button("Genera e procedi alla selezione mirata dei Punti di Interesse", use_container_width=True):
        if not selected_hubs:
            st.error("Devi confermare almeno 1 tappa.")
            return
            
        st.session_state.multi_itinerary_config = {
            "hubs": selected_hubs, "hotels": hotels_dict, 
            "days": days_dict, "notes": notes_dict
        }
        
        with st.spinner("Analisi semantica nazionale ed estrazione delle attrazioni salienti..."):
            # Chiamata alla nuova logica che estrae i POI salienti dell'intera nazione in base agli hub (senza rumore)
            all_attractions_dict = places_svc.fetch_national_attractions_via_llm(
                country_or_region=st.session_state.location,
                hubs=selected_hubs,
                llm_svc=llm_svc
            )
            
            st.session_state.attractions = all_attractions_dict
            st.session_state.step = 2
            st.rerun()