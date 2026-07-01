# conf/indonesia.py

INDONESIA_CONFIG = {
    "country_name": "Indonesia",
    "default_hubs": [
        "Jakarta", "Yogyakarta", "Denpasar", "Komodo Island", "Ubud",
        "Lombok", "Medan", "Bandung", "Surabaya", "Makassar",
        "Manado", "Raja Ampat"
    ],
    "coordinates": {
        "Jakarta": [-6.2088, 106.8456],
        "Yogyakarta": [-7.7956, 110.3695],
        "Denpasar": [-8.6705, 115.2126],
        "Komodo Island": [-8.5911, 119.4442],
        "Ubud": [-8.5069, 115.2625],
        "Lombok": [-8.6500, 116.3500],
        "Medan": [3.5952, 98.6722],
        "Bandung": [-6.9175, 107.6191],
        "Surabaya": [-7.2575, 112.7521],
        "Makassar": [-5.1476, 119.4327],
        "Manado": [1.4748, 124.8428],
        "Raja Ampat": [-0.4262, 130.8656]
    },
    "escursioni_predefinite": [
        {"hub": "Yogyakarta", "desc": "Alba al Tempio di Borobudur", "durata": 240},
        {"hub": "Yogyakarta", "desc": "Visita al Tempio di Prambanan", "durata": 180},
        {"hub": "Denpasar", "desc": "Tour di un giorno a Nusa Penida", "durata": 540},
        {"hub": "Komodo Island", "desc": "Trekking e avvistamento Draghi di Komodo", "durata": 420},
        {"hub": "Ubud", "desc": "Tour delle risaie di Tegalalang e Foresta delle Scimmie", "durata": 300},
        {"hub": "Ubud", "desc": "Trekking all'alba sul Monte Batur", "durata": 360},
        {"hub": "Surabaya", "desc": "Escursione al vulcano Monte Bromo", "durata": 480},
        {"hub": "Surabaya", "desc": "Trekking notturno al cratere Ijen (Blue Fire)", "durata": 540},
        {"hub": "Lombok", "desc": "Snorkeling e tour delle isole Gili", "durata": 420},
        {"hub": "Raja Ampat", "desc": "Esplorazione marina e snorkeling guidato", "durata": 480}
    ],
    "attrazioni": {
        "Jakarta": [
            {"attivita": "Monas (Monumento Nazionale)", "coordinates": [-6.1754, 106.8272]},
            {"attivita": "Istiqlal Mosque", "coordinates": [-6.1702, 106.8314]},
            {"attivita": "Jakarta Old Town (Kota Tua)", "coordinates": [-6.1376, 106.8125]},
            {"attivita": "Taman Mini Indonesia Indah", "coordinates": [-6.3024, 106.8951]},
            {"attivita": "Ancol Dreamland", "coordinates": [-6.1247, 106.8422]},
            {"attivita": "Gereja Katedral Jakarta", "coordinates": [-6.1694, 106.8331]},
            {"attivita": "National Museum of Indonesia", "coordinates": [-6.1761, 106.8219]},
            {"attivita": "Sunda Kelapa Harbour", "coordinates": [-6.1228, 106.8086]},
            {"attivita": "Plaza Indonesia", "coordinates": [-6.1919, 106.8228]},
            {"attivita": "Ragunan Zoo", "coordinates": [-6.3124, 106.8203]}
        ],
        "Yogyakarta": [
            {"attivita": "Kraton Ngayogyakarta Hadiningrat", "coordinates": [-7.8053, 110.3642]},
            {"attivita": "Taman Sari", "coordinates": [-7.8101, 110.3592]},
            {"attivita": "Jalan Malioboro", "coordinates": [-7.7925, 110.3658]},
            {"attivita": "Fort Vredeburg Museum", "coordinates": [-7.8003, 110.3664]},
            {"attivita": "Pasar Beringharjo", "coordinates": [-7.7989, 110.3661]},
            {"attivita": "Sonobudoyo Museum", "coordinates": [-7.8025, 110.3639]},
            {"attivita": "Affandi Museum", "coordinates": [-7.7828, 110.3964]},
            {"attivita": "Alun-Alun Kidul", "coordinates": [-7.8119, 110.3631]},
            {"attivita": "Tugu Yogyakarta", "coordinates": [-7.7828, 110.3672]},
            {"attivita": "Sleman City Hall (Area)", "coordinates": [-7.7125, 110.3614]}
        ],
        "Denpasar": [
            {"attivita": "Bajra Sandhi Monument", "coordinates": [-8.6717, 115.2339]},
            {"attivita": "Pura Jagatnatha", "coordinates": [-8.6576, 115.2183]},
            {"attivita": "Sanur Beach", "coordinates": [-8.6756, 115.2642]},
            {"attivita": "Bali Museum", "coordinates": [-8.6578, 115.2189]},
            {"attivita": "Pasar Badung", "coordinates": [-8.6572, 115.2114]},
            {"attivita": "Pura Maospahit", "coordinates": [-8.6531, 115.2106]},
            {"attivita": "Art Center Denpasar (Taman Werdhi Budaya)", "coordinates": [-8.6569, 115.2353]},
            {"attivita": "Serangan Island (Turtle Conservation)", "coordinates": [-8.7236, 115.2314]},
            {"attivita": "Sindhu Night Market", "coordinates": [-8.6836, 115.2589]},
            {"attivita": "Shark Island Bali", "coordinates": [-8.7291, 115.2411]}
        ],
        "Komodo Island": [
            {"attivita": "Pink Beach", "coordinates": [-8.6015, 119.5168]},
            {"attivita": "Loh Liang", "coordinates": [-8.5775, 119.5036]},
            {"attivita": "Padar Island Viewpoint", "coordinates": [-8.6514, 119.4319]},
            {"attivita": "Manta Point", "coordinates": [-8.5328, 119.4892]},
            {"attivita": "Kanawa Island", "coordinates": [-8.4967, 119.7564]},
            {"attivita": "Taka Makassar", "coordinates": [-8.5472, 119.5114]},
            {"attivita": "Rinca Island (Loh Buaya)", "coordinates": [-8.6558, 119.7128]},
            {"attivita": "Gili Lawa Darat", "coordinates": [-8.4514, 119.4386]},
            {"attivita": "Batu Bolong Reef", "coordinates": [-8.5022, 119.4611]},
            {"attivita": "Kalong Island (Flying Foxes)", "coordinates": [-8.6083, 119.6014]}
        ],
        "Ubud": [
            {"attivita": "Sacred Monkey Forest Sanctuary", "coordinates": [-8.5194, 115.2606]},
            {"attivita": "Ubud Palace (Puri Saren Agung)", "coordinates": [-8.5068, 115.2625]},
            {"attivita": "Tegalalang Rice Terrace", "coordinates": [-8.4314, 115.2789]},
            {"attivita": "Campuhan Ridge Walk", "coordinates": [-8.5036, 115.2547]},
            {"attivita": "Ubud Art Market", "coordinates": [-8.5072, 115.2628]},
            {"attivita": "Pura Taman Saraswati", "coordinates": [-8.5061, 115.2614]},
            {"attivita": "Goa Gajah (Elephant Cave)", "coordinates": [-8.5233, 115.2861]},
            {"attivita": "Agung Rai Museum of Art (ARMA)", "coordinates": [-8.5219, 115.2644]},
            {"attivita": "Blanco Renaissance Museum", "coordinates": [-8.5042, 115.2508]},
            {"attivita": "Tegenungan Waterfall", "coordinates": [-8.5753, 115.2811]}
        ],
        "Lombok": [
            {"attivita": "Senggigi Beach", "coordinates": [-8.5015, 116.0416]},
            {"attivita": "Kuta Beach Lombok", "coordinates": [-8.8931, 116.2814]},
            {"attivita": "Mount Rinjani (National Park)", "coordinates": [-8.4114, 116.4572]},
            {"attivita": "Sendang Nile Waterfall", "coordinates": [-8.2736, 116.4114]},
            {"attivita": "Tanjung Aan Beach", "coordinates": [-8.9114, 116.3192]},
            {"attivita": "Sade Traditional Sasak Village", "coordinates": [-8.8394, 116.2917]},
            {"attivita": "Pura Batu Bolong", "coordinates": [-8.5094, 116.0361]},
            {"attivita": "Tiu Kelep Waterfall", "coordinates": [-8.2789, 116.4056]},
            {"attivita": "Selong Belanak Beach", "coordinates": [-8.8711, 116.1614]},
            {"attivita": "Gili Trawangan Ferry Terminal", "coordinates": [-8.3514, 116.0422]}
        ],
        "Medan": [
            {"attivita": "Istana Maimun", "coordinates": [3.5751, 98.6839]},
            {"attivita": "Great Mosque of Medan", "coordinates": [3.5746, 98.6872]},
            {"attivita": "Tjong A Fie Mansion", "coordinates": [3.5861, 98.6792]},
            {"attivita": "Graha Maria Annai Velangkanni", "coordinates": [3.5514, 98.6089]},
            {"attivita": "Rahmat International Wildlife Museum", "coordinates": [3.5786, 98.6614]},
            {"attivita": "Maha Vihara Maitreya", "coordinates": [3.6264, 98.6914]},
            {"attivita": "Merdeka Walk", "coordinates": [3.5914, 98.6761]},
            {"attivita": "Sri Mariamman Temple", "coordinates": [3.5853, 98.6711]},
            {"attivita": "Asam Kumbang Crocodile Farm", "coordinates": [3.5414, 98.6036]},
            {"attivita": "Medan Mall", "coordinates": [3.5903, 98.6853]}
        ],
        "Bandung": [
            {"attivita": "Kawah Putih", "coordinates": [-7.1662, 107.4021]},
            {"attivita": "Gedung Sate", "coordinates": [-6.9025, 107.6187]},
            {"attivita": "Tangkuban Perahu", "coordinates": [-6.7594, 107.6097]},
            {"attivita": "Jalan Braga", "coordinates": [-6.9178, 107.6092]},
            {"attivita": "Saung Angklung Udjo", "coordinates": [-6.8978, 107.6551]},
            {"attivita": "Floating Market Lembang", "coordinates": [-6.8189, 107.6178]},
            {"attivita": "Dago Dream Park", "coordinates": [-6.8472, 107.6256]},
            {"attivita": "Farmhouse Bandung", "coordinates": [-6.8328, 107.6044]},
            {"attivita": "Tebing Keraton", "coordinates": [-6.8344, 107.6636]},
            {"attivita": "Trans Studio Bandung", "coordinates": [-6.9250, 107.6364]}
        ],
        "Surabaya": [
            {"attivita": "House of Sampoerna", "coordinates": [-7.2307, 112.7342]},
            {"attivita": "Suramadu Bridge", "coordinates": [-7.1901, 112.7792]},
            {"attivita": "Submarine Monument (Monkasel)", "coordinates": [-7.2656, 112.7503]},
            {"attivita": "Heroes Monument (Tugu Pahlawan)", "coordinates": [-7.2436, 112.7378]},
            {"attivita": "Surabaya Zoo", "coordinates": [-7.2956, 112.7364]},
            {"attivita": "Bungkul Park", "coordinates": [-7.2886, 112.7383]},
            {"attivita": "Ciputra Waterpark", "coordinates": [-7.2847, 112.6314]},
            {"attivita": "Sanggar Agung Temple", "coordinates": [-7.2483, 112.7889]},
            {"attivita": "Klenteng Hong Tiek Hian", "coordinates": [-7.2344, 112.7431]},
            {"attivita": "Tunjungan Plaza", "coordinates": [-7.2619, 112.7386]}
        ],
        "Makassar": [
            {"attivita": "Fort Rotterdam", "coordinates": [-5.1339, 119.4047]},
            {"attivita": "Losari Beach", "coordinates": [-5.1444, 119.4082]},
            {"attivita": "Trans Studio Mall Makassar", "coordinates": [-5.1589, 119.3892]},
            {"attivita": "Bantimurung Bulusaraung National Park", "coordinates": [-5.0136, 119.6842]},
            {"attivita": "Paotere Harbour", "coordinates": [-5.1067, 119.4128]},
            {"attivita": "Samalona Island", "coordinates": [-5.1242, 119.3436]},
            {"attivita": "Somba Opu Shopping Street", "coordinates": [-5.1411, 119.4094]},
            {"attivita": "Great Mosque of Makassar", "coordinates": [-5.1278, 119.4219]},
            {"attivita": "Kodingareng Keke Island", "coordinates": [-5.1014, 119.2614]},
            {"attivita": "Fort Somba Opu", "coordinates": [-5.1889, 119.4011]}
        ],
        "Manado": [
            {"attivita": "Bunaken National Marine Park", "coordinates": [1.6156, 124.7431]},
            {"attivita": "Jesus Blesses Statue", "coordinates": [1.4247, 124.8436]},
            {"attivita": "Manado Boulevard", "coordinates": [1.4789, 124.8256]},
            {"attivita": "Lake Linow", "coordinates": [1.2725, 124.8214]},
            {"attivita": "Mount Lokon", "coordinates": [1.3578, 124.7931]},
            {"attivita": "Tangkoko Nature Reserve", "coordinates": [1.5114, 125.1589]},
            {"attivita": "Siladen Island", "coordinates": [1.6311, 124.8014]},
            {"attivita": "Ban Hin Kiong Temple", "coordinates": [1.4931, 124.8419]},
            {"attivita": "Malalayang Beach", "coordinates": [1.4514, 124.8089]},
            {"attivita": "Paal Beach", "coordinates": [1.4328, 125.0414]}
        ],
        "Raja Ampat": [
            {"attivita": "Piaynemo", "coordinates": [-0.5637, 130.2721]},
            {"attivita": "Misool Island", "coordinates": [-1.8833, 130.1333]},
            {"attivita": "Wayag Island", "coordinates": [0.1872, 130.0347]},
            {"attivita": "Arborek Tourism Village", "coordinates": [-0.5658, 130.5186]},
            {"attivita": "Friwen Wall", "coordinates": [-0.4856, 130.6722]},
            {"attivita": "Pasir Timbul", "coordinates": [-0.4356, 130.6811]},
            {"attivita": "Sawinggrai Village", "coordinates": [-0.4342, 130.5342]},
            {"attivita": "Kri Island Reef", "coordinates": [-0.5514, 130.6436]},
            {"attivita": "Batu Pensil (Kabui Bay)", "coordinates": [-0.3614, 130.5489]},
            {"attivita": "Batanta Waterfall", "coordinates": [-0.8514, 130.6124]}
        ]
    }
}