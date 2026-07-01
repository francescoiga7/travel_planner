import streamlit as st
from datetime import datetime, timedelta
from core.config_map import get_country_data

def render_step2(places_svc, llm_svc) -> None:
    st.header(f"2. Configurazione delle Tappe in {st.session_state.location}")
    
    selected_hubs = st.multiselect(
        "Verifica o modifica gli hub principali del viaggio itinerante:",
        options=list(set(st.session_state.hub_options + ["Aggiungi Località..."])),
        default=[h for h in st.session_state.hub_options if h != "Aggiungi Località..."]
    )
    
    st.markdown("### 🗓️ Pianificazione Date Alloggi, Basi Operative e Voli Interni")
    hotels_dict = {}
    days_dict = {}
    notes_dict = {} 
    
    if "selected_escursioni" not in st.session_state:
        st.session_state.selected_escursioni = {}
    if "internal_transports" not in st.session_state:
        st.session_state.internal_transports = {}

    map_data = get_country_data(st.session_state.location)
    predefined_tours = map_data.get("escursioni_predefinite", []) if map_data else []

    start_date_str = st.session_state.get("start_date", datetime.today().strftime("%Y/%m/%d"))
    try:
        current_date_pointer = datetime.strptime(start_date_str, "%Y/%m/%d")
    except Exception:
        current_date_pointer = datetime.today()

    for hub in selected_hubs:
        if hub == "Aggiungi Località...":
            continue
            
        card = st.container(border=True)
        with card:
            st.subheader(f"📍 {hub}")
            col_days, col_hotel = st.columns([1, 2])
            with col_days:
                duration_days = st.number_input(f"Notti di permanenza a {hub}", min_value=1, value=2, key=f"days_{hub}")
                days_dict[hub] = duration_days
                check_in_date = current_date_pointer
                check_out_date = current_date_pointer + timedelta(days=duration_days)
                st.caption(f"📅 **Check-in:** {check_in_date.strftime('%d/%m/%Y')} | **Check-out:** {check_out_date.strftime('%d/%m/%Y')}")
            
            with col_hotel:
                hotels_dict[hub] = st.text_input(f"Nome Hotel o Alloggio a {hub}", key=f"hotel_{hub}")
            
            st.markdown(f"✈️ **Collegamenti Interni associati a {hub}:**")
            t_code = st.text_input(f"Codice Volo Interno / Mezzo per {hub}", key=f"t_code_{hub}", placeholder="Es: Y4712 (Estrazione auto attive)")
            if t_code:
                st.session_state.internal_transports[hub] = {"code": t_code}
            
            hub_suggestions = [t for t in predefined_tours if t.get("hub", "").lower() == hub.lower()]
            if hub_suggestions:
                st.markdown("#### 🎫 Seleziona le Escursioni:")
                date_opzioni = [f"{(check_in_date + timedelta(days=d)).strftime('%d/%m/%Y')} (Giorno {d + 1})" for d in range(duration_days)]
                
                for idx, tour in enumerate(hub_suggestions):
                    col_check, col_select, col_meeting = st.columns([2, 1, 1])
                    with col_check:
                        is_chosen = st.checkbox(f"✨ {tour['desc']} ({tour['durata']} min)", key=f"chk_{hub}_{idx}")
                    if is_chosen:
                        with col_select:
                            giorno_scelto_str = st.selectbox("Data", options=date_opzioni, key=f"date_sel_{hub}_{idx}", label_visibility="collapsed")
                        with col_meeting:
                            meeting_type = st.selectbox("Incontro", options=["Hotel", "Altro..."], key=f"meet_type_{hub}_{idx}", label_visibility="collapsed")
                            meeting_point_final = st.text_input("Specifica", placeholder="Ingresso porto...", key=f"meet_text_{hub}_{idx}", label_visibility="collapsed") if meeting_type == "Altro..." else "Hotel"
                        
                        dt_str = giorno_scelto_str.split(" ")[0]
                        try:
                            iso_key = datetime.strptime(dt_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                            st.session_state.selected_escursioni[iso_key] = {"hub": hub, "desc": tour['desc'], "durata": tour['durata'], "meeting_point": meeting_point_final}
                        except Exception:
                            pass
            
            notes_dict[hub] = st.text_area(f"Note aggiuntive per {hub}", key=f"notes_{hub}")
            current_date_pointer = check_out_date
                
    if st.button("Genera e procedi alla selezione dei Punti di Interesse", use_container_width=True):
        st.session_state.multi_itinerary_config = {
            "hubs": [h for h in selected_hubs if h != "Aggiungi Località..."], "hotels": hotels_dict, "days": days_dict, "notes": notes_dict,
            "escursioni_predefinite": st.session_state.selected_escursioni, "internal_transports": st.session_state.internal_transports
        }
        with st.spinner("Caricamento attrazioni..."):
            st.session_state.attractions = places_svc.fetch_national_attractions_via_llm(st.session_state.location, st.session_state.multi_itinerary_config["hubs"])
            st.session_state.step = 3
            st.rerun()