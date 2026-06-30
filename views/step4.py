import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from core.models import Place, RouteSegment, ItineraryDay
from core.config_map import get_country_data

def render_step4(places_svc, routing_svc) -> None:
    st.header(f"4. Il tuo Programma di Viaggio Ottimizzato")
    
    if not st.session_state.itinerary:
        with st.spinner("Risoluzione delle matrici di instradamento inter-city e bilanciamento orari..."):
            places = st.session_state.selected_places
            
            if st.session_state.multi_itinerary_config:
                config = st.session_state.multi_itinerary_config
                hubs = config.get("hubs", [])
                hotels = config.get("hotels", {})
                days_alloc = config.get("days", {})
                special_activities = config.get("escursioni_predefinite", {})
                
                # Recuperiamo le coordinate fisse della ConfigMap per i fallback di sicurezza
                map_data = get_country_data(st.session_state.location)
                map_coords = map_data.get("coordinates", {}) if map_data else {}
                
                final_itinerary = []
                current_day_global = 1
                
                # Teniamo traccia dell'hotel precedente per creare il ponte logistico corretto
                active_hotel_place = None
                
                start_date_val = st.session_state.get("start_date")
                if isinstance(start_date_val, (datetime, timedelta)):
                    base_date = start_date_val
                elif isinstance(start_date_val, str):
                    try:
                        base_date = datetime.strptime(start_date_val.replace("-", "/"), "%Y/%m/%d")
                    except Exception:
                        base_date = datetime.today()
                else:
                    base_date = datetime.today()
                
                for idx, hub in enumerate(hubs):
                    hub_days = int(days_alloc.get(hub, 1))
                    hub_origin_ids = {p.id for p in st.session_state.attractions.get(hub, [])}
                    hub_places = [p for p in places if p.id in hub_origin_ids]
                    
                    # Calcolo date Check-in / Check-out basate sulla timeline globale
                    check_in_date = base_date + timedelta(days=current_day_global - 1)
                    check_out_date = check_in_date + timedelta(days=hub_days)
                    
                    check_in_str = check_in_date.strftime("%d/%m/%Y")
                    check_out_str = check_out_date.strftime("%d/%m/%Y")
                    
                    hub_hotel_name = hotels.get(hub, "")
                    hub_hotel_place = None
                    
                    # Proviamo a geolocalizzare l'hotel inserito dall'utente
                    if hub_hotel_name:
                        hub_hotel_coords = places_svc.get_coordinates(f"{hub_hotel_name}, {hub}")
                        if hub_hotel_coords:
                            hub_hotel_place = Place(
                                id=f"hotel_node_{hub}", 
                                name=f"🏨 {hub_hotel_name} ({hub}) - [Check-in: {check_in_str} ➔ Check-out: {check_out_str}]",
                                lat=hub_hotel_coords[0], 
                                lon=hub_hotel_coords[1],
                                category="hotel", 
                                rating=1
                            )
                    
                    # FIX LOCK SICUREZZA: Se l'hotel fallisce o è vuoto, usiamo il centro geografico dell'hub dalla ConfigMap
                    if not hub_hotel_place and hub in map_coords:
                        fallback_coords = map_coords[hub]
                        hub_hotel_place = Place(
                            id=f"hotel_node_{hub}_fallback", 
                            name=f"🏨 Alloggio base a {hub} (Centro) - [Check-in: {check_in_str} ➔ Check-out: {check_out_str}]",
                            lat=fallback_coords[0], 
                            lon=fallback_coords[1],
                            category="hotel", 
                            rating=1
                        )

                    # Configurazione nodi speciali tecnici (Aeroporto solo al primissimo giorno)
                    arrival_start_node = None
                    if idx == 0 and st.session_state.flight_info:
                        arrival_start_node = Place(
                            id=f"airport_{hub}", name=f"🛬 Aeroporto / Arrivo a {hub}",
                            lat=hub_hotel_place.lat if hub_hotel_place else 0,
                            lon=hub_hotel_place.lon if hub_hotel_place else 0,
                            category="airport", rating=1, visit_duration_minutes=30
                        )
                    elif active_hotel_place:
                        # Se cambiamo città, partiamo esplicitamente dall'hotel in cui abbiamo dormito la notte precedente
                        arrival_start_node = active_hotel_place

                    if not hub_places and not hub_hotel_place:
                        continue
                    
                    # Generazione cluster giornalieri per le attrazioni interne all'hub
                    actual_clusters_days = min(hub_days, max(1, len(hub_places)))
                    hub_clusters = routing_svc.cluster_pois_by_day(hub_places, actual_clusters_days)
                    
                    hub_places_dict = {p.id: p for p in hub_places}
                    if hub_hotel_place:
                        hub_places_dict[hub_hotel_place.id] = hub_hotel_place
                    if active_hotel_place:
                        hub_places_dict[active_hotel_place.id] = active_hotel_place
                    
                    hub_notes = config.get("notes", {}).get(hub, "")
                    current_flight_info = st.session_state.flight_info if idx == 0 else ""

                    # Generazione itinerario per i giorni di permanenza in questo hub
                    raw_hub_itinerary = routing_svc.build_deterministic_itinerary(
                        hub_clusters, hub_places_dict, hotel_place=hub_hotel_place,
                        flight_info_str=current_flight_info, 
                        start_node=arrival_start_node,
                        user_notes=hub_notes
                    )
                    
                    # AGGIORNAMENTO LOGICA DEI TRASFERIMENTI TRA HOTEL (Anello Continuo)
                    for day_idx, day_data in enumerate(raw_hub_itinerary):
                        validated_segments = []
                        day_date = base_date + timedelta(days=current_day_global - 1)
                        day_date_iso = day_date.strftime("%Y-%m-%d")

                        # INTERCETTAZIONE ESCURSIONI PREDEFINITE SELEZIONATE INTERATTIVAMENTE
                        if day_date_iso in special_activities and special_activities[day_date_iso]["hub"] == hub:
                            activity_info = special_activities[day_date_iso]
                            m_point = activity_info.get("meeting_point", "Hotel")

                            special_place = Place(
                                id=f"map_act_{current_day_global}",
                                name=f"🌟 {activity_info['desc']}",
                                lat=hub_hotel_place.lat if hub_hotel_place else 0.0,
                                lon=hub_hotel_place.lon if hub_hotel_place else 0.0,
                                category="event", rating=5,
                                visit_duration_minutes=activity_info.get("durata", 360)
                            )

                            places_as_dicts = [hub_hotel_place.model_dump(), special_place.model_dump(), hub_hotel_place.model_dump()] if hub_hotel_place else [special_place.model_dump()]

                            if m_point == "Hotel":
                                meet_desc = f"Partenza direttamente dalla hall del tuo alloggio: {hub_hotel_name if hub_hotel_name else 'Hotel'}."
                            else:
                                meet_desc = f"Uscita e spostamento autonomo verso il Punto di Incontro: 📍 {m_point}."

                            seg_out = RouteSegment(
                                from_place=hub_hotel_place.name if hub_hotel_place else "Hotel",
                                to_place=special_place.name,
                                distance_meters=0.0, duration_minutes=30, transport_mode="🚗 Spostamento Tour",
                                departure_time="08:30", arrival_time="09:00",
                                additional_info=f"Inizio attività programmata. {meet_desc}"
                            )

                            seg_in = RouteSegment(
                                from_place=special_place.name,
                                to_place=hub_hotel_place.name if hub_hotel_place else "Hotel",
                                distance_meters=0.0, duration_minutes=45, transport_mode="🚗 Rientro",
                                departure_time="17:00", arrival_time="17:45",
                                additional_info="Fine del tour e rientro alla base operativa."
                            )

                            # Modifica del segmento finale per il cambio città/hotel se ultimo giorno dell'hub
                            if day_idx == len(raw_hub_itinerary) - 1 and idx < len(hubs) - 1:
                                next_hub = hubs[idx + 1]
                                next_hotel_name = hotels.get(next_hub, "")
                                next_hotel_coords = places_svc.get_coordinates(f"{next_hotel_name}, {next_hub}")
                                if not next_hotel_coords and next_hub in map_coords:
                                    next_hotel_coords = map_coords[next_hub]
                                    
                                if next_hotel_coords and hub_hotel_place:
                                    dist_m, duration_min, info, mode = routing_svc.get_real_transit_route(
                                        hub_hotel_place.lat, hub_hotel_place.lon,
                                        next_hotel_coords[0], next_hotel_coords[1]
                                    )
                                    seg_in = RouteSegment(
                                        from_place=special_place.name,
                                        to_place=f"🏠 Spostamento e Check-in a {next_hub}: {next_hotel_name if next_hotel_name else 'Alloggio'}",
                                        distance_meters=dist_m, duration_minutes=duration_min, transport_mode=mode,
                                        departure_time="16:30", arrival_time=f"{16 + int(duration_min)//60:02d}:{(30 + int(duration_min)%60)%60:02d}",
                                        additional_info=f"Spostamento inter-city serale. {info}"
                                    )

                            final_itinerary.append(ItineraryDay(
                                day_number=current_day_global,
                                places_visited=places_as_dicts,
                                segments=[seg_out, seg_in]
                            ))
                            current_day_global += 1
                            continue
                        
                        # Se è l'ultimo giorno di questo hub ed esiste un hub successivo (Logica Standard POI),
                        # forziamo l'ultimo segmento a connettersi al PROSSIMO hotel, non a quello corrente.
                        if day_idx == len(raw_hub_itinerary) - 1 and idx < len(hubs) - 1:
                            next_hub = hubs[idx + 1]
                            next_hotel_name = hotels.get(next_hub, "")
                            next_hotel_coords = places_svc.get_coordinates(f"{next_hotel_name}, {next_hub}")
                            if not next_hotel_coords and next_hub in map_coords:
                                next_hotel_coords = map_coords[next_hub]
                            
                            if next_hotel_coords and day_data["places_visited"]:
                                last_visited_place = day_data["places_visited"][-1]
                                
                                # Ricalcoliamo il segmento finale verso la nuova città
                                dist_m, duration_min, info, mode = routing_svc.get_real_transit_route(
                                    last_visited_place.lat, last_visited_place.lon,
                                    next_hotel_coords[0], next_hotel_coords[1]
                                )
                                
                                # Modifichiamo l'ultimo segmento della lista per reindirizzarlo
                                if day_data["segments"]:
                                    orig_seg = day_data["segments"][-1]
                                    dep_time = orig_seg["departure_time"]
                                    
                                    # Calcolo orario arrivo nel nuovo hotel
                                    try:
                                        h_dep, m_dep = map(int, dep_time.split(":"))
                                        m_arr = (m_dep + int(duration_min))
                                        h_arr = (h_dep + m_arr // 60) % 24
                                        m_arr %= 60
                                        arr_time_str = f"{h_arr:02d}:{m_arr:02d}"
                                    except Exception:
                                        arr_time_str = "Sera"

                                    day_data["segments"][-1] = {
                                        "from_place": last_visited_place.name,
                                        "to_place": f"🏠 Check-out da {hub} ➔ Spostamento e Check-in a {next_hub}: {next_hotel_name if next_hotel_name else 'Alloggio'}",
                                        "distance_meters": dist_m,
                                        "duration_minutes": duration_min,
                                        "transport_mode": mode,
                                        "departure_time": dep_time,
                                        "arrival_time": arr_time_str,
                                        "additional_info": f"🌙 Fine giornata con trasferimento inter-city. {info}"
                                    }
                        
                        # Validazione segmenti finali standard
                        for seg in day_data["segments"]:
                            validated_segments.append(RouteSegment(**seg))
                            
                        places_as_dicts = [p.model_dump() if hasattr(p, 'model_dump') else p for p in day_data["places_visited"]]
                        
                        final_itinerary.append(ItineraryDay(
                            day_number=current_day_global,
                            places_visited=places_as_dicts,
                            segments=validated_segments
                        ))
                        current_day_global += 1
                    
                    # Impostiamo l'hotel corrente come "passato" per il prossimo ciclo
                    active_hotel_place = hub_hotel_place
                    
                    # Giorni cuscino di puro relax se l'utente alloca più tempo dei monumenti scelti
                    if hub_days > actual_clusters_days:
                        for _ in range(hub_days - actual_clusters_days):
                            final_itinerary.append(ItineraryDay(
                                day_number=current_day_global,
                                places_visited=[hub_hotel_place.model_dump()] if hub_hotel_place else [],
                                segments=[]
                            ))
                            current_day_global += 1
                
                st.session_state.itinerary = final_itinerary
                st.session_state.reasoning_logs = ["Logistica dei trasferimenti ad anello inter-hotel consolidata."]
            
            else:
                # Logica standard città singola
                num_days = st.session_state.num_days
                hotel = st.session_state.hotel_place
                
                daily_clusters = routing_svc.cluster_pois_by_day(places, num_days)
                places_dict = {p.id: p for p in places}
                if hotel:
                    places_dict[hotel.id] = hotel
                    
                raw_itinerary = routing_svc.build_deterministic_itinerary(
                    daily_clusters, places_dict, hotel_place=hotel
                )
                
                final_itinerary = []
                for day in raw_itinerary:
                    segments = [RouteSegment(**seg) for seg in day["segments"]]
                    places_as_dicts = [p.model_dump() if hasattr(p, 'model_dump') else p for p in day["places_visited"]]
                    final_itinerary.append(ItineraryDay(
                        day_number=day["day_number"],
                        places_visited=places_as_dicts,
                        segments=segments
                    ))
                st.session_state.itinerary = final_itinerary
                st.session_state.reasoning_logs = ["Ottimizzazione ad anello chiuso completata."]

    # INTERFACCIA GRAFICA STREAMLIT
    if st.session_state.reasoning_logs:
        with st.status("🧠 Log del Ragionamento Spaziale", expanded=False):
            for log in st.session_state.reasoning_logs:
                st.code(f"[ENGINE_LOG] {log}", language="bash")

    if st.session_state.itinerary is None:
        st.error("❌ Impossibile generare il piano di viaggio.")
    elif len(st.session_state.itinerary) == 0:
        st.warning("⚠️ L'itinerario calcolato risulta vuoto.")
    else:
        if st.session_state.flight_info:
            st.warning(f"✈️ **Vincoli di Volo impostati:** {st.session_state.flight_info}")
            
        st.write("### 📅 Programma Giornaliero Dettagliato")
        
        if st.session_state.multi_itinerary_config and "notes" in st.session_state.multi_itinerary_config:
            st.write("### 📝 Note, Tour ed Escursioni Pianificate")
            for h, n in st.session_state.multi_itinerary_config["notes"].items():
                if n.strip():
                    st.info(f"**{h}:** {n}")
                    
        final_map_df = pd.DataFrame([{
            "latitude": p.lat,
            "longitude": p.lon,
            "name": p.name
        } for p in st.session_state.selected_places])
        st.map(final_map_df, width='stretch')
        
        for day in st.session_state.itinerary:
            with st.expander(f"🗓️ GIORNO {day.day_number}", expanded=True):
                if not day.places_visited:
                    st.markdown("_Nessuna attività pianificata o giornata di trasferimento inter-city._")
                    continue
                
                for idx, place in enumerate(day.places_visited):
                    col_time, col_content = st.columns([1, 4])
                    
                    if isinstance(place, dict):
                        p_name = place.get('name', 'Sconosciuto')
                        p_cat = place.get('category', 'attraction').lower()
                        p_rating = place.get('rating', 1)
                        p_id = place.get('id', '')
                    else:
                        p_name = getattr(place, 'name', 'Sconosciuto')
                        p_cat = getattr(place, 'category', 'attraction').lower()
                        p_rating = getattr(place, 'rating', 1)
                        p_id = getattr(place, 'id', '')

                    with col_time:
                        if idx == 0:
                            start_time = day.segments[0].departure_time if len(day.segments) > 0 else "09:00"
                            st.markdown(f"### ⏰ {start_time}")
                            st.caption("🚀 _Inizio giornata_")
                        elif idx == len(day.places_visited) - 1 and ("hotel" in p_cat or "hotel" in p_id):
                            end_time = day.segments[-1].arrival_time if len(day.segments) > 0 else "Fine"
                            st.markdown(f"### ⏰ {end_time}")
                            st.caption("🌙 _Rientro in Hotel_")
                        else:
                            arrival = day.segments[idx-1].arrival_time if idx-1 < len(day.segments) else "--:--"
                            departure = day.segments[idx].departure_time if idx < len(day.segments) else "--:--"
                            st.markdown(f"### ⏰ {arrival} - {departure}")
                            st.caption("⏱️ _Intervallo Visita_")
                    
                    with col_content:
                        if "hotel" in p_cat or "hotel" in p_id:
                            st.markdown(f"### 🏠 {p_name}")
                        elif "event" in p_cat or "special" in p_id or "map_act" in p_id:
                            st.markdown(f"### 🌟 {p_name}")
                        elif "transfer" in p_cat:
                            st.markdown(f"### 🚀 {p_name}")
                        else:
                            st.markdown(f"### 📍 {p_name}")
                            st.caption(f"Categoria: {p_cat.upper()} | Rilevanza: {'⭐' * p_rating}")
                        
                        if idx < len(day.segments):
                            seg = day.segments[idx]
                            mode_lower = seg.transport_mode.lower()
                            
                            icon = "🚶"
                            if any(m in mode_lower for m in ["mezzi", "bus", "metro", "autobus", "transit"]):
                                icon = "🚇"
                            elif any(m in mode_lower for m in ["taxi", "auto", "treno", "volo", "aereo"]):
                                icon = "🚖" if "treno" not in mode_lower and "volo" not in mode_lower else "🚄"
                            
                            clean_info = seg.additional_info.split('|')[-1].strip() if '|' in seg.additional_info else seg.additional_info
                            st.info(
                                f"{icon} **Prossimo Spostamento verso {seg.to_place}** alle ore **{seg.departure_time}**\n\n"
                                f"Mezzo: {seg.transport_mode} | Distanza: {seg.distance_meters:.0f} m | Tempo: {seg.duration_minutes:.0f} min\n\n"
                                f"_{clean_info}_"
                            )
                    st.markdown("---")

    if st.button("🔄 Pianifica un nuovo viaggio", use_container_width=True):
        st.session_state.clear()
        st.rerun()