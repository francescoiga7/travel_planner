import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from services.places_api import PlacesService
from services.routing_api import RoutingService
from services.llm_engine import LLMEngine
from core.logger import get_logger
from core.models import RouteSegment, ItineraryDay

logger = get_logger(__name__)

places_svc = PlacesService()
routing_svc = RoutingService()
llm_svc = LLMEngine()

def init_session_state() -> None:
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'location' not in st.session_state:
        st.session_state.location = ""
    if 'attractions' not in st.session_state:
        st.session_state.attractions = []
    if 'selected_places' not in st.session_state:
        st.session_state.selected_places = []
    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = None
    if 'reasoning_logs' not in st.session_state:
        st.session_state.reasoning_logs = []
    if 'num_days' not in st.session_state:
        st.session_state.num_days = 3
    if 'hotel_name' not in st.session_state:
        st.session_state.hotel_name = ""
    if 'hotel_place' not in st.session_state:
        st.session_state.hotel_place = None

def main() -> None:
    st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")
    init_session_state()
    
    st.title("🌍 Smart Travel Planner & Routing Engine")

    # --- STEP 1: Input Località, Date e Hotel ---
    if st.session_state.step == 1:
        st.header("1. Scegli la destinazione e i dettagli del soggiorno")
        
        trip_type = st.radio("Tipo di destinazione", ["Città Singola (es: Roma)", "Nazione / Multi-tappa (es: Indonesia)"])
        location = st.text_input("Inserisci la destinazione", st.session_state.location)
        
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Data di Partenza", datetime.today())
        with col_end:
            end_date = st.date_input("Data di Ritorno", datetime.today() + timedelta(days=3))
            
        hotel_input = st.text_input("Hotel Prenotato (es: Hotel Artemide Roma, o un indirizzo specifico)", st.session_state.hotel_name)
        
        num_days = (end_date - start_date).days + 1
        
        if st.button("Avanti", use_container_width=True):
            if not location or not hotel_input:
                st.error("Inserisci sia la destinazione che l'hotel per ottimizzare i percorsi!")
                return
                
            st.session_state.location = location
            st.session_state.num_days = num_days
            st.session_state.hotel_name = hotel_input
            
            with st.spinner("Geolocalizzazione dell'Hotel e analisi destinazione..."):
                # Geocodifichiamo l'hotel per avere lat/lon esatte
                hotel_coords = places_svc.get_coordinates(hotel_input)
                if hotel_coords:
                    from core.models import Place
                    st.session_state.hotel_place = Place(
                        id="hotel_hub_node",
                        name=f"🏨 {hotel_input}",
                        lat=hotel_coords[0],
                        lon=hotel_coords[1],
                        category="hotel",
                        rating=5
                    )
                else:
                    st.warning("Impossibile trovare la posizione esatta dell'hotel. Verrà usato il centro città come base.")
            
            if "Nazione" in trip_type:
                with st.spinner(f"Ricerca dei principali hub in {location}..."):
                    st.session_state.hub_options = llm_svc.get_country_hubs(location)
                    st.session_state.step = 1.5
                    st.rerun()
            else:
                with st.spinner("Scaricamento attrazioni locali..."):
                    coords = places_svc.get_coordinates(location)
                    st.session_state.attractions = places_svc.fetch_attractions(*coords)
                    st.session_state.step = 2
                    st.rerun()

    # --- STEP 2: Selezione Attività con Visualizzazione Mappa ---
    elif st.session_state.step == 2:
        st.header(f"2. Cosa vedere a: {st.session_state.location} ({st.session_state.num_days} giorni ordinati)")
        
        col_list, col_map = st.columns([1, 1])
        selected = []
        
        with col_list:
            st.caption("Seleziona i punti di interesse da includere nell'itinerario:")
            for p in st.session_state.attractions:
                stars = "⭐" * p.rating
                # Il key ora è garantito univoco grazie al fix dello Step 1
                if st.checkbox(f"{p.name} ({p.category}) - {stars}", key=p.id):
                    selected.append(p)
                    
        with col_map:
            st.write("### 🗺️ Georilevazione in Tempo Reale")
            if selected:
                map_df = pd.DataFrame([{
                    "latitude": p.lat,
                    "longitude": p.lon,
                    "name": p.name
                } for p in selected])
                st.map(map_df, width='stretch')
            else:
                st.info("Seleziona una o più caselle a sinistra per mappare i nodi geografici.")
                
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Genera Itinerario Ottimizzato", use_container_width=True):
                if len(selected) < 1:
                    st.warning("Seleziona almeno 1 attività per generare il piano di viaggio.")
                else:
                    st.session_state.selected_places = selected
                    st.session_state.step = 3
                    st.rerun()
        with col_btn2:
            if st.button("🔙 Torna alla ricerca", use_container_width=True):
                st.session_state.step = 1
                st.rerun()

# --- STEP 3: Generazione ed Ottimizzazione con Vincolo Hotel ---
    elif st.session_state.step == 3:
        st.header(f"3. Il tuo Itinerario Ottimizzato dal al (Giorni: {st.session_state.num_days})")
        st.subheader(f"Base Operativa: {st.session_state.hotel_name}")
        
        if not st.session_state.itinerary:
            with st.spinner("Clustering Spaziale e Calcolo Itinerari con Rientro in Hotel..."):
                places = st.session_state.selected_places
                num_days = st.session_state.num_days
                hotel = st.session_state.hotel_place
                
                # 1. Clustering spaziale K-Means
                daily_clusters = routing_svc.cluster_pois_by_day(places, num_days)
                places_dict = {p.id: p for p in places}
                if hotel:
                    places_dict[hotel.id] = hotel
                
                # 2. Costruzione itinerario deterministico passando l'hotel
                raw_itinerary = routing_svc.build_deterministic_itinerary(
                    daily_clusters, places_dict, hotel_place=hotel
                )
                
                # 3. Parsing Pydantic
                final_itinerary = []
                for day in raw_itinerary:
                    segments = [RouteSegment(**seg) for seg in day["segments"]]
                    final_itinerary.append(ItineraryDay(
                        day_number=day["day_number"],
                        places_visited=day["places_visited"],
                        segments=segments
                    ))
                
                st.session_state.itinerary = final_itinerary
                st.session_state.reasoning_logs = ["Ottimizzazione TSP ad anello chiusa sull'Hotel completata."]

        if st.session_state.reasoning_logs:
            with st.status("🧠 Log del Ragionamento Spaziale (Engine Deterministico)", expanded=False):
                for log in st.session_state.reasoning_logs:
                    st.code(f"[ENGINE_LOG] {log}", language="bash")

        if st.session_state.itinerary:
            st.write("### 📅 Programma di Viaggio")
            
            final_map_df = pd.DataFrame([{
                "latitude": p.lat,
                "longitude": p.lon,
                "name": p.name
            } for p in st.session_state.selected_places])
            st.map(final_map_df, width='stretch')
            
            for day in st.session_state.itinerary:
                with st.expander(f"Giorno {day.day_number}", expanded=True):
                    if day.places_visited:
                        st.markdown("**Luoghi visitati oggi:** " + ", ".join([p.name for p in day.places_visited]))
                    else:
                        st.markdown("_Nessuna attività pianificata per oggi. Giornata libera o di trasferimento._")
                    st.markdown("---")
                    
                    for seg in day.segments:
                        col1, col2 = st.columns([1, 4])
                        mode_lower = seg.transport_mode.lower()
                        
                        icon = "🚶"
                        if "mezzi" in mode_lower or "bus" in mode_lower or "metro" in mode_lower:
                            icon = "🚇"
                        elif "taxi" in mode_lower or "auto" in mode_lower:
                            icon = "🚖"
                            
                        with col1:
                            st.write(f"**{icon} {seg.transport_mode}**")
                        with col2:
                            st.write(f"Da **{seg.from_place}** a **{seg.to_place}**")
                            if seg.distance_meters > 0:
                                st.caption(f"Distanza: {seg.distance_meters} m | Tempo Stimato: {seg.duration_minutes} min")
                            if seg.additional_info:
                                st.info(seg.additional_info)
        else:
            st.error("Errore critico durante la generazione dello scaffolding strutturale.")

        if st.button("🔄 Pianifica un nuovo viaggio", use_container_width=True):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()