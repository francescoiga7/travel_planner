import streamlit as st
import pandas as pd
from core.models import Place, RouteSegment, ItineraryDay

def render_step3(places_svc, routing_svc) -> None:
    st.header(f"3. Il tuo Programma di Viaggio Ottimizzato")
    
    if not st.session_state.itinerary:
        with st.spinner("Risoluzione delle matrici di instradamento e bilanciamento orari..."):
            places = st.session_state.selected_places
            
            if st.session_state.multi_itinerary_config:
                config = st.session_state.multi_itinerary_config
                hubs = config.get("hubs", [])
                hotels = config.get("hotels", {})
                days_alloc = config.get("days", {})
                
                final_itinerary = []
                current_day_global = 1
                
                for hub in hubs:
                    hub_days = int(days_alloc.get(hub, 1))
                    hub_origin_ids = {p.id for p in st.session_state.attractions.get(hub, [])}
                    hub_places = [p for p in places if p.id in hub_origin_ids]
                    
                    hub_hotel_name = hotels.get(hub, "")
                    hub_hotel_place = None
                    if hub_hotel_name:
                        hub_hotel_coords = places_svc.get_coordinates(hub_hotel_name)
                        if hub_hotel_coords:
                            hub_hotel_place = Place(
                                id=f"hotel_node_{hub}",
                                name=f"🏨 {hub_hotel_name}",
                                lat=hub_hotel_coords[0],
                                lon=hub_hotel_coords[1],
                                category="hotel",
                                rating=5
                            )
                    
                    if not hub_places:
                        for _ in range(hub_days):
                            final_itinerary.append(ItineraryDay(
                                day_number=current_day_global,
                                places_visited=[hub_hotel_place] if hub_hotel_place else [],
                                segments=[]
                            ))
                            current_day_global += 1
                        continue
                    
                    actual_clusters_days = min(hub_days, len(hub_places))
                    hub_clusters = routing_svc.cluster_pois_by_day(hub_places, actual_clusters_days)
                    
                    hub_places_dict = {p.id: p for p in hub_places}
                    if hub_hotel_place:
                        hub_places_dict[hub_hotel_place.id] = hub_hotel_place
                    
                    raw_hub_itinerary = routing_svc.build_deterministic_itinerary(
                        hub_clusters, hub_places_dict, hotel_place=hub_hotel_place,
                        flight_info_str=st.session_state.flight_info
                    )
                    
                    for day_data in raw_hub_itinerary:
                        validated_segments = [RouteSegment(**seg) for seg in day_data["segments"]]
                        final_itinerary.append(ItineraryDay(
                            day_number=current_day_global,
                            places_visited=day_data["places_visited"],
                            segments=validated_segments
                        ))
                        current_day_global += 1
                    
                    if hub_days > actual_clusters_days:
                        for _ in range(hub_days - actual_clusters_days):
                            final_itinerary.append(ItineraryDay(
                                day_number=current_day_global,
                                places_visited=[hub_hotel_place] if hub_hotel_place else [],
                                segments=[]
                            ))
                            current_day_global += 1
                
                st.session_state.itinerary = final_itinerary
                st.session_state.reasoning_logs = ["Sincronizzazione TSP multi-hub conclusa."]
            
            else:
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
                    final_itinerary.append(ItineraryDay(
                        day_number=day["day_number"],
                        places_visited=day["places_visited"],
                        segments=segments
                    ))
                st.session_state.itinerary = final_itinerary
                st.session_state.reasoning_logs = ["Ottimizzazione ad anello chiuso completata."]

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
                    
                    with col_time:
                        if idx == 0:
                            start_time = day.segments[0].departure_time if len(day.segments) > 0 else "09:00"
                            st.markdown(f"### ⏰ {start_time}")
                            st.caption("🚀 _Inizio giornata_")
                        elif idx == len(day.places_visited) - 1 and "hotel" in place.id:
                            end_time = day.segments[-1].arrival_time if len(day.segments) > 0 else "Fine"
                            st.markdown(f"### ⏰ {end_time}")
                            st.caption("🌙 _Rientro in Hotel_")
                        else:
                            arrival = day.segments[idx-1].arrival_time if idx-1 < len(day.segments) else "--:--"
                            departure = day.segments[idx].departure_time if idx < len(day.segments) else "--:--"
                            st.markdown(f"### ⏰ {arrival} - {departure}")
                            st.caption("⏱️ _Intervallo Visita_")
                    
                    with col_content:
                        if "hotel" in place.id or place.category.lower() == "hotel":
                            st.markdown(f"### 🏠 {place.name}")
                        else:
                            st.markdown(f"### 📍 {place.name}")
                            st.caption(f"Categoria: {place.category.upper()} | Rilevanza: {'⭐' * place.rating}")
                        
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