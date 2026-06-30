import streamlit as st
import pandas as pd

def render_step3() -> None:
    st.header(f"3. Cosa vedere a: {st.session_state.location} ({st.session_state.num_days} giorni totali)")
    
    col_list, col_map = st.columns([1, 1])
    selected = []
    
    with col_list:
        st.caption("Seleziona i punti di interesse presi direttamente dalla mappa ufficiale:")
        
        if isinstance(st.session_state.attractions, dict):
            for hub, hub_list in st.session_state.attractions.items():
                with st.expander(f"🏙️ Monumenti e Punti di Interesse consigliati a {hub}", expanded=True):
                    if not hub_list:
                        st.write("_Nessun monumento mappato in archivio per questa località._")
                        continue
                    
                    for p in hub_list:
                        stars = "⭐" * p.rating
                        # Casella di spunta per ciascuna attrazione statica
                        if st.checkbox(f"📍 {p.name} - {stars}", key=f"poi_{hub}_{p.id}"):
                            selected.append(p)
        else:
            for p in st.session_state.attractions:
                stars = "⭐" * p.rating
                if st.checkbox(f"📍 {p.name} - {stars}", key=p.id):
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
            st.info("Seleziona i punti di interesse della ConfigMap a sinistra per aggiornare geometricamente la mappa.")
            
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Genera Itinerario Ottimizzato", use_container_width=True):
            if len(selected) < 1:
                st.warning("Seleziona almeno 1 attività per inizializzare il motore TSP.")
            else:
                st.session_state.selected_places = selected
                st.session_state.step = 4
                st.rerun()
    with col_btn2:
        if st.button("🔙 Torna alla pianificazione tappe", use_container_width=True):
            st.session_state.step = 2
            st.rerun()