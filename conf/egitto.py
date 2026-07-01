# conf/egitto.py

EGITTO_CONFIG = {
    "country_name": "Egitto",
    "default_hubs": [
        "Il Cairo", "Luxor", "Aswan", "Sharm el-Sheikh", "Hurghada",
        "Alessandria", "Marsa Alam", "Giza", "Siwa Oasis", "Dahab",
        "Port Said", "Suez"
    ],
    "coordinates": {
        "Il Cairo": [30.0444, 31.2357],
        "Luxor": [25.6872, 32.6396],
        "Aswan": [24.0889, 32.8998],
        "Sharm el-Sheikh": [27.9158, 34.3299],
        "Hurghada": [27.2579, 33.8116],
        "Alessandria": [31.2001, 29.9187],
        "Marsa Alam": [25.0719, 34.8932],
        "Giza": [30.0131, 31.2089],
        "Siwa Oasis": [29.2032, 25.5195],
        "Dahab": [28.5094, 34.5134],
        "Port Said": [31.2653, 32.3019],
        "Suez": [29.9668, 32.5498]
    },
    "escursioni_predefinite": [
        {"hub": "Il Cairo", "desc": "Visita alle Piramidi di Giza e alla Sfinge", "durata": 240},
        {"hub": "Il Cairo", "desc": "Tour del Museo Egizio e bazar di Khan el-Khalili", "durata": 300},
        {"hub": "Luxor", "desc": "Tour della Valle dei Re e Tempio di Hatshepsut", "durata": 360},
        {"hub": "Luxor", "desc": "Visita ai Templi di Karnak e Luxor", "durata": 240},
        {"hub": "Luxor", "desc": "Volo in mongolfiera all'alba sulla Valle dei Re", "durata": 120},
        {"hub": "Aswan", "desc": "Escursione ai Templi di Abu Simbel", "durata": 540},
        {"hub": "Aswan", "desc": "Giro in feluca sul Nilo e visita al Tempio di Philae", "durata": 180},
        {"hub": "Sharm el-Sheikh", "desc": "Snorkeling nel Parco Nazionale di Ras Mohammed", "durata": 360},
        {"hub": "Sharm el-Sheikh", "desc": "Safari nel deserto in quad al tramonto", "durata": 180},
        {"hub": "Alessandria", "desc": "Tour delle Catacombe e della Biblioteca di Alessandria", "durata": 240}
    ],
    "attrazioni": {
        "Il Cairo": [
            {"attivita": "Egyptian Museum (Piazza Tahrir)", "coordinates": [30.0478, 31.2336]},
            {"attivita": "Khan el-Khalili", "coordinates": [30.0475, 31.2622]},
            {"attivita": "The Citadel of Saladin", "coordinates": [30.0294, 31.2614]},
            {"attivita": "Al-Azhar Mosque", "coordinates": [30.0458, 31.2625]},
            {"attivita": "Coptic Cairo & Hanging Church", "coordinates": [30.0053, 31.2301]},
            {"attivita": "Cairo Tower", "coordinates": [30.0458, 31.2242]},
            {"attivita": "Al-Azhar Park", "coordinates": [30.0411, 31.2653]},
            {"attivita": "Mosque of Sultan Hassan", "coordinates": [30.0322, 31.2561]},
            {"attivita": "Museum of Islamic Art", "coordinates": [30.0442, 31.2514]},
            {"attivita": "National Museum of Egyptian Civilization (NMEC)", "coordinates": [30.0083, 31.2481]}
        ],
        "Luxor": [
            {"attivita": "Valley of the Kings", "coordinates": [25.7401, 32.6014]},
            {"attivita": "Karnak Temple Complex", "coordinates": [25.7188, 32.6586]},
            {"attivita": "Luxor Temple", "coordinates": [25.6997, 32.6394]},
            {"attivita": "Mortuary Temple of Hatshepsut", "coordinates": [25.7381, 32.6067]},
            {"attivita": "Colossi of Memnon", "coordinates": [25.7203, 32.6103]},
            {"attivita": "Valley of the Queens", "coordinates": [25.7281, 32.5931]},
            {"attivita": "Luxor Museum", "coordinates": [25.7075, 32.6436]},
            {"attivita": "Medinet Habu Temple", "coordinates": [25.7206, 32.6008]},
            {"attivita": "Ramesseum", "coordinates": [25.7289, 32.6106]},
            {"attivita": "Deir el-Medina (Artisans Village)", "coordinates": [25.7286, 32.6014]}
        ],
        "Aswan": [
            {"attivita": "Philae Temple", "coordinates": [24.0253, 32.8844]},
            {"attivita": "Aswan High Dam", "coordinates": [23.9697, 32.8664]},
            {"attivita": "The Unfinished Obelisk", "coordinates": [24.0768, 32.8953]},
            {"attivita": "Elephantine Island", "coordinates": [24.0914, 32.8872]},
            {"attivita": "Nubian Village", "coordinates": [24.0583, 32.8672]},
            {"attivita": "Nubian Museum", "coordinates": [24.0792, 32.8886]},
            {"attivita": "Tombs of the Nobles", "coordinates": [24.1031, 32.8814]},
            {"attivita": "Kitchener's Island (Botanical Garden)", "coordinates": [24.0936, 32.8894]},
            {"attivita": "Temple of Kom Ombo (Area)", "coordinates": [24.4711, 32.9286]},
            {"attivita": "Agha Khan Mausoleum", "coordinates": [24.0847, 32.8711]}
        ],
        "Sharm el-Sheikh": [
            {"attivita": "Ras Mohammed National Park", "coordinates": [27.7554, 34.2542]},
            {"attivita": "Naama Bay", "coordinates": [27.9142, 34.3247]},
            {"attivita": "Soho Square", "coordinates": [27.9653, 34.3944]},
            {"attivita": "Old Market & Al Sahaba Mosque", "coordinates": [27.8656, 34.2986]},
            {"attivita": "Shark's Bay", "coordinates": [27.9542, 34.3892]},
            {"attivita": "Hollywood Sharm El Sheikh", "coordinates": [27.9256, 34.3414]},
            {"attivita": "Nabq Protected Area", "coordinates": [28.0931, 34.4361]},
            {"attivita": "Aqua Blue Water Park", "coordinates": [27.8647, 34.3056]},
            {"attivita": "Al Mustafa Mosque", "coordinates": [27.8931, 34.3008]},
            {"attivita": "Cleo Park", "coordinates": [27.9136, 34.3211]}
        ],
        "Hurghada": [
            {"attivita": "Giftun Islands", "coordinates": [27.2281, 33.9317]},
            {"attivita": "Hurghada Marina", "coordinates": [27.2219, 33.8436]},
            {"attivita": "El Dahar (Old Town)", "coordinates": [27.2589, 33.8116]},
            {"attivita": "Hurghada Grand Aquarium", "coordinates": [27.1356, 33.8214]},
            {"attivita": "Makadi Bay Water World", "coordinates": [26.9856, 33.8964]},
            {"attivita": "Sand City Hurghada", "coordinates": [27.1147, 33.8256]},
            {"attivita": "Mini Egypt Park", "coordinates": [26.9631, 33.9114]},
            {"attivita": "Soma Bay (Area Balneare)", "coordinates": [26.8472, 33.9892]},
            {"attivita": "Senzo Mall", "coordinates": [27.0989, 33.8242]},
            {"attivita": "Al Mina Mosque", "coordinates": [27.2256, 33.8414]}
        ],
        "Alessandria": [
            {"attivita": "Bibliotheca Alexandrina", "coordinates": [31.2089, 29.9092]},
            {"attivita": "Citadel of Qaitbay", "coordinates": [31.2141, 29.8821]},
            {"attivita": "Pompey's Pillar", "coordinates": [31.1825, 29.8967]},
            {"attivita": "Catacombs of Kom El Shoqafa", "coordinates": [31.1786, 29.8928]},
            {"attivita": "Montaza Palace Gardens", "coordinates": [31.2872, 30.0156]},
            {"attivita": "Roman Amphitheatre (Kom El Deka)", "coordinates": [31.1953, 29.9167]},
            {"attivita": "Alexandria National Museum", "coordinates": [31.2011, 29.9189]},
            {"attivita": "Stanley Bridge", "coordinates": [31.2344, 29.9483]},
            {"attivita": "Abu al-Abbas al-Mursi Mosque", "coordinates": [31.2056, 29.8822]},
            {"attivita": "Royal Jewelry Museum", "coordinates": [31.2411, 29.9614]}
        ],
        "Marsa Alam": [
            {"attivita": "Abu Dabbab Bay", "coordinates": [25.3371, 34.7412]},
            {"attivita": "Sataya Reef (Dolphin House)", "coordinates": [24.1623, 35.1914]},
            {"attivita": "Wadi El Gemal National Park", "coordinates": [24.3942, 35.0931]},
            {"attivita": "Sharm El Luli", "coordinates": [24.6056, 35.1214]},
            {"attivita": "Marsa Mubarak", "coordinates": [25.5089, 34.6472]},
            {"attivita": "Port Ghalib Marina", "coordinates": [25.5342, 34.6364]},
            {"attivita": "Elphinstone Reef", "coordinates": [25.3142, 34.8611]},
            {"attivita": "Gorgonia Beach Reef", "coordinates": [24.2872, 35.2914]},
            {"attivita": "Coraya Bay", "coordinates": [25.6011, 34.6056]},
            {"attivita": "Hankorab Beach", "coordinates": [24.5811, 35.1414]}
        ],
        "Giza": [
            {"attivita": "Great Pyramid of Giza (Khufu)", "coordinates": [29.9792, 31.1342]},
            {"attivita": "The Great Sphinx of Giza", "coordinates": [29.9753, 31.1376]},
            {"attivita": "Pyramid of Khafre", "coordinates": [29.9761, 31.1308]},
            {"attivita": "Pyramid of Menkaure", "coordinates": [29.9725, 31.1283]},
            {"attivita": "Grand Egyptian Museum (GEM)", "coordinates": [29.9953, 31.1194]},
            {"attivita": "Giza Plateau Panoramic View", "coordinates": [29.9731, 31.1214]},
            {"attivita": "Solar Boat Museum (Sito)", "coordinates": [29.9781, 31.1344]},
            {"attivita": "Saqqara Step Pyramid (Area)", "coordinates": [29.8711, 31.2142]},
            {"attivita": "Memphis Open Air Museum (Area)", "coordinates": [29.8456, 31.2531]},
            {"attivita": "Sound & Light Show Giza", "coordinates": [29.9744, 31.1411]}
        ],
        "Siwa Oasis": [
            {"attivita": "Cleopatra's Pool", "coordinates": [29.2014, 25.5342]},
            {"attivita": "Temple of the Oracle of Amun", "coordinates": [29.2043, 25.5416]},
            {"attivita": "Shali Fortress", "coordinates": [29.2031, 25.5189]},
            {"attivita": "Gebel al-Mawta (Mountain of the Dead)", "coordinates": [29.2114, 25.5183]},
            {"attivita": "Fatnas Island (Sunset View)", "coordinates": [29.2025, 25.4856]},
            {"attivita": "Siwa Salt Lakes", "coordinates": [29.2214, 25.6124]},
            {"attivita": "Great Sand Sea (Safari Area)", "coordinates": [29.1114, 25.4114]},
            {"attivita": "Bir Wahed (Desert Spring)", "coordinates": [29.1436, 25.2636]},
            {"attivita": "Siwa House Museum", "coordinates": [29.2019, 25.5192]},
            {"attivita": "Amun Temple Ruins", "coordinates": [29.2011, 25.5464]}
        ],
        "Dahab": [
            {"attivita": "The Blue Hole", "coordinates": [28.5721, 34.5364]},
            {"attivita": "Lighthouse Reef", "coordinates": [28.5034, 34.5222]},
            {"attivita": "The Canyon (Immersioni)", "coordinates": [28.5531, 34.5311]},
            {"attivita": "Blue Lagoon", "coordinates": [28.6311, 34.5489]},
            {"attivita": "Ras Abu Galum Protected Area", "coordinates": [28.6014, 34.5556]},
            {"attivita": "Laguna Beach (Windsurf Area)", "coordinates": [28.4856, 34.5122]},
            {"attivita": "Eel Garden Reef", "coordinates": [28.5106, 34.5244]},
            {"attivita": "Mashraba Beach", "coordinates": [28.4967, 34.5192]},
            {"attivita": "Three Pools (Snorkeling)", "coordinates": [28.4124, 34.4636]},
            {"attivita": "Wadi Gnai (Climbing Area)", "coordinates": [28.4236, 34.4114]}
        ],
        "Port Said": [
            {"attivita": "Port Said Lighthouse", "coordinates": [31.2644, 32.3056]},
            {"attivita": "Military Museum", "coordinates": [31.2589, 32.2954]},
            {"attivita": "Suez Canal Authority Building", "coordinates": [31.2575, 32.3061]},
            {"attivita": "Port Said Boardwalk", "coordinates": [31.2653, 32.3019]},
            {"attivita": "Port Fouad Ferry", "coordinates": [31.2611, 32.3072]},
            {"attivita": "Great Mosque of Port Fouad", "coordinates": [31.2581, 32.3175]},
            {"attivita": "El-Nasr Museum For Modern Art", "coordinates": [31.2536, 32.2911]},
            {"attivita": "Ashtoum el-Gamil National Park", "coordinates": [31.2783, 32.1614]},
            {"attivita": "Port Said Tourist Market", "coordinates": [31.2619, 32.2936]},
            {"attivita": "Base de la Statue de de Lesseps", "coordinates": [31.2675, 32.3042]}
        ],
        "Suez": [
            {"attivita": "Suez Canal Port", "coordinates": [29.9324, 32.5632]},
            {"attivita": "El-Arbaeen Mosque", "coordinates": [29.9742, 32.5394]},
            {"attivita": "Suez National Museum", "coordinates": [29.9511, 32.5556]},
            {"attivita": "Port Tawfik Promenade", "coordinates": [29.9356, 32.5686]},
            {"attivita": "Suez Canal Golf Club", "coordinates": [29.9611, 32.5414]},
            {"attivita": "El-Gharib Mosque", "coordinates": [29.9714, 32.5447]},
            {"attivita": "Suez Public Park", "coordinates": [29.9589, 32.5361]},
            {"attivita": "Ataqah Mountains Viewpoint", "coordinates": [29.9114, 32.3414]},
            {"attivita": "Port Tawfik Memorial", "coordinates": [29.9311, 32.5658]},
            {"attivita": "Suez Corniche", "coordinates": [29.9472, 32.5611]}
        ]
    }
}