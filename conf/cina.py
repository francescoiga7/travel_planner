# conf/cina.py

CINA_CONFIG = {
    "country_name": "Cina",
    "default_hubs": [
        "Pechino", "Shanghai", "Xi'an", "Guilin", "Chengdu",
        "Hangzhou", "Suzhou", "Guangzhou", "Shenzhen", "Lhasa",
        "Chongqing", "Zhangjiajie"
    ],
    "coordinates": {
        "Pechino": [39.9042, 116.4074],
        "Shanghai": [31.2304, 121.4737],
        "Xi'an": [34.3416, 108.9398],
        "Guilin": [25.2736, 110.2901],
        "Chengdu": [30.5728, 104.0668],
        "Hangzhou": [30.2741, 120.1551],
        "Suzhou": [31.2990, 120.5853],
        "Guangzhou": [23.1291, 113.2644],
        "Shenzhen": [22.5431, 114.0579],
        "Lhasa": [29.6524, 91.1172],
        "Chongqing": [29.5630, 106.5516],
        "Zhangjiajie": [29.1170, 110.4790]
    },
    "escursioni_predefinite": [
        {"hub": "Pechino", "desc": "Escursione alla Grande Muraglia (Mutianyu)", "durata": 480},
        {"hub": "Pechino", "desc": "Visita della Città Proibita e Piazza Tienanmen", "durata": 240},
        {"hub": "Pechino", "desc": "Tour in risciò degli Hutong tradizionali", "durata": 180},
        {"hub": "Xi'an", "desc": "Tour dell'Esercito di Terracotta", "durata": 300},
        {"hub": "Chengdu", "desc": "Visita alla Base di Ricerca dei Panda Giganti", "durata": 240},
        {"hub": "Chengdu", "desc": "Escursione al Buddha Gigante di Leshan", "durata": 420},
        {"hub": "Guilin", "desc": "Crociera sul fiume Li verso Yangshuo", "durata": 360},
        {"hub": "Hangzhou", "desc": "Giro in barca sul Lago dell'Ovest e piantagioni di tè", "durata": 240},
        {"hub": "Suzhou", "desc": "Tour dei Giardini Classici e canali storici", "durata": 300},
        {"hub": "Zhangjiajie", "desc": "Esplorazione delle montagne Avatar (Parco Nazionale)", "durata": 540}
    ],
    "attrazioni": {
        "Pechino": [
            {"attivita": "Forbidden City", "coordinates": [39.9163, 116.3972]},
            {"attivita": "Summer Palace", "coordinates": [39.9998, 116.2755]},
            {"attivita": "Tiananmen Square", "coordinates": [39.9054, 116.3976]},
            {"attivita": "Temple of Heaven", "coordinates": [39.8836, 116.4128]},
            {"attivita": "Great Wall of Badaling (Ingresso)", "coordinates": [40.3611, 116.0122]},
            {"attivita": "Nanluoguxiang (Hutong)", "coordinates": [39.9378, 116.4031]},
            {"attivita": "Jingshan Park", "coordinates": [39.9242, 116.3969]},
            {"attivita": "Olympic Park & Bird's Nest", "coordinates": [39.9928, 116.3964]},
            {"attivita": "Yonghe Lama Temple", "coordinates": [39.9469, 116.4172]},
            {"attivita": "Wangfujing Street", "coordinates": [39.9114, 116.4111]}
        ],
        "Shanghai": [
            {"attivita": "The Bund", "coordinates": [31.2403, 121.4905]},
            {"attivita": "Yu Garden", "coordinates": [31.2272, 121.4922]},
            {"attivita": "Shanghai Tower", "coordinates": [31.2356, 121.5014]},
            {"attivita": "Nanjing Road Shopping Street", "coordinates": [31.2383, 121.4741]},
            {"attivita": "Oriental Pearl TV Tower", "coordinates": [31.2397, 121.4997]},
            {"attivita": "Jade Buddha Temple", "coordinates": [31.2422, 121.4442]},
            {"attivita": "Xintiandi (Historic District)", "coordinates": [31.2214, 121.4756]},
            {"attivita": "Shanghai Museum", "coordinates": [31.2289, 121.4753]},
            {"attivita": "People's Square", "coordinates": [31.2319, 121.4714]},
            {"attivita": "Zhujiajiao Water Town (Ingresso)", "coordinates": [31.1114, 121.0416]}
        ],
        "Xi'an": [
            {"attivita": "Ancient City Wall", "coordinates": [34.2542, 108.9425]},
            {"attivita": "Giant Wild Goose Pagoda", "coordinates": [34.2181, 108.9634]},
            {"attivita": "Terracotta Army Museum", "coordinates": [34.3842, 109.2789]},
            {"attivita": "Muslim Quarter", "coordinates": [34.2636, 108.9386]},
            {"attivita": "Great Mosque of Xi'an", "coordinates": [34.2631, 108.9392]},
            {"attivita": "Bell Tower of Xi'an", "coordinates": [34.2619, 108.9422]},
            {"attivita": "Drum Tower of Xi'an", "coordinates": [34.2614, 108.9392]},
            {"attivita": "Small Wild Goose Pagoda", "coordinates": [34.2406, 108.9419]},
            {"attivita": "Shaanxi History Museum", "coordinates": [34.2253, 108.9536]},
            {"attivita": "Tang Paradise", "coordinates": [34.2131, 108.9731]}
        ],
        "Guilin": [
            {"attivita": "Reed Flute Cave", "coordinates": [25.3061, 110.2662]},
            {"attivita": "Elephant Trunk Hill", "coordinates": [25.2683, 110.2917]},
            {"attivita": "Li River Cruise Pier", "coordinates": [25.2736, 110.2901]},
            {"attivita": "Seven Star Park", "coordinates": [25.2725, 110.3056]},
            {"attivita": "Sun and Moon Twin Pagodas", "coordinates": [25.2722, 110.2936]},
            {"attivita": "Solitary Beauty Peak", "coordinates": [25.2861, 110.2953]},
            {"attivita": "West Street (Yangshuo Area)", "coordinates": [24.7783, 110.4931]},
            {"attivita": "Longji Rice Terraces (Ingresso)", "coordinates": [25.7556, 109.9114]},
            {"attivita": "Yulong River (Snorkeling/Rafting)", "coordinates": [24.7936, 110.4314]},
            {"attivita": "Fubo Hill", "coordinates": [25.2914, 110.2972]}
        ],
        "Chengdu": [
            {"attivita": "Jinli Ancient Street", "coordinates": [30.6481, 104.0494]},
            {"attivita": "Wuhou Shrine", "coordinates": [30.6492, 104.0482]},
            {"attivita": "Chengdu Research Base of Giant Panda", "coordinates": [30.7336, 104.1442]},
            {"attivita": "Wide and Narrow Alleys (Kuanzhai Xiangzi)", "coordinates": [30.6636, 104.0531]},
            {"attivita": "Wenshu Monastery", "coordinates": [30.6728, 104.0714]},
            {"attivita": "Du Fu Thatched Cottage", "coordinates": [30.6603, 104.0289]},
            {"attivita": "People's Park (Renmin Park)", "coordinates": [30.6558, 104.0544]},
            {"attivita": "Chunxi Road Shopping District", "coordinates": [30.6569, 104.0811]},
            {"attivita": "Anshun Bridge", "coordinates": [30.6467, 104.0839]},
            {"attivita": "Sichuan Science and Technology Museum", "coordinates": [30.6594, 104.0653]}
        ],
        "Hangzhou": [
            {"attivita": "West Lake (Xihu)", "coordinates": [30.2458, 120.1456]},
            {"attivita": "Lingyin Temple", "coordinates": [30.2443, 120.0964]},
            {"attivita": "Leifeng Pagoda", "coordinates": [30.2322, 120.1417]},
            {"attivita": "Feilai Peak", "coordinates": [30.2425, 120.0986]},
            {"attivita": "He坊 Street (Hefang Street)", "coordinates": [30.2394, 120.1656]},
            {"attivita": "National Tea Museum", "coordinates": [30.2314, 120.1114]},
            {"attivita": "Longjing Tea Village", "coordinates": [30.2189, 120.1014]},
            {"attivita": "Xixi National Wetland Park", "coordinates": [30.2683, 120.0636]},
            {"attivita": "Liuhe Pagoda (Six Harmonies Pagoda)", "coordinates": [30.1989, 120.1267]},
            {"attivita": "Prince Bay Park", "coordinates": [30.2222, 120.1389]}
        ],
        "Suzhou": [
            {"attivita": "Humble Administrator's Garden", "coordinates": [31.3262, 120.6247]},
            {"attivita": "Shantang Street", "coordinates": [31.3242, 120.5982]},
            {"attivita": "Lingering Garden (Liu Yuan)", "coordinates": [31.3175, 120.5886]},
            {"attivita": "Tiger Hill (Huqiu)", "coordinates": [31.3431, 120.5764]},
            {"attivita": "Master of the Nets Garden", "coordinates": [31.3003, 120.6292]},
            {"attivita": "Pingjiang Road Historic Block", "coordinates": [31.3142, 120.6314]},
            {"attivita": "Suzhou Museum", "coordinates": [31.3256, 120.6231]},
            {"attivita": "Hanshan Temple", "coordinates": [31.3128, 120.5658]},
            {"attivita": "Panmen Gate", "coordinates": [31.2889, 120.6114]},
            {"attivita": "Zhouzhuang Water Town (Area)", "coordinates": [31.1147, 120.8411]}
        ],
        "Guangzhou": [
            {"attivita": "Canton Tower", "coordinates": [23.1065, 113.3245]},
            {"attivita": "Chen Clan Ancestral Hall", "coordinates": [23.1264, 113.2436]},
            {"attivita": "Shamian Island", "coordinates": [23.1089, 113.2386]},
            {"attivita": "Yuexiu Park", "coordinates": [23.1431, 113.2642]},
            {"attivita": "Temple of the Six Banyan Trees", "coordinates": [23.1278, 113.2564]},
            {"attivita": "Guangzhou Museum", "coordinates": [23.1414, 113.2678]},
            {"attivita": "Baiyun Mountain", "coordinates": [23.1783, 113.2964]},
            {"attivita": "Sun Yat-sen Memorial Hall", "coordinates": [23.1342, 113.2656]},
            {"attivita": "Sacred Heart Cathedral", "coordinates": [23.1167, 113.2536]},
            {"attivita": "Chimelong Safari Park", "coordinates": [22.9942, 113.3236]}
        ],
        "Shenzhen": [
            {"attivita": "Windows of the World", "coordinates": [22.5347, 113.9742]},
            {"attivita": "Lianhuashan Park", "coordinates": [22.5539, 114.0564]},
            {"attivita": "Splendid China Folk Village", "coordinates": [22.5314, 113.9911]},
            {"attivita": "Happy Valley Shenzhen", "coordinates": [22.5411, 113.9814]},
            {"attivita": "Dameisha Beach", "coordinates": [22.5956, 114.3056]},
            {"attivita": "Shenzhen Museum", "coordinates": [22.5436, 114.0589]},
            {"attivita": "Ping An Finance Centre (Skydeck)", "coordinates": [22.5331, 114.0553]},
            {"attivita": "OCT Loft Creative Culture Park", "coordinates": [22.5389, 113.9989]},
            {"attivita": "Futian Mangrove Nature Reserve", "coordinates": [22.5161, 114.0089]},
            {"attivita": "Dongmen Pedestrian Street", "coordinates": [22.5489, 114.1189]}
        ],
        "Lhasa": [
            {"attivita": "Potala Palace", "coordinates": [29.6578, 91.1172]},
            {"attivita": "Jokhang Temple & Barkhor Street", "coordinates": [29.6528, 91.1314]},
            {"attivita": "Norbulingka (Summer Palace)", "coordinates": [29.6531, 91.0917]},
            {"attivita": "Sera Monastery", "coordinates": [29.6964, 91.1314]},
            {"attivita": "Drepung Monastery", "coordinates": [29.6761, 91.0489]},
            {"attivita": "Ramoche Temple", "coordinates": [29.6619, 91.1275]},
            {"attivita": "Tibet Museum", "coordinates": [29.6514, 91.0922]},
            {"attivita": "Chagpori Hill (Medicine Mountain)", "coordinates": [29.6542, 91.1114]},
            {"attivita": "Gandain Monastery (Area)", "coordinates": [29.7556, 91.4742]},
            {"attivita": "Lhasa River Promenade", "coordinates": [29.6389, 91.1214]}
        ],
        "Chongqing": [
            {"attivita": "Hongyadong", "coordinates": [29.5651, 106.5794]},
            {"attivita": "Jiefangbei Central Business District", "coordinates": [29.5574, 106.5772]},
            {"attivita": "Ciqikou Ancient Town", "coordinates": [29.5856, 106.4436]},
            {"attivita": "Liziba Station (Monorail in Building)", "coordinates": [29.5528, 106.5114]},
            {"attivita": "Chongqing Zoo", "coordinates": [29.5056, 106.5056]},
            {"attivita": "Three Gorges Museum", "coordinates": [29.5647, 106.5411]},
            {"attivita": "Eling Park", "coordinates": [29.5483, 106.5289]},
            {"attivita": "W隆 Karst National Geology Park (Area)", "coordinates": [29.3314, 107.7856]},
            {"attivita": "Dazu Rock Carvings (Area)", "coordinates": [29.7506, 105.7914]},
            {"attivita": "Raffles City Chongqing", "coordinates": [29.5658, 106.5861]}
        ],
        "Zhangjiajie": [
            {"attivita": "Tianmen Mountain", "coordinates": [29.0504, 110.4789]},
            {"attivita": "Yuanjiajie (Avatar Hallelujah Mountain)", "coordinates": [29.3491, 110.4347]},
            {"attivita": "Zhangjiajie National Forest Park", "coordinates": [29.3174, 110.4790]},
            {"attivita": "Golden Whip Stream", "coordinates": [29.3242, 110.4386]},
            {"attivita": "Tianzi Mountain", "coordinates": [29.3942, 110.4314]},
            {"attivita": "Bailong Elevator", "coordinates": [29.3514, 110.4489]},
            {"attivita": "Zhangjiajie Glass Bridge", "coordinates": [29.3956, 110.6914]},
            {"attivita": "Yellow Dragon Cave (Huanglong Cave)", "coordinates": [29.3414, 110.6124]},
            {"attivita": "Baofeng Lake", "coordinates": [29.3289, 110.5161]},
            {"attivita": "Tujia Folk Customs Park", "coordinates": [29.1242, 110.4856]}
        ]
    }
}