import streamlit as st
from datetime import datetime, timedelta
from core.config_map import get_country_data

def render_step2(places_svc, llm_svc, logger) -> None:
    st.header(f"2. Configurazione delle Tappe in {st.session_state.location}")
    
    selected_hubs = st.multiselect(
        "Verifica o modifica gli hub principali del viaggio itinerante:",
        options=list(set(st.session_state.hub_options + ["Aggiungi Località..."])),
        default=[h for h in st.session_state.hub_options if h != "Aggiungi Località..."]
    )
    
    st.markdown("### 🗓️ Pianificazione Date Alloggi (Check-in / Check-out) e Basi Operative")
    hotels_dict = {}
    days_dict = {}
    notes_dict = {} 
    
    if "selected_escursioni" not in st.session_state:
        st.session_state.selected_escursioni = {}
    else:
        st.session_state.selected_escursioni = {}

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
                duration_days = st.number_input(
                    f"Notti di permanenza a {hub}", 
                    min_value=1, 
                    value=2, 
                    key=f"days_{hub}"
                )
                days_dict[hub] = duration_days
                
                check_in_date = current_date_pointer
                check_out_date = current_date_pointer + timedelta(days=duration_days)
                
                st.caption(f"📅 **Check-in:** {check_in_date.strftime('%d/%m/%Y')} | **Check-out:** {check_out_date.strftime('%d/%m/%Y')}")
            
            with col_hotel:
                hotels_dict[hub] = st.text_input(f"Nome Hotel o Alloggio a {hub}", key=f"hotel_{hub}")
            
            # --- SEZIONE ATTIVITÀ E SELEZIONE DEL GIORNO / PUNTO DI INCONTRO ---
            hub_suggestions = [t for t in predefined_tours if t.get("hub", "").lower() == hub.lower()]
            
            if hub_suggestions:
                st.markdown("#### 🎫 Seleziona le Escursioni e personalizza la logica:")
                
                # FIX ERRORE STRFTIME: Generiamo correttamente le opzioni stringa
                date_opzioni = []
                date_opzioni_dict = {}
                for d in range(duration_days):
                    dt_possibile = check_in_date + timedelta(days=d)
                    # Formattiamo prima la data e poi concateniamo il numero del giorno in modo sicuro
                    S_str = f"{dt_possibile.strftime('%d/%m/%Y')} (Giorno {d + 1})"
                    date_opzioni.append(S_str)
                    date_opzioni_dict[S_str] = dt_possibile.strftime("%Y-%m-%d")

                for idx, tour in enumerate(hub_suggestions):
                    col_check, col_select, col_meeting = st.columns([2, 1, 1])
                    with col_check:
                        is_chosen = st.checkbox(
                            f"✨ {tour['desc']} ({tour['durata']} min)", 
                            key=f"chk_{hub}_{idx}"
                        )
                    
                    giorno_scelto_str = None
                    meeting_point_final = "Hotel"
                    
                    if is_chosen:
                        with col_select:
                            giorno_scelto_str = st.selectbox(
                                "Seleziona data",
                                options=date_opzioni,
                                key=f"date_sel_{hub}_{idx}",
                                label_visibility="collapsed"
                            )
                        with col_meeting:
                            meeting_type = st.selectbox(
                                "Punto di incontro",
                                options=["Hotel / Alloggio", "Altro posto..."],
                                key=f"meet_type_{hub}_{idx}",
                                label_visibility="collapsed"
                            )
                            if meeting_type == "Altro posto...":
                                meeting_point_final = st.text_input(
                                    "Specifiche Meeting Point", 
                                    placeholder="Es: Ingresso Porto, Marina...",
                                    key=f"meet_text_{hub}_{idx}"
                                )
                                if not meeting_point_final.strip():
                                    meeting_point_final = "Punto d'incontro esterno specificato"
                            else:
                                meeting_point_final = "Hotel"

                        # Salvataggio dati strutturati comprensivi del meeting point
                        data_iso_key = date_opzioni_dict[giorno_scelto_str]
                        st.session_state.selected_escursioni[data_iso_key] = {
                            "hub": hub,
                            "desc": tour['desc'],
                            "durata": tour['durata'],
                            "meeting_point": meeting_point_final
                        }
            else:
                st.markdown("_💡 Nessun tour predefinito nella ConfigMap per questa località._")
            
            st.markdown("")
            notes_dict[hub] = st.text_area(
                f"Note aggiuntive libere per {hub} (es. voli interni, preferenze cibo)", 
                key=f"notes_{hub}"
            )
            
            current_date_pointer = check_out_date
                
    if st.button("Genera e procedi alla selezione mirata dei Punti di Interesse", use_container_width=True):
        if not selected_hubs or (len(selected_hubs) == 1 and "Aggiungi Località..." in selected_hubs):
            st.error("Devi confermare almeno 1 tappa valida.")
            return
            
        st.session_state.multi_itinerary_config = {
            "hubs": [h for h in selected_hubs if h != "Aggiungi Località..."], 
            "hotels": hotels_dict, 
            "days": days_dict, 
            "notes": notes_dict,
            "escursioni_predefinite": st.session_state.selected_escursioni
        }
        
        with st.spinner("Estrazione geospaziale delle attrazioni salienti..."):
            all_attractions_dict = places_svc.fetch_national_attractions_via_llm(
                country_or_region=st.session_state.location,
                hubs=st.session_state.multi_itinerary_config["hubs"],
                llm_svc=llm_svc
            )
            
            st.session_state.attractions = all_attractions_dict
            st.session_state.step = 3
            st.rerun()