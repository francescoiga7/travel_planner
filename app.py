import streamlit as st
from services.places_api import PlacesService
from services.routing_api import RoutingService
from services.llm_engine import LLMEngine
from core.logger import get_logger

# Import dei componenti di interfaccia scorporati
from views.step1 import render_step1
from views.step1_5 import render_step1_5
from views.step2 import render_step2
from views.step3 import render_step3

logger = get_logger(__name__)

places_svc = PlacesService()
routing_svc = RoutingService()
llm_svc = LLMEngine()

def init_session_state() -> None:
    defaults = {
        'step': 1, 'location': "", 'attractions': [], 'selected_places': [],
        'itinerary': None, 'reasoning_logs': [], 'num_days': 3, 'hotel_name': "",
        'hotel_place': None, 'flight_info': "", 'pre_selected_cities': [],
        'hub_options': [], 'multi_itinerary_config': {}
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def main() -> None:
    st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")
    init_session_state()
    
    st.title("🌍 Smart Travel Planner & Routing Engine")

    # Routing delle viste basato sullo stato globale dell'applicazione
    if st.session_state.step == 1:
        render_step1(places_svc, llm_svc)
        
    elif st.session_state.step == 1.5:
        render_step1_5(places_svc, llm_svc, logger)
        
    elif st.session_state.step == 2:
        render_step2()
        
    elif st.session_state.step == 3:
        render_step3(places_svc, routing_svc)

if __name__ == "__main__":
    main()