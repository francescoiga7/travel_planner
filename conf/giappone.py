# conf/giappone.py

GIAPPONE_CONFIG = {
    "country_name": "Giappone",
    "default_hubs": [
        "Tokyo", "Kyoto", "Osaka", "Hiroshima", "Nara",
        "Sapporo", "Fukuoka", "Nagoya", "Kanazawa", "Hakone",
        "Takayama", "Okinawa"
    ],
    "coordinates": {
        "Tokyo": [35.6762, 139.6503],
        "Kyoto": [35.0116, 135.7681],
        "Osaka": [34.6937, 135.5023],
        "Hiroshima": [34.3853, 132.4553],
        "Nara": [34.6851, 135.8048],
        "Sapporo": [43.0618, 141.3545],
        "Fukuoka": [33.5904, 130.4017],
        "Nagoya": [35.1815, 136.9066],
        "Kanazawa": [36.5613, 136.6562],
        "Hakone": [35.2324, 139.1069],
        "Takayama": [36.1408, 137.2522],
        "Okinawa": [26.2124, 127.6809]
    },
    "escursioni_predefinite": [
        {"hub": "Tokyo", "desc": "Gita in giornata al Monte Fuji e Hakone", "durata": 600},
        {"hub": "Tokyo", "desc": "Tour del quartiere storico di Asakusa e Akihabara", "durata": 240},
        {"hub": "Kyoto", "desc": "Tour di Arashiyama Bamboo Forest e Kinkaku-ji", "durata": 300},
        {"hub": "Kyoto", "desc": "Camminata sotto i torii del Fushimi Inari", "durata": 180},
        {"hub": "Nara", "desc": "Incontro con i cervi e visita al Tempio Todai-ji", "durata": 180},
        {"hub": "Osaka", "desc": "Street food tour nel distretto di Dotonbori", "durata": 180},
        {"hub": "Hiroshima", "desc": "Visita del Parco della Pace e Isola di Miyajima", "durata": 480},
        {"hub": "Kanazawa", "desc": "Passeggiata nel giardino Kenroku-en e quartiere Samurai", "durata": 240},
        {"hub": "Takayama", "desc": "Escursione al villaggio storico di Shirakawa-go", "durata": 360},
        {"hub": "Okinawa", "desc": "Snorkeling nella Grotta Azzurra", "durata": 180}
    ],
    "attrazioni": {
        "Tokyo": [
            {"attivita": "Senso-ji Temple", "coordinates": [35.7148, 139.7967]},
            {"attivita": "Shibuya Crossing", "coordinates": [35.6595, 139.7005]},
            {"attivita": "Tokyo Skytree", "coordinates": [35.7100, 139.8107]},
            {"attivita": "Meiji Jingu Shrine", "coordinates": [35.6764, 139.6993]},
            {"attivita": "Tsukiji Outer Market", "coordinates": [35.6654, 139.7705]},
            {"attivita": "Shinjuku Gyoen National Garden", "coordinates": [35.6852, 139.7101]},
            {"attivita": "Akihabara Electric Town", "coordinates": [35.6997, 139.7715]},
            {"attivita": "Tokyo Tower", "coordinates": [35.6586, 139.7454]},
            {"attivita": "teamLab Planets", "coordinates": [35.6436, 139.7914]},
            {"attivita": "Imperial Palace East Gardens", "coordinates": [35.6866, 139.7619]}
        ],
        "Kyoto": [
            {"attivita": "Fushimi Inari-Taisha", "coordinates": [34.9671, 135.7727]},
            {"attivita": "Kinkaku-ji (Padiglione d'Oro)", "coordinates": [35.0394, 135.7292]},
            {"attivita": "Kiyomizu-dera", "coordinates": [34.9949, 135.7850]},
            {"attivita": "Arashiyama Bamboo Grove", "coordinates": [35.0156, 135.6714]},
            {"attivita": "Gion District", "coordinates": [35.0036, 135.7781]},
            {"attivita": "Nijo Castle", "coordinates": [35.0142, 135.7481]},
            {"attivita": "Ginkaku-ji (Padiglione d'Argento)", "coordinates": [35.0267, 135.7982]},
            {"attivita": "Philosopher's Path", "coordinates": [35.0244, 135.7961]},
            {"attivita": "Nishiki Market", "coordinates": [35.0050, 135.7649]},
            {"attivita": "Sanjusangen-do", "coordinates": [34.9878, 135.7717]}
        ],
        "Osaka": [
            {"attivita": "Dotonbori", "coordinates": [34.6687, 135.5013]},
            {"attivita": "Osaka Castle", "coordinates": [34.6873, 135.5262]},
            {"attivita": "Universal Studios Japan", "coordinates": [34.6654, 135.4323]},
            {"attivita": "Umeda Sky Building", "coordinates": [34.7053, 135.4903]},
            {"attivita": "Shitenno-ji Temple", "coordinates": [34.6544, 135.5167]},
            {"attivita": "Osaka Aquarium Kaiyukan", "coordinates": [34.6547, 135.4289]},
            {"attivita": "Kuromon Ichiba Market", "coordinates": [34.6658, 135.5072]},
            {"attivita": "Shinsekai & Tsutenkaku Tower", "coordinates": [34.6525, 135.5064]},
            {"attivita": "Sumiyoshi Taisha", "coordinates": [34.6125, 135.4936]},
            {"attivita": "Abeno Harukas", "coordinates": [34.6458, 135.5139]}
        ],
        "Hiroshima": [
            {"attivita": "Hiroshima Peace Memorial Park", "coordinates": [34.3927, 132.4523]},
            {"attivita": "Itsukushima Shrine (Miyajima)", "coordinates": [34.2960, 132.3197]},
            {"attivita": "Atomic Bomb Dome", "coordinates": [34.3947, 132.4547]},
            {"attivita": "Hiroshima Castle", "coordinates": [34.4022, 132.4594]},
            {"attivita": "Shukkei-en Garden", "coordinates": [34.4003, 132.4675]},
            {"attivita": "Hiroshima Peace Memorial Museum", "coordinates": [34.3894, 132.4536]},
            {"attivita": "Mount Misen (Miyajima)", "coordinates": [34.2794, 132.3194]},
            {"attivita": "Okonomimura (Food Mall)", "coordinates": [34.3906, 132.4614]},
            {"attivita": "Mitaki-dera Temple", "coordinates": [34.4186, 132.4372]},
            {"attivita": "Mazda Museum", "coordinates": [34.3611, 132.4844]}
        ],
        "Nara": [
            {"attivita": "Nara Park", "coordinates": [34.6851, 135.8428]},
            {"attivita": "Todai-ji Temple", "coordinates": [34.6889, 135.8398]},
            {"attivita": "Kasuga Taisha Shrine", "coordinates": [34.6814, 135.8483]},
            {"attivita": "Kofuku-ji Temple", "coordinates": [34.6828, 135.8322]},
            {"attivita": "Horyu-ji Temple", "coordinates": [34.6144, 135.7342]},
            {"attivita": "Isui-en Garden", "coordinates": [34.6856, 135.8378]},
            {"attivita": "Naramachi (Historic District)", "coordinates": [34.6781, 135.8286]},
            {"attivita": "Toshodai-ji Temple", "coordinates": [34.6753, 135.7844]},
            {"attivita": "Yakushi-ji Temple", "coordinates": [34.6683, 135.7844]},
            {"attivita": "Mount Wakakusa", "coordinates": [34.6889, 135.8611]}
        ],
        "Sapporo": [
            {"attivita": "Odori Park", "coordinates": [43.0605, 141.3468]},
            {"attivita": "Sapporo Beer Museum", "coordinates": [43.0716, 141.3694]},
            {"attivita": "Susukino District", "coordinates": [43.0556, 141.3536]},
            {"attivita": "Mount Moiwa Ropeway", "coordinates": [43.0242, 141.3233]},
            {"attivita": "Shiroi Koibito Park", "coordinates": [43.0886, 141.2714]},
            {"attivita": "Sapporo Clock Tower", "coordinates": [43.0628, 141.3536]},
            {"attivita": "Hokkaido Shrine", "coordinates": [43.0547, 141.3075]},
            {"attivita": "Moerenuma Park", "coordinates": [43.1214, 141.4256]},
            {"attivita": "Nijo Market", "coordinates": [43.0594, 141.3589]},
            {"attivita": "Hokkaido Museum", "coordinates": [43.0417, 141.5161]}
        ],
        "Fukuoka": [
            {"attivita": "Ohori Park", "coordinates": [33.5859, 130.3764]},
            {"attivita": "Yatai Food Stalls", "coordinates": [33.5932, 130.4081]},
            {"attivita": "Canal City Hakata", "coordinates": [33.5897, 130.4108]},
            {"attivita": "Kushida Shrine", "coordinates": [33.5928, 130.4106]},
            {"attivita": "Fukuoka Tower", "coordinates": [33.5931, 130.3514]},
            {"attivita": "Marine World Uminonakamichi", "coordinates": [33.6619, 130.3644]},
            {"attivita": "Dazaifu Tenmangu (Area)", "coordinates": [33.5214, 130.5342]},
            {"attivita": "Fukuoka Castle Ruins", "coordinates": [33.5872, 130.3831]},
            {"attivita": "Tocho-ji Temple", "coordinates": [33.5950, 130.4139]},
            {"attivita": "Nokonoshima Island Park", "coordinates": [33.6289, 130.3014]}
        ],
        "Nagoya": [
            {"attivita": "Nagoya Castle", "coordinates": [35.1855, 136.8991]},
            {"attivita": "SCMAGLEV and Railway Park", "coordinates": [35.0489, 136.8508]},
            {"attivita": "Atsuta Jingu Shrine", "coordinates": [35.1256, 136.9089]},
            {"attivita": "Osu Kannon Temple & Shopping District", "coordinates": [35.1594, 136.8992]},
            {"attivita": "Toyota Commemorative Museum of Industry", "coordinates": [35.1814, 136.8775]},
            {"attivita": "Nagoya TV Tower (MIRAI TOWER)", "coordinates": [35.1722, 136.9083]},
            {"attivita": "Oasis 21", "coordinates": [35.1714, 136.9106]},
            {"attivita": "Port of Nagoya Public Aquarium", "coordinates": [35.0906, 136.8781]},
            {"attivita": "Higashiyama Zoo and Botanical Gardens", "coordinates": [35.1564, 136.9806]},
            {"attivita": "Noritake Garden", "coordinates": [35.1794, 136.8814]}
        ],
        "Kanazawa": [
            {"attivita": "Kenroku-en Garden", "coordinates": [36.5621, 136.6624]},
            {"attivita": "Higashi Chaya District", "coordinates": [36.5724, 136.6665]},
            {"attivita": "Kanazawa Castle Park", "coordinates": [36.5644, 136.6592]},
            {"attivita": "21st Century Museum of Contemporary Art", "coordinates": [36.5608, 136.6581]},
            {"attivita": "Nagamachi Samurai District", "coordinates": [36.5636, 136.6514]},
            {"attivita": "Omicho Market", "coordinates": [36.5706, 136.6561]},
            {"attivita": "Myoryuji Temple (Ninja Temple)", "coordinates": [36.5514, 136.6489]},
            {"attivita": "Oyama Shrine", "coordinates": [36.5656, 136.6544]},
            {"attivita": "Nishi Chaya District", "coordinates": [36.5564, 136.6472]},
            {"attivita": "Kanazawa Phonograph Museum", "coordinates": [36.5714, 136.6611]}
        ],
        "Hakone": [
            {"attivita": "Lake Ashi", "coordinates": [35.2033, 139.0022]},
            {"attivita": "Hakone Open-Air Museum", "coordinates": [35.2443, 139.0515]},
            {"attivita": "Owakudani Valley", "coordinates": [35.2419, 139.0194]},
            {"attivita": "Hakone Shrine (Torii in water)", "coordinates": [35.2044, 139.0256]},
            {"attivita": "Hakone Ropeway (Sounzan Station)", "coordinates": [35.2458, 139.0378]},
            {"attivita": "Hakone Tozan Railway", "coordinates": [35.2324, 139.1069]},
            {"attivita": "Pola Museum of Art", "coordinates": [35.2556, 139.0242]},
            {"attivita": "Hakone Sekisho (Checkpoint)", "coordinates": [35.1931, 139.0258]},
            {"attivita": "Venetian Glass Museum", "coordinates": [35.2636, 139.0211]},
            {"attivita": "Hakone Yuryo (Onsen)", "coordinates": [35.2344, 139.1014]}
        ],
        "Takayama": [
            {"attivita": "Sanmachi Suji Historic District", "coordinates": [36.1401, 137.2581]},
            {"attivita": "Miyagawa Morning Market", "coordinates": [36.1428, 137.2589]},
            {"attivita": "Takayama Jinya", "coordinates": [36.1394, 137.2575]},
            {"attivita": "Hida Folk Village", "coordinates": [36.1328, 137.2347]},
            {"attivita": "Higashiyama Walking Course", "coordinates": [36.1422, 137.2661]},
            {"attivita": "Sakurayama Hachimangu Shrine", "coordinates": [36.1492, 137.2611]},
            {"attivita": "Takayama Matsuri Yatai Kaikan", "coordinates": [36.1494, 137.2614]},
            {"attivita": "Hida Kokubun-ji Temple", "coordinates": [36.1428, 137.2519]},
            {"attivita": "Shiroyama Park", "coordinates": [36.1364, 137.2644]},
            {"attivita": "Nakabashi Bridge", "coordinates": [36.1403, 137.2586]}
        ],
        "Okinawa": [
            {"attivita": "Okinawa Churaumi Aquarium", "coordinates": [26.6942, 127.8779]},
            {"attivita": "Shuri Castle", "coordinates": [26.2170, 127.7194]},
            {"attivita": "Kokusai Dori Street", "coordinates": [26.2144, 127.6836]},
            {"attivita": "Cape Manzamo", "coordinates": [26.5050, 127.8514]},
            {"attivita": "Okinawa World (Gyokusendo Cave)", "coordinates": [26.1397, 127.7503]},
            {"attivita": "American Village Mihama", "coordinates": [26.3164, 127.7564]},
            {"attivita": "Emerald Beach", "coordinates": [26.7011, 127.8772]},
            {"attivita": "Valley of Gangala", "coordinates": [26.1389, 127.7489]},
            {"attivita": "Makishi Public Market", "coordinates": [26.2128, 127.6883]},
            {"attivita": "Cape Maeda (Blue Grotto)", "coordinates": [26.4442, 127.7719]}
        ]
    }
}