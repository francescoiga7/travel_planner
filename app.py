import streamlit as st
import pandas as pd
from services.places_api import PlacesService
from services.routing_api import RoutingService
from services.llm_engine import LLMEngine
from core.logger import get_logger

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

def main() -> None:
    st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")
    init_session_state()
    
    st.title("🌍 Smart Travel Planner & Routing Engine")

    # --- STEP 1: Input Località ---
    if st.session_state.step == 1:
        st.header("1. Scegli la destinazione")
        location = st.text_input("Inserisci una città o nazione (es: Roma, Indonesia, Messico)", st.session_state.location)
        
        if st.button("Cerca Attività"):
            if location:
                with st.spinner("Interrogazione dei database geografici ed esecuzione fallback semantici..."):
                    coords = places_svc.get_coordinates(location)
                    attractions = []
                    if coords:
                        attractions = places_svc.fetch_attractions(*coords)
                    
                    if not attractions:
                        logger.info(f"Nessun dato locale trovato per '{location}'. Attivazione del fallback semantico via LLM.")
                        attractions = llm_svc.fetch_attractions_fallback(location)
                    
                    if attractions:
                        st.session_state.location = location
                        st.session_state.attractions = attractions
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("Impossibile recuperare punti di interesse per questa località.")

    # --- STEP 2: Selezione Attività con Visualizzazione Mappa ---
    elif st.session_state.step == 2:
        st.header(f"2. Cosa vedere a: {st.session_state.location}")
        
        # Split dello schermo per visualizzazione affiancata Lista / Mappa
        col_list, col_map = st.columns([1, 1])
        selected = []
        
        with col_list:
            st.caption("Seleziona i punti di interesse:")
            for p in st.session_state.attractions:
                stars = "⭐" * p.rating
                if st.checkbox(f"{p.name} ({p.category}) - {stars}", key=p.id):
                    selected.append(p)
                    
        with col_map:
            st.write("### 🗺️ Georilevazione in Tempo Reale")
            if selected:
                # Creazione del DataFrame richiesto nativamente da st.map
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
            if st.button("Genera Itinerario Ottimizzato"):
                if len(selected) < 2:
                    st.warning("Seleziona almeno 2 attività per calcolare la matrice dei percorsi.")
                else:
                    st.session_state.selected_places = selected
                    st.session_state.step = 3
                    st.rerun()
        with col_btn2:
            if st.button("🔙 Torna alla ricerca"):
                st.session_state.step = 1
                st.rerun()

    # --- STEP 3: Generazione ed Ottimizzazione ---
    elif st.session_state.step == 3:
        st.header("3. Il tuo Itinerario Ottimizzato")
        
        if not st.session_state.itinerary:
            with st.spinner("Analisi dei nodi geografici, calcolo matrici OSRM e inferenza logistica..."):
                places = st.session_state.selected_places
                distances = {}
                
                for i in range(len(places)-1):
                    p1, p2 = places[i], places[i+1]
                    dist, duration = routing_svc.get_walking_route(p1, p2)
                    distances[(p1.name, p2.name)] = {"dist": dist, "time": duration}
                
                itinerary, logs = llm_svc.optimize_and_enrich_itinerary(
                    st.session_state.location, places, distances
                )
                st.session_state.itinerary = itinerary
                st.session_state.reasoning_logs = logs

        if st.session_state.reasoning_logs:
            with st.status("🧠 Log del Ragionamento dell'AI (Ottimizzazione Spostamenti)", expanded=True):
                for log in st.session_state.reasoning_logs:
                    st.code(f"[ENGINE_LOG] {log}", language="bash")

        if st.session_state.itinerary:
            st.write("### 📅 Programma di Viaggio")
            
            # Mostriamo la mappa complessiva del viaggio anche nello step finale
            final_map_df = pd.DataFrame([{
                "latitude": p.lat,
                "longitude": p.lon,
                "name": p.name
            } for p in st.session_state.selected_places])
            st.map(final_map_df, width='stretch')
            
            for day in st.session_state.itinerary:
                with st.expander(f"Giorno {day.day_number}", expanded=True):
                    st.markdown("**Luoghi visitati:** " + ", ".join([p.name for p in day.places_visited]))
                    st.markdown("---")
                    
                    for seg in day.segments:
                        col1, col2 = st.columns([1, 4])
                        mode_lower = seg.transport_mode.lower()
                        icon = "🚶" if "piede" in mode_lower or "walk" in mode_lower else "🚇"
                        if "volo" in mode_lower or "aereo" in mode_lower: icon = "✈️"
                        elif "treno" in mode_lower: icon = "🚆"
                            
                        with col1:
                            st.write(f"**{icon} {seg.transport_mode}**")
                        with col2:
                            st.write(f"Da **{seg.from_place}** a **{seg.to_place}**")
                            if seg.distance_meters > 0:
                                st.caption(f"Spazio: {seg.distance_meters}m | Tempo: {seg.duration_minutes} min")
                            if seg.additional_info:
                                st.info(seg.additional_info)
        else:
            st.error("Errore critico durante la generazione o la mappatura dei nodi.")

        if st.button("🔄 Pianifica un nuovo viaggio"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()