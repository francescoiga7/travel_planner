import streamlit as st
import pandas as pd

def render_step2() -> None:
    st.header(f"2. Cosa vedere a: {st.session_state.location} ({st.session_state.num_days} giorni totali)")
    
    col_list, col_map = st.columns([1, 1])
    selected = []
    
    with col_list:
        st.caption("Seleziona i punti di interesse suddivisi per ciascuna delle tue tappe:")
        
        if isinstance(st.session_state.attractions, dict):
            for hub, hub_list in st.session_state.attractions.items():
                with st.expander(f"🏙️ Monumenti e Punti di Interesse consigliati a {hub}", expanded=True):
                    if not hub_list:
                        st.write("_Nessun monumento rilevato per questa specifica area geografica._")
                    for p in hub_list:
                        stars = "⭐" * p.rating
                        if st.checkbox(f"{p.name} ({p.category}) - {stars}", key=f"poi_{hub}_{p.id}"):
                            selected.append(p)
        else:
            for p in st.session_state.attractions:
                stars = "⭐" * p.rating
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
            st.info("Seleziona una o più caselle a sinistra per visualizzare la distribuzione geografica dei nodi.")
            
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Genera Itinerario Ottimizzato", use_container_width=True):
            if len(selected) < 1:
                st.warning("Seleziona almeno 1 attività per abilitare i motori di calcolo TSP.")
            else:
                st.session_state.selected_places = selected
                st.session_state.step = 3
                st.rerun()
    with col_btn2:
        if st.button("🔙 Torna alla ricerca", use_container_width=True):
            st.session_state.step = 1
            st.rerun()