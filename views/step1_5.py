import streamlit as st
import re

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
    notes_dict = {} # <-- NUOVO: Raccoglie note custom (Bug 5)
    
    for hub in selected_hubs:
        card = st.container(border=True)
        with card:
            st.subheader(f"📍 {hub}")
            col_days, col_hotel = st.columns([1, 2])
            with col_days:
                days_dict[hub] = st.number_input(f"Giorni di permanenza a {hub}", min_value=1, value=2, key=f"days_{hub}")
            with col_hotel:
                hotels_dict[hub] = st.text_input(f"Nome Hotel a {hub}", key=f"hotel_{hub}")
            # NUOVO: Area di testo per inserire direttive di viaggio (Bug 5)
            notes_dict[hub] = st.text_area(f"Info extra, Voli o Tour per {hub} (es. Trasferimento diretto a Bali)", key=f"notes_{hub}")
                
    if st.button("Genera e procedi alla selezione mirata dei Punti di Interesse", use_container_width=True):
        if not selected_hubs:
            st.error("Devi confermare almeno 1 tappa.")
            return
            
        st.session_state.multi_itinerary_config = {
            "hubs": selected_hubs, "hotels": hotels_dict, 
            "days": days_dict, "notes": notes_dict
        }
        
        with st.spinner("Estrazione e categorizzazione geospaziale di attrazioni..."):
            all_attractions_dict = {}
            for hub in selected_hubs:
                # FIX (Bug 1): Puliamo il nome per Nominatim (da "Ubud (Bali)" a "Ubud")
                clean_hub_name = re.sub(r'\(.*?\)', '', hub).strip()
                coords = places_svc.get_coordinates(clean_hub_name)
                
                hub_attractions = places_svc.fetch_attractions(*coords) if coords else []
                
                if not hub_attractions:
                    # FIX (Bug 1): Fallback semantico rimosso e sostituito con un warning pulito
                    logger.warning(f"Nessun dato locale trovato per '{clean_hub_name}'. Fallback disabilitato.")
                    st.warning(f"Nessuna attrazione trovata in automatico per {clean_hub_name}.")
                    
                all_attractions_dict[hub] = hub_attractions
            
            st.session_state.attractions = all_attractions_dict
            st.session_state.step = 2
            st.rerun()