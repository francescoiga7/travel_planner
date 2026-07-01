# conf/usa.py

USA_CONFIG = {
    "country_name": "USA",
    "default_hubs": [
        "New York", "Los Angeles", "Las Vegas", "San Francisco", "Miami",
        "Orlando", "Chicago", "Washington DC", "Seattle", "Boston",
        "Honolulu", "New Orleans"
    ],
    "coordinates": {
        "New York": [40.7128, -74.0060],
        "Los Angeles": [34.0522, -118.2437],
        "Las Vegas": [36.1716, -115.1398],
        "San Francisco": [37.7749, -122.4194],
        "Miami": [25.7617, -80.1918],
        "Orlando": [28.5383, -81.3792],
        "Chicago": [41.8781, -87.6298],
        "Washington DC": [38.9072, -77.0369],
        "Seattle": [47.6062, -122.3321],
        "Boston": [42.3601, -71.0589],
        "Honolulu": [21.3069, -157.8583],
        "New Orleans": [29.9511, -90.0715]
    },
    "escursioni_predefinite": [
        {"hub": "New York", "desc": "Tour della Statua della Libertà ed Ellis Island", "durata": 240},
        {"hub": "New York", "desc": "Osservatorio Empire State Building e Central Park", "durata": 180},
        {"hub": "Las Vegas", "desc": "Escursione in elicottero al Grand Canyon", "durata": 360},
        {"hub": "Las Vegas", "desc": "Tour giornaliero della Death Valley", "durata": 540},
        {"hub": "San Francisco", "desc": "Visita all'Isola di Alcatraz", "durata": 210},
        {"hub": "San Francisco", "desc": "Tour di Muir Woods e degustazione a Napa Valley", "durata": 480},
        {"hub": "Miami", "desc": "Tour in Airboat nelle Everglades", "durata": 300},
        {"hub": "Miami", "desc": "Gita in giornata a Key West", "durata": 660},
        {"hub": "Honolulu", "desc": "Visita storica a Pearl Harbor", "durata": 240},
        {"hub": "Los Angeles", "desc": "Tour degli studi cinematografici Warner Bros", "durata": 180}
    ],
    "attrazioni": {
        "New York": [
            {"attivita": "Times Square", "coordinates": [40.7580, -73.9855]},
            {"attivita": "Central Park", "coordinates": [40.7829, -73.9654]},
            {"attivita": "Empire State Building", "coordinates": [40.7484, -73.9857]},
            {"attivita": "Statue of Liberty", "coordinates": [40.6892, -74.0445]},
            {"attivita": "Metropolitan Museum of Art", "coordinates": [40.7794, -73.9632]},
            {"attivita": "Brooklyn Bridge", "coordinates": [40.7061, -73.9969]},
            {"attivita": "9/11 Memorial & Museum", "coordinates": [40.7115, -74.0131]},
            {"attivita": "High Line", "coordinates": [40.7480, -74.0048]},
            {"attivita": "Top of the Rock", "coordinates": [40.7587, -73.9786]},
            {"attivita": "Grand Central Terminal", "coordinates": [40.7527, -73.9772]}
        ],
        "Los Angeles": [
            {"attivita": "Hollywood Walk of Fame", "coordinates": [34.1016, -118.3268]},
            {"attivita": "Santa Monica Pier", "coordinates": [34.0101, -118.4962]},
            {"attivita": "Griffith Observatory", "coordinates": [34.1184, -118.3004]},
            {"attivita": "Universal Studios Hollywood", "coordinates": [34.1381, -118.3534]},
            {"attivita": "The Getty Center", "coordinates": [34.0768, -118.4741]},
            {"attivita": "LACMA", "coordinates": [34.0639, -118.3592]},
            {"attivita": "Venice Beach Boardwalk", "coordinates": [33.9850, -118.4694]},
            {"attivita": "TCL Chinese Theatre", "coordinates": [34.1020, -118.3411]},
            {"attivita": "Rodeo Drive", "coordinates": [34.0674, -118.4003]},
            {"attivita": "Walt Disney Concert Hall", "coordinates": [34.0553, -118.2498]}
        ],
        "Las Vegas": [
            {"attivita": "The Strip (Las Vegas Boulevard)", "coordinates": [36.1147, -115.1728]},
            {"attivita": "Bellagio Fountains", "coordinates": [36.1126, -115.1767]},
            {"attivita": "Fremont Street Experience", "coordinates": [36.1694, -115.1439]},
            {"attivita": "The High Roller", "coordinates": [36.1174, -115.1681]},
            {"attivita": "Welcome to Fabulous Las Vegas Sign", "coordinates": [36.0820, -115.1728]},
            {"attivita": "The Stratosphere Tower", "coordinates": [36.1475, -115.1556]},
            {"attivita": "The Venetian Gondola Rides", "coordinates": [36.1214, -115.1697]},
            {"attivita": "The Mob Museum", "coordinates": [36.1728, -115.1412]},
            {"attivita": "Neon Museum", "coordinates": [36.1800, -115.1356]},
            {"attivita": "Eiffel Tower Viewing Deck", "coordinates": [36.1122, -115.1725]}
        ],
        "San Francisco": [
            {"attivita": "Golden Gate Bridge", "coordinates": [37.8199, -122.4783]},
            {"attivita": "Fisherman's Wharf & Pier 39", "coordinates": [37.8080, -122.4177]},
            {"attivita": "Alcatraz Island", "coordinates": [37.8267, -122.4230]},
            {"attivita": "Lombard Street", "coordinates": [37.8021, -122.4189]},
            {"attivita": "Golden Gate Park", "coordinates": [37.7694, -122.4862]},
            {"attivita": "Painted Ladies", "coordinates": [37.7763, -122.4328]},
            {"attivita": "Union Square", "coordinates": [37.7879, -122.4074]},
            {"attivita": "Coit Tower", "coordinates": [37.8024, -122.4058]},
            {"attivita": "Chinatown San Francisco", "coordinates": [37.7941, -122.4078]},
            {"attivita": "California Academy of Sciences", "coordinates": [37.7699, -122.4661]}
        ],
        "Miami": [
            {"attivita": "South Beach Art Deco Historic District", "coordinates": [25.7813, -80.1313]},
            {"attivita": "Wynwood Walls", "coordinates": [25.8010, -80.1993]},
            {"attivita": "Vizcaya Museum and Gardens", "coordinates": [25.7444, -80.2106]},
            {"attivita": "Bayside Marketplace", "coordinates": [25.7783, -80.1867]},
            {"attivita": "Little Havana (Calle Ocho)", "coordinates": [25.7658, -80.2203]},
            {"attivita": "Miami Seaquarium", "coordinates": [25.7328, -80.1651]},
            {"attivita": "Crandon Park", "coordinates": [25.7161, -80.1583]},
            {"attivita": "Pérez Art Museum Miami", "coordinates": [25.7858, -80.1856]},
            {"attivita": "Bayfront Park", "coordinates": [25.7747, -80.1856]},
            {"attivita": "Jungle Island", "coordinates": [25.7828, -80.1742]}
        ],
        "Orlando": [
            {"attivita": "Magic Kingdom Park", "coordinates": [28.4178, -81.5812]},
            {"attivita": "Universal Studios Florida", "coordinates": [28.4751, -81.4674]},
            {"attivita": "Epcot", "coordinates": [28.3747, -81.5494]},
            {"attivita": "Disney's Hollywood Studios", "coordinates": [28.3575, -81.5583]},
            {"attivita": "Disney's Animal Kingdom", "coordinates": [28.3528, -81.5906]},
            {"attivita": "Universal's Islands of Adventure", "coordinates": [28.4714, -81.4711]},
            {"attivita": "SeaWorld Orlando", "coordinates": [28.4114, -81.4614]},
            {"attivita": "Icon Park (The Wheel)", "coordinates": [28.4431, -81.4681]},
            {"attivita": "Gatorland", "coordinates": [28.3556, -81.3664]},
            {"attivita": "Discovery Cove", "coordinates": [28.4053, -81.4633]}
        ],
        "Chicago": [
            {"attivita": "Millennium Park & Cloud Gate", "coordinates": [41.8827, -87.6227]},
            {"attivita": "Willis Tower Skydeck", "coordinates": [41.8789, -87.6359]},
            {"attivita": "Navy Pier", "coordinates": [41.8917, -87.6047]},
            {"attivita": "Art Institute of Chicago", "coordinates": [41.8796, -87.6237]},
            {"attivita": "The Magnificent Mile", "coordinates": [41.8958, -87.6242]},
            {"attivita": "Shedd Aquarium", "coordinates": [41.8675, -87.6142]},
            {"attivita": "Field Museum", "coordinates": [41.8661, -87.6169]},
            {"attivita": "Lincoln Park Zoo", "coordinates": [41.9214, -87.6331]},
            {"attivita": "Museum of Science and Industry", "coordinates": [41.7906, -87.5831]},
            {"attivita": "360 Chicago (John Hancock Center)", "coordinates": [41.8989, -87.6231]}
        ],
        "Washington DC": [
            {"attivita": "The White House", "coordinates": [38.8977, -77.0365]},
            {"attivita": "National Mall & Lincoln Memorial", "coordinates": [38.8893, -77.0502]},
            {"attivita": "United States Capitol", "coordinates": [38.8899, -77.0091]},
            {"attivita": "Washington Monument", "coordinates": [38.8895, -77.0353]},
            {"attivita": "National Air and Space Museum", "coordinates": [38.8882, -77.0199]},
            {"attivita": "Smithsonian National Museum of Natural History", "coordinates": [38.8913, -77.0261]},
            {"attivita": "Thomas Jefferson Memorial", "coordinates": [38.8814, -77.0365]},
            {"attivita": "National Gallery of Art", "coordinates": [38.8913, -77.0199]},
            {"attivita": "Library of Congress", "coordinates": [38.8887, -77.0047]},
            {"attivita": "National World War II Memorial", "coordinates": [38.8894, -77.0406]}
        ],
        "Seattle": [
            {"attivita": "Space Needle", "coordinates": [47.6205, -122.3493]},
            {"attivita": "Pike Place Market", "coordinates": [47.6097, -122.3422]},
            {"attivita": "Chihuly Garden and Glass", "coordinates": [47.6206, -122.3503]},
            {"attivita": "Seattle Art Museum", "coordinates": [47.6074, -122.3381]},
            {"attivita": "Museum of Pop Culture (MoPOP)", "coordinates": [47.6214, -122.3481]},
            {"attivita": "Seattle Waterfront", "coordinates": [47.6061, -122.3428]},
            {"attivita": "The Seattle Great Wheel", "coordinates": [47.6062, -122.3436]},
            {"attivita": "Pacific Science Center", "coordinates": [47.6194, -122.3519]},
            {"attivita": "Olympic Sculpture Park", "coordinates": [47.6167, -122.3553]},
            {"attivita": "Woodland Park Zoo", "coordinates": [47.6683, -122.3508]}
        ],
        "Boston": [
            {"attivita": "Freedom Trail", "coordinates": [42.3584, -71.0631]},
            {"attivita": "Fenway Park", "coordinates": [42.3467, -71.0972]},
            {"attivita": "Museum of Fine Arts", "coordinates": [42.3394, -71.0942]},
            {"attivita": "Boston Common", "coordinates": [42.3550, -71.0656]},
            {"attivita": "New England Aquarium", "coordinates": [42.3592, -71.0494]},
            {"attivita": "Faneuil Hall Marketplace", "coordinates": [42.3600, -71.0564]},
            {"attivita": "Museum of Science", "coordinates": [42.3678, -71.0711]},
            {"attivita": "Boston Public Garden", "coordinates": [42.3542, -71.0703]},
            {"attivita": "Skywalk Observatory", "coordinates": [42.3472, -71.0825]},
            {"attivita": "USS Constitution Museum", "coordinates": [42.3725, -71.0567]}
        ],
        "Honolulu": [
            {"attivita": "Waikiki Beach", "coordinates": [21.2764, -157.8282]},
            {"attivita": "Diamond Head State Monument", "coordinates": [21.2620, -157.8062]},
            {"attivita": "Pearl Harbor National Memorial", "coordinates": [21.3649, -157.9494]},
            {"attivita": "Hanauma Bay Nature Preserve", "coordinates": [21.2753, -157.6947]},
            {"attivita": "Iolani Palace", "coordinates": [21.3067, -157.8589]},
            {"attivita": "Honolulu Museum of Art", "coordinates": [21.3044, -157.8486]},
            {"attivita": "Ala Moana Center", "coordinates": [21.2917, -157.8436]},
            {"attivita": "Nuʻuanu Pali Lookout", "coordinates": [21.3675, -157.7931]},
            {"attivita": "Bishop Museum", "coordinates": [21.3328, -157.8711]},
            {"attivita": "Manoa Falls Trail", "coordinates": [21.3425, -157.8014]}
        ],
        "New Orleans": [
            {"attivita": "French Quarter & Bourbon Street", "coordinates": [29.9584, -90.0644]},
            {"attivita": "Jackson Square", "coordinates": [29.9575, -90.0629]},
            {"attivita": "The National WWII Museum", "coordinates": [29.9431, -90.0703]},
            {"attivita": "St. Louis Cathedral", "coordinates": [29.9579, -90.0631]},
            {"attivita": "Garden District", "coordinates": [29.9286, -90.0844]},
            {"attivita": "City Park", "coordinates": [29.9922, -90.0975]},
            {"attivita": "Frenchmen Street", "coordinates": [29.9636, -90.0583]},
            {"attivita": "Audubon Zoo", "coordinates": [29.9242, -90.1339]},
            {"attivita": "Mardi Gras World", "coordinates": [29.9383, -90.0631]},
            {"attivita": "Preservation Hall", "coordinates": [29.9592, -90.0656]}
        ]
    }
}