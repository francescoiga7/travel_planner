import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
from core.models import Place, RouteSegment, ItineraryDay
from core.config_map import get_country_data

def render_step4(places_svc, routing_svc) -> None:
    st.header("4. Il tuo Programma di Viaggio Ottimizzato")
    
    if not st.session_state.itinerary:
        with st.spinner("Generazione dell'instradamento logistico e sequenza hotel..."):
            places = st.session_state.selected_places
            
            if st.session_state.multi_itinerary_config:
                config = st.session_state.multi_itinerary_config
                hubs = config.get("hubs", [])
                hotels = config.get("hotels", {})
                days_alloc = config.get("days", {})
                special_activities = config.get("escursioni_predefinite", {})
                internal_transports = config.get("internal_transports", {})
                
                map_data = get_country_data(st.session_state.location)
                map_coords = map_data.get("coordinates", {}) if map_data else {}
                
                final_itinerary = []
                current_day_global = 1
                active_hotel_place = None
                
                start_date_val = st.session_state.get("start_date")
                try:
                    base_date = datetime.strptime(start_date_val.replace("-", "/"), "%Y/%m/%d")
                except Exception:
                    base_date = datetime.today()
                
                flat_days_raw = []
                
                for idx, hub in enumerate(hubs):
                    hub_days = int(days_alloc.get(hub, 1))
                    hub_origin_ids = {p.id for p in st.session_state.attractions.get(hub, [])}
                    hub_places = [p for p in places if p.id in hub_origin_ids]
                    
                    hub_hotel_name = hotels.get(hub, "")
                    hub_hotel_place = None
                    if hub_hotel_name:
                        hub_hotel_coords = places_svc.get_coordinates(f"{hub_hotel_name}, {hub}")
                        if hub_hotel_coords:
                            hub_hotel_place = Place(id=f"hotel_node_{hub}", name=f"🏨 Alloggio a {hub_hotel_name}", lat=hub_hotel_coords[0], lon=hub_hotel_coords[1], category="hotel", rating=1)
                    if not hub_hotel_place and hub in map_coords:
                        fallback_coords = map_coords[hub]
                        hub_hotel_place = Place(id=f"hotel_node_{hub}_fallback", name=f"🏨 Alloggio base a {hub}", lat=fallback_coords[0], lon=fallback_coords[1], category="hotel", rating=1)

                    arrival_start_node = None
                    current_flight_info = ""
                    
                    if idx == 0 and st.session_state.get("main_flights"):
                        flight_names = []
                        # Trova l'ultimo volo inserito per determinare l'orario esatto di arrivo a destinazione (AM504 -> 10:30)
                        last_flight = [f for f in st.session_state.main_flights if f.get("code")][-1]
                        current_flight_info = f"Ricerca info per: {last_flight['code']}"
                        
                        for f in st.session_state.main_flights:
                            if f.get("code"):
                                f_auto = routing_svc.scrape_flight_route_auto(f["code"])
                                flight_names.append(f"Volo {f_auto['code']} ({f_auto['from']} ➔ {f_auto['to']})")
                        
                        full_flight_desc = " | ".join(flight_names)
                        arrival_start_node = Place(id=f"airport_{hub}", name=f"🛬 Arrivo: {full_flight_desc}", lat=hub_hotel_place.lat, lon=hub_hotel_place.lon, category="airport", rating=1, visit_duration_minutes=30)
                    elif active_hotel_place:
                        arrival_start_node = active_hotel_place

                    actual_clusters_days = min(hub_days, max(1, len(hub_places)))
                    hub_clusters = routing_svc.cluster_pois_by_day(hub_places, actual_clusters_days)
                    hub_places_dict = {p.id: p for p in hub_places}
                    if hub_hotel_place: hub_places_dict[hub_hotel_place.id] = hub_hotel_place
                    if active_hotel_place: hub_places_dict[active_hotel_place.id] = active_hotel_place
                    
                    raw_hub_itinerary = routing_svc.build_deterministic_itinerary(
                        hub_clusters, hub_places_dict, hotel_place=hub_hotel_place, 
                        flight_info_str=current_flight_info, start_node=arrival_start_node
                    )
                    
                    for d_data in raw_hub_itinerary:
                        d_data["meta_hub"] = hub
                        d_data["meta_hotel"] = hub_hotel_place
                        flat_days_raw.append(d_data)
                        
                    # Se i giorni effettivi con attrazioni sono meno delle notti prenotate, riempiamo i vuoti per l'alloggio
                    if hub_days > len(raw_hub_itinerary):
                        for _ in range(hub_days - len(raw_hub_itinerary)):
                            flat_days_raw.append({
                                "day_number": len(flat_days_raw) + 1,
                                "places_visited": [hub_hotel_place],
                                "segments": [],
                                "meta_hub": hub,
                                "meta_hotel": hub_hotel_place
                            })
                            
                    active_hotel_place = hub_hotel_place

                # CORREZIONE SPOSTAMENTI INTER-HUB SERALI (EVITA SVEGLIE MAGICHE)
                for g_idx, day_data in enumerate(flat_days_raw):
                    validated_segments = []
                    day_date_iso = (base_date + timedelta(days=current_day_global - 1)).strftime("%Y-%m-%d")
                    current_hub = day_data["meta_hub"]
                    current_hotel = day_data["meta_hotel"]

                    if day_date_iso in special_activities and special_activities[day_date_iso]["hub"] == current_hub:
                        act = special_activities[day_date_iso]
                        special_place = Place(id=f"map_act_{current_day_global}", name=f"🌟 {act['desc']} (Incontro: {act['meeting_point']})", lat=current_hotel.lat, lon=current_hotel.lon, category="event", rating=5, visit_duration_minutes=act['durata'])
                        places_as_dicts = [current_hotel.model_dump(), special_place.model_dump(), current_hotel.model_dump()]
                        final_itinerary.append(ItineraryDay(day_number=current_day_global, places_visited=places_as_dicts, segments=[
                            RouteSegment(from_place=current_hotel.name, to_place=special_place.name, distance_meters=0.0, duration_minutes=30, transport_mode="🚗 Navetta", departure_time="08:30", arrival_time="09:00", additional_info="Inizio attività"),
                            RouteSegment(from_place=special_place.name, to_place=current_hotel.name, distance_meters=0.0, duration_minutes=30, transport_mode="🚗 Navetta", departure_time="17:00", arrival_time="17:30", additional_info="Rientro alloggio")
                        ]))
                        current_day_global += 1
                        continue

                    if g_idx < len(flat_days_raw) - 1:
                        next_day_data = flat_days_raw[g_idx + 1]
                        next_hotel = next_day_data["meta_hotel"]
                        
                        if current_hotel.id != next_hotel.id:
                            dist_m, duration_min, info, mode = routing_svc.get_real_transit_route(current_hotel.lat, current_hotel.lon, next_hotel.lat, next_hotel.lon)
                            
                            if current_hub in internal_transports:
                                f_auto = routing_svc.scrape_flight_route_auto(internal_transports[current_hub]["code"])
                                info = f"Volo {f_auto['code']} ({f_auto['from']} ➔ {f_auto['to']})"
                                mode = "✈️ Volo Interno"

                            if day_data["segments"]:
                                last_seg_time = day_data["segments"][-1]["arrival_time"]
                                day_data["segments"][-1] = {
                                    "from_place": day_data["segments"][-1]["from_place"],
                                    "to_place": next_hotel.name,
                                    "distance_meters": dist_m, "duration_minutes": duration_min,
                                    "transport_mode": mode, "departure_time": last_seg_time if last_seg_time != "Fine" else "17:00",
                                    "arrival_time": "In serata", "additional_info": info
                                }
                            else:
                                day_data["segments"].append({
                                    "from_place": current_hotel.name, "to_place": next_hotel.name,
                                    "distance_meters": dist_m, "duration_minutes": duration_min,
                                    "transport_mode": mode, "departure_time": "16:00", "arrival_time": "In serata", "additional_info": info
                                })
                            if next_hotel not in day_data["places_visited"]:
                                day_data["places_visited"].append(next_hotel)
                    else:
                        if day_data["segments"]:
                            last_dep = day_data["segments"][-1]["arrival_time"]
                            day_data["segments"].append({
                                "from_place": current_hotel.name, "to_place": "🛫 Aeroporto Internazionale (Volo di Rientro)", "distance_meters": 15000.0, "duration_minutes": 45, "transport_mode": "🚇 Navetta / Taxi", "departure_time": last_dep if last_dep != "Fine" else "19:00", "arrival_time": "Fine", "additional_info": "Spostamento finale per imbarco volo di ritorno."
                            })

                    for seg in day_data["segments"]:
                        validated_segments.append(RouteSegment(**seg))
                    places_as_dicts = [p.model_dump() if hasattr(p, 'model_dump') else p for p in day_data["places_visited"]]
                    final_itinerary.append(ItineraryDay(day_number=current_day_global, places_visited=places_as_dicts, segments=validated_segments))
                    current_day_global += 1

                # ERRORE 6 RISOLTO: Se mancano giorni per coprire la data finale del viaggio (es. fino al 05/04), li estendiamo qui
                total_trip_days = st.session_state.num_days
                while current_day_global <= total_trip_days:
                    last_hotel = flat_days_raw[-1]["meta_hotel"] if flat_days_raw else None
                    final_itinerary.append(ItineraryDay(
                        day_number=current_day_global,
                        places_visited=[last_hotel.model_dump()] if last_hotel else [],
                        segments=[]
                    ))
                    current_day_global += 1
                
                st.session_state.itinerary = final_itinerary

    if st.session_state.itinerary:
        try:
            base_date = datetime.strptime(st.session_state.get("start_date").replace("-", "/"), "%Y/%m/%d")
        except Exception:
            base_date = datetime.today()
            
        final_map_df = pd.DataFrame([{"latitude": p.lat, "longitude": p.lon, "name": p.name} for p in st.session_state.selected_places])
        st.map(final_map_df, width='stretch')
        
        for day in st.session_state.itinerary:
            current_date = base_date + timedelta(days=day.day_number - 1)
            with st.expander(f"🗓️ GIORNO {day.day_number} - {current_date.strftime('%d/%m/%Y')}", expanded=True):
                if not day.places_visited:
                    st.markdown("_Giornata libera di relax o rientro._")
                    continue
                
                first_segment_departure = day.segments[0].departure_time if day.segments else "09:00"
                try:
                    hour_check = int(first_segment_departure.split(":")[0])
                    is_late_night = hour_check >= 21 or hour_check < 5
                except Exception:
                    is_late_night = False

                for idx, place in enumerate(day.places_visited):
                    p_name = place.get('name', 'Sconosciuto') if isinstance(place, dict) else getattr(place, 'name', 'Sconosciuto')
                    p_name = re.sub(r'\[Check-in:.*?\]', '', p_name).strip()
                    
                    start_time = "--:--"
                    if idx == 0 and day.segments:
                        start_time = day.segments[0].departure_time
                    elif idx > 0 and idx - 1 < len(day.segments):
                        start_time = day.segments[idx - 1].arrival_time

                    end_time = day.segments[idx].departure_time if idx < len(day.segments) else "Fine"
                    
                    # Corretto l'allineamento degli orari diurni per evitare sfasamenti a tarda notte
                    if is_late_night and "Alloggio" not in p_name and "Volo" not in p_name and "Arrivo" not in p_name and "Ritiro" not in p_name:
                        simulated_hour = 9 + (idx * 2)
                        start_time = f"{simulated_hour:02d}:00"
                        end_time = f"{(simulated_hour + 1):02d}:00"
                    
                    if start_time == end_time and end_time != "Fine":
                        try:
                            h, m = map(int, start_time.split(":"))
                            v_dur = place.get('visit_duration_minutes', 60) if isinstance(place, dict) else getattr(place, 'visit_duration_minutes', 60)
                            m_total = m + v_dur
                            end_time = f"{(h + m_total // 60) % 24:02d}:{m_total % 60:02d}"
                        except Exception:
                            pass

                    st.markdown(f"**{start_time} - {end_time}** | 📍 **{p_name}**")
                    
                    if idx < len(day.segments):
                        seg = day.segments[idx]
                        dist_km = seg.distance_meters / 1000
                        extra_details = f" ({seg.additional_info})" if seg.additional_info and "Cammina" not in seg.additional_info and "A piedi" not in seg.additional_info else ""
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;↳ ➡️ *{seg.transport_mode}{extra_details} | {dist_km:.1f} km | {seg.duration_minutes:.02g} min*")

    if st.button("🔄 Pianifica un nuovo viaggio", use_container_width=True):
        st.session_state.clear()
        st.rerun()