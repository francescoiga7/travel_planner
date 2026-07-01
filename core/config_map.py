# core/config_map.py

from conf.messico import MESSICO_CONFIG
from conf.indonesia import INDONESIA_CONFIG
from conf.usa import USA_CONFIG
from conf.thailandia import THAILANDIA_CONFIG
from conf.giappone import GIAPPONE_CONFIG
from conf.cina import CINA_CONFIG
from conf.egitto import EGITTO_CONFIG

COUNTRY_CONFIG_MAP = {
    "messico": MESSICO_CONFIG,
    "mexico": MESSICO_CONFIG,
    "indonesia": INDONESIA_CONFIG,
    "usa": USA_CONFIG,
    "thailandia": THAILANDIA_CONFIG,
    "giappone": GIAPPONE_CONFIG,
    "cina": CINA_CONFIG,
    "egitto": EGITTO_CONFIG,
}

def get_country_data(country_name: str) -> dict | None:
    """Ritorna i metadati della nazione normalizzando la stringa di input."""
    if not country_name:
        return None
    return COUNTRY_CONFIG_MAP.get(country_name.strip().lower())