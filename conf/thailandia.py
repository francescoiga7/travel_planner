# conf/thailandia.py

THAILANDIA_CONFIG = {
    "country_name": "Thailandia",
    "default_hubs": [
        "Bangkok", "Chiang Mai", "Phuket", "Krabi", "Koh Samui",
        "Pattaya", "Ayutthaya", "Sukhothai", "Hua Hin", "Chiang Rai",
        "Koh Tao", "Kanchanaburi"
    ],
    "coordinates": {
        "Bangkok": [13.7563, 100.5018],
        "Chiang Mai": [18.7883, 98.9853],
        "Phuket": [7.8804, 98.3922],
        "Krabi": [8.0855, 98.9067],
        "Koh Samui": [9.5120, 100.0136],
        "Pattaya": [12.9236, 100.8824],
        "Ayutthaya": [14.3532, 100.5681],
        "Sukhothai": [17.0072, 99.8262],
        "Hua Hin": [12.5684, 99.9576],
        "Chiang Rai": [19.9105, 99.8406],
        "Koh Tao": [10.0956, 99.8404],
        "Kanchanaburi": [14.0228, 99.5328]
    },
    "escursioni_predefinite": [
        {"hub": "Bangkok", "desc": "Tour dei Templi Reali e Palazzo Reale", "durata": 240},
        {"hub": "Bangkok", "desc": "Mercato Galleggiante di Damnoen Saduak", "durata": 360},
        {"hub": "Bangkok", "desc": "Gita storica ai templi di Ayutthaya", "durata": 420},
        {"hub": "Kanchanaburi", "desc": "Cascate di Erawan e Ponte sul fiume Kwai", "durata": 480},
        {"hub": "Chiang Mai", "desc": "Santuario degli Elefanti (Etico)", "durata": 480},
        {"hub": "Chiang Mai", "desc": "Tour del tempio Doi Suthep e villaggi Hill Tribe", "durata": 300},
        {"hub": "Chiang Rai", "desc": "Visita al Tempio Bianco (Wat Rong Khun)", "durata": 240},
        {"hub": "Phuket", "desc": "Tour in barca alle isole Phi Phi", "durata": 540},
        {"hub": "Krabi", "desc": "Tour delle 4 Isole in barca tradicional", "durata": 360},
        {"hub": "Koh Tao", "desc": "Battesimo del mare ed escursione di snorkeling", "durata": 300}
    ],
    "attrazioni": {
        "Bangkok": [
            {"attivita": "Grand Palace & Wat Phra Kaew", "coordinates": [13.7516, 100.4927]},
            {"attivita": "Wat Arun (Tempio dell'Alba)", "coordinates": [13.7437, 100.4889]},
            {"attivita": "Wat Pho (Buddha Sdraiato)", "coordinates": [13.7465, 100.4933]},
            {"attivita": "Chatuchak Weekend Market", "coordinates": [13.7999, 100.5506]},
            {"attivita": "Khao San Road", "coordinates": [13.7589, 100.4974]},
            {"attivita": "Jim Thompson House", "coordinates": [13.7492, 100.5283]},
            {"attivita": "Asiatique The Riverfront", "coordinates": [13.7047, 100.5028]},
            {"attivita": "Wat Saket (Golden Mount)", "coordinates": [13.7539, 100.5067]},
            {"attivita": "Lumphini Park", "coordinates": [13.7314, 100.5414]},
            {"attivita": "Siam Paragon", "coordinates": [13.7461, 100.5342]}
        ],
        "Chiang Mai": [
            {"attivita": "Wat Phra That Doi Suthep", "coordinates": [18.8049, 98.9217]},
            {"attivita": "Chiang Mai Night Bazaar", "coordinates": [18.7850, 99.0003]},
            {"attivita": "Wat Chedi Luang", "coordinates": [18.7869, 98.9864]},
            {"attivita": "Wat Phra Singh", "coordinates": [18.7889, 98.9822]},
            {"attivita": "Sunday Walking Street", "coordinates": [18.7878, 98.9856]},
            {"attivita": "Doi Inthanon National Park", "coordinates": [18.5914, 98.4867]},
            {"attivita": "Elephant Nature Park (Ufficio)", "coordinates": [18.7892, 98.9958]},
            {"attivita": "Art in Paradise Chiang Mai", "coordinates": [18.7758, 100.0019]},
            {"attivita": "Wat Umong (Tunnel Temple)", "coordinates": [18.7836, 98.9514]},
            {"attivita": "Nimman Haemin Road", "coordinates": [18.7994, 98.9678]}
        ],
        "Phuket": [
            {"attivita": "Patong Beach & Bangla Road", "coordinates": [7.8939, 98.2964]},
            {"attivita": "Big Buddha Phuket", "coordinates": [7.8277, 98.3128]},
            {"attivita": "Wat Chalong", "coordinates": [7.8467, 98.3364]},
            {"attivita": "Phuket Old Town", "coordinates": [7.8847, 98.3892]},
            {"attivita": "Karon Viewpoint", "coordinates": [7.8214, 98.3025]},
            {"attivita": "Promthep Cape", "coordinates": [7.7631, 98.3056]},
            {"attivita": "Kata Noi Beach", "coordinates": [7.8089, 98.2994]},
            {"attivita": "Phuket FantaSea", "coordinates": [7.9564, 98.2872]},
            {"attivita": "Freedom Beach", "coordinates": [7.8744, 98.2756]},
            {"attivita": "Nai Harn Beach", "coordinates": [7.7928, 98.3053]}
        ],
        "Krabi": [
            {"attivita": "Railay Beach", "coordinates": [8.0119, 98.8393]},
            {"attivita": "Wat Tham Suea (Tiger Cave Temple)", "coordinates": [8.1242, 98.9248]},
            {"attivita": "Ao Nang Beach", "coordinates": [8.0322, 98.8186]},
            {"attivita": "Emerald Pool (Sa Morakot)", "coordinates": [7.9224, 99.2611]},
            {"attivita": "Phra Nang Cave Beach", "coordinates": [8.0089, 98.8378]},
            {"attivita": "Krabi Town Night Market", "coordinates": [8.0650, 98.9167]},
            {"attivita": "Thung Teao Forest Natural Park", "coordinates": [7.9256, 99.2556]},
            {"attivita": "Klong Thom Hot Springs", "coordinates": [7.9261, 99.2989]},
            {"attivita": "Phu Phi Phi (Molo ferry)", "coordinates": [8.0614, 98.9114]},
            {"attivita": "Tab Kak Hang Nak Hill Trail", "coordinates": [8.0931, 98.7522]}
        ],
        "Koh Samui": [
            {"attivita": "Wat Phra Yai (Big Buddha Temple)", "coordinates": [9.5707, 100.0604]},
            {"attivita": "Hin Ta and Hin Yai Rocks", "coordinates": [9.4524, 100.0396]},
            {"attivita": "Chaweng Beach", "coordinates": [9.5328, 100.0614]},
            {"attivita": "Fisherman's Village Bophut", "coordinates": [9.5594, 100.0317]},
            {"attivita": "Lamai Beach", "coordinates": [9.4658, 100.0461]},
            {"attivita": "Na Muang Waterfall 1", "coordinates": [9.4653, 99.9839]},
            {"attivita": "Wat Plai Laem", "coordinates": [9.5714, 100.0669]},
            {"attivita": "Secret Buddha Garden", "coordinates": [9.4831, 99.9944]},
            {"attivita": "Silver Beach", "coordinates": [9.4811, 100.0617]},
            {"attivita": "Samui Elephant Sanctuary", "coordinates": [9.5442, 99.9986]}
        ],
        "Pattaya": [
            {"attivita": "Sanctuary of Truth", "coordinates": [12.9727, 100.8891]},
            {"attivita": "Walking Street Pattaya", "coordinates": [12.9262, 100.8732]},
            {"attivita": "Jomtien Beach", "coordinates": [12.8931, 100.8714]},
            {"attivita": "Nong Nooch Tropical Botanical Garden", "coordinates": [12.7664, 100.9317]},
            {"attivita": "Pattaya Floating Market", "coordinates": [12.8678, 100.9242]},
            {"attivita": "Big Buddha Temple (Wat Phra Yai)", "coordinates": [12.9136, 100.8681]},
            {"attivita": "Art in Paradise Pattaya", "coordinates": [12.9431, 100.8894]},
            {"attivita": "Pattaya Beach Road", "coordinates": [12.9378, 100.8819]},
            {"attivita": "Koh Larn (Coral Island Ferry)", "coordinates": [12.9256, 100.8656]},
            {"attivita": "Ramayana Water Park", "coordinates": [12.7514, 100.9614]}
        ],
        "Ayutthaya": [
            {"attivita": "Wat Mahathat", "coordinates": [14.3570, 100.5675]},
            {"attivita": "Wat Chaiwatthanaram", "coordinates": [14.3436, 100.5414]},
            {"attivita": "Wat Phra Si Sanphet", "coordinates": [14.3558, 100.5583]},
            {"attivita": "Wat Yai Chai Mongkhon", "coordinates": [14.3456, 100.5925]},
            {"attivita": "Ayutthaya Historical Park", "coordinates": [14.3514, 100.5572]},
            {"attivita": "Wat Lokayasutharam", "coordinates": [14.3561, 100.5525]},
            {"attivita": "Wat Ratchaburana", "coordinates": [14.3589, 100.5678]},
            {"attivita": "Bang Pa-In Royal Palace", "coordinates": [14.2314, 100.5783]},
            {"attivita": "Ayutthaya Floating Market", "coordinates": [14.3592, 100.5914]},
            {"attivita": "Wat Phra Ram", "coordinates": [14.3542, 100.5614]}
        ],
        "Sukhothai": [
            {"attivita": "Sukhothai Historical Park", "coordinates": [17.0211, 99.7037]},
            {"attivita": "Wat Mahathat Sukhothai", "coordinates": [17.0177, 99.7042]},
            {"attivita": "Wat Si Chum", "coordinates": [17.0267, 99.6931]},
            {"attivita": "Wat Sra Sri", "coordinates": [17.0194, 99.7019]},
            {"attivita": "Ramkhamhaeng National Museum", "coordinates": [17.0169, 99.7061]},
            {"attivita": "Wat Saphan Hin", "coordinates": [17.0214, 99.6739]},
            {"attivita": "Wat Chang Lom", "coordinates": [17.0142, 99.7189]},
            {"attivita": "Wat Sorasak", "coordinates": [17.0225, 99.7056]},
            {"attivita": "Sukhothai New Town Market", "coordinates": [17.0072, 99.8262]},
            {"attivita": "Si Satchanalai Historical Park", "coordinates": [17.4314, 99.7856]}
        ],
        "Hua Hin": [
            {"attivita": "Hua Hin Railway Station", "coordinates": [12.5674, 99.9548]},
            {"attivita": "Cicada Market", "coordinates": [12.5342, 99.9657]},
            {"attivita": "Hua Hin Beach", "coordinates": [12.5614, 99.9631]},
            {"attivita": "Wat Khao Takiab", "coordinates": [12.5186, 99.9819]},
            {"attivita": "Hua Hin Night Market", "coordinates": [12.5714, 99.9561]},
            {"attivita": "Vana Nava Water Jungle", "coordinates": [12.5311, 99.9614]},
            {"attivita": "Phraya Nakhon Cave (Ingresso)", "coordinates": [12.2344, 100.0114]},
            {"attivita": "Tamarind Market", "coordinates": [12.5336, 99.9661]},
            {"attivita": "Black Mountain Water Park", "coordinates": [12.6056, 99.8911]},
            {"attivita": "Rajabhakti Park", "coordinates": [12.5011, 99.9658]}
        ],
        "Chiang Rai": [
            {"attivita": "Wat Rong Khun (Tempio Bianco)", "coordinates": [19.8242, 99.7632]},
            {"attivita": "Wat Rong Suea Ten (Tempio Blu)", "coordinates": [19.9232, 99.8418]},
            {"attivita": "Baan Dam Museum (Black House)", "coordinates": [19.9911, 99.8603]},
            {"attivita": "Chiang Rai Clock Tower", "coordinates": [19.9072, 99.8325]},
            {"attivita": "Wat Phra Kaew Chiang Rai", "coordinates": [19.9117, 99.8278]},
            {"attivita": "Chiang Rai Night Bazaar", "coordinates": [19.9064, 99.8336]},
            {"attivita": "Singha Park", "coordinates": [19.8531, 99.7431]},
            {"attivita": "Wat Huay Pla Kang", "coordinates": [19.9486, 99.8042]},
            {"attivita": "Khun Korn Waterfall", "coordinates": [19.8514, 99.6514]},
            {"attivita": "Golden Triangle Viewpoint", "coordinates": [20.3531, 100.0819]}
        ],
        "Koh Tao": [
            {"attivita": "Nang Yuan Island", "coordinates": [10.1174, 99.8142]},
            {"attivita": "Sairee Beach", "coordinates": [10.0967, 99.8272]},
            {"attivita": "Shark Bay", "coordinates": [10.0658, 99.8314]},
            {"attivita": "John-Suwan Viewpoint", "coordinates": [10.0594, 99.8306]},
            {"attivita": "Tanote Bay", "coordinates": [10.0872, 99.8447]},
            {"attivita": "Mango Viewpoint", "coordinates": [10.1114, 99.8286]},
            {"attivita": "Mae Haad Pier", "coordinates": [10.0847, 99.8256]},
            {"attivita": "Freedom Beach Koh Tao", "coordinates": [10.0603, 99.8278]},
            {"attivita": "Ao Hin Wong", "coordinates": [10.1031, 99.8464]},
            {"attivita": "Chalok Baan Kao Bay", "coordinates": [10.0622, 99.8267]}
        ],
        "Kanchanaburi": [
            {"attivita": "The Bridge on the River Kwai", "coordinates": [14.0409, 99.5037]},
            {"attivita": "Erawan National Park", "coordinates": [14.3688, 99.1436]},
            {"attivita": "Death Railway Museum", "coordinates": [14.0319, 99.5256]},
            {"attivita": "Kanchanaburi War Cemetery", "coordinates": [14.0314, 99.5258]},
            {"attivita": "Wat Tham Suea (Tiger Cave Kanchanaburi)", "coordinates": [13.9539, 99.6056]},
            {"attivita": "Hellfire Pass Interpretive Centre", "coordinates": [14.3514, 98.9567]},
            {"attivita": "Mallika City R.E 124", "coordinates": [14.1224, 99.3672]},
            {"attivita": "Sai Yok Noi Waterfall", "coordinates": [14.2411, 99.1436]},
            {"attivita": "Prasat Muang Sing Historical Park", "coordinates": [14.0389, 99.3242]},
            {"attivita": "Chungkai War Cemetery", "coordinates": [14.0094, 99.5144]}
        ]
    }
}