API_URL_DATA = ".renoweb.dk/Legacy/JService.asmx/GetAffaldsplanMateriel_mitAffald"
API_URL_SEARCH = ".renoweb.dk/Legacy/JService.asmx/Adresse_SearchByString"

NON_SUPPORTED_ITEMS = [
    "Asbest",
    "Beholderservice",
    "Bestillerordning",
    "Henteordning for grene",
    "Trærødder og stammer",
    "Ingen tømningsdato fundet!",
    "Skal tilmeldes",
    "Bestil afhentning",
    "Farligt affald (skal bestilles)",
    "Storskrald (skal bestilles)",
    "Haveaffald (skal bestilles)",
    "Beholderudbringning",
]

SUPPORTED_ITEMS = {
    "restaffaldmadaffald": [
        "Restaffald-Madaffald",
        "Rest/mad",
        "Restaffald",
        "Rest - Mad",
        "Rest-/Madaffald",
        "Mad- og restaffald",
        "Mad/rest",
        "Rest-/madaffald",
        "Mad/Rest",
        "Mad og restaffald",
        "Mad-/ og restaffald",
        "Rest / Mad",
        "Rest Mad",
        "Energispand - Obligatorisk min. 1 spand",
        "Rest/madaffald",
        "Energibeholder (mad/rest)",
        "Rest- og Madaffald",
    ],
    "madaffald": [""],
    "batterier": ["Batterier"],
    "dagrenovation": ["Dagrenovation"],
    "elektronik": [""],
    "glas": ["Industri Genbrugeligt"],
    "metalglas": ["Glas og metal", "Metal-Glas", "Glas/Metal", "Metal og Glas"],
    "pappi": [
        "Plast MDK og papir",
        "PAPPI",
        "Plast/MD-karton/PP",
        "Plast/Papir",
        "Papir/Plast og kartoner",
        "Plast og Mad- & drikkekartoner/Papir",
        "Plast, Mad- og drikkekartoner, Småt Pap og Papir",
    ],
    "farligtaffald": [
        "Farligt affald",
        "Miljøkasser",
        "Farligt Affald, Rød boks",
        "Genbrugsbilen",
    ],
    "farligtaffaldmiljoboks": [
        "Farligt affald/Miljøboks",
        "Papir og glas/dåser",
        "Miljøboks",
    ],
    "flis": [
        "Flis",
        "Flishugning",
    ],
    "genbrug": [
        "Genbrug",
        "Genbrugsøer",
        "Genanvendeligt",
        "Genbrug 240 L",
        "Genbrugshal (1 stk.)",
    ],
    "jern": [
        "Jern",
    ],
    "papir": [
        "Papir",
        "Papir 660 L",
    ],
    "papirglasdaaser": [
        "Papir og glas/dåser",
    ],
    "papirmetal": [
        "Papir & Metal",
        "Papir/metal",
        "Metal/papir",
        "Papir og Metal",
    ],
    "pap": [
        "Pap",
    ],
    "plastmetal": [
        "Plast & Metal",
        "Plast, metal & MDK 660L",
        "Plast/ Metal",
        "Plast/MDK/Metal",
        "Plast-metal",
        "Plast/Metal",
        "Plast, Metal, MDK",
    ],
    "restaffald": ["",],
    "storskrald": [
        "Storskrald",
        "Stort elektronik",
        "Storskrald og genbrug",
        "Pap og Storskrald",
    ],
    "storskraldogtekstilaffald": [
        "Storskrald og tekstilaffald",
    ],
    "haveaffald": [
        "Haveaffald, flishugning",
        "Haveaffald",
        "Trærødder og stammer",
        "Haveaffald - Frivilligt",
        "Haveaffald 140 L",
        "Frivillig Haveaffald tømmes fra mandag til onsdag",
    ],
    "papirglas": ["Papir og pap/Glas", "Glas-papir", "Papir, Pap/Glas"],
    "plastmadkarton": [
        "Plast/MDK",
        "Plast & mad- og drikkekartoner",
        "Plast/ Mad- og drikkekartoner",
        "Plast og MDK",
    ],
    "pappapirglasmetal": [
        "Pap, papir, tekstil & metal og glas",
        "4delt beholder",
        "Ressourcebeholder (pap/papir og glas/metal)",
    ],
    "plastmetalmadmdk": [
        "Plast/Metal/Mad- & drikkekartoner",
        "Plast, mad- og drikkekartoner og metal",
    ],
    "plastmdkglasmetal": [],
    "pappapir": ["Pap/Papir", "Papir/Pap", "Papir og Pap"],
    "tekstil": [
        "Tekstiler",
        "Standplads",
        "Tekstilaffald",
        "Miljøkasse/tekstiler",
        "Tekstil",
        "Tekstilposer (1 stk.)",
    ],
    "glasplast": [
        "Glas/Plast og MDK",
    ],
    "plastmetalpapir": [
        "Plast/Metal/Papir ",
        "Genbrugsspand - Obligatorisk min. 1 spand",
    ],
    "plast": ["Plast - Obligatorisk min. 1 spand", "Plast"],
}

NON_MATERIAL_LIST = [
    "Pap bundtet, havebolig (1 stk.)",
]

MATERIAL_LIST = {
    "restaffaldmadaffald": [""],
    "batterier": [
        "Batterier i pose på låg (1 stk.)",
    ],
    "dagrenovation": [
        "240 l. container 1 x ugentligt (12 stk.)",
    ],
    "elektronik": [
        "Småt elektronik i pose på låg (1 stk.)",
    ],
    "glas": [
        "240 L glas (1 stk.)",
        "Glas, 660 liter (2 stk.)",
        "400 liter - Glas - Tømmes hver 8. uge (1 stk.)",
    ],
    "metalglas": [
        "Glas/metal (1 stk.)",
        "240 l Glas/metal Egenløsning (1 stk.)",
        "Metal/Glas 240 l - 2-kammer (1 stk.)",
        "Glas/metal, afstand over 5 meter (1 stk.)",
        "240 L - Metal og Glas (1 stk.)",
        "240 l glas/metal - 4 tømninger (1 stk.)",
        "240 liter - Metal/Glas - tømmes hver 8. uge (1 stk.)",
    ],
    "pappi": [
        "Plast/papir (1 stk.)",
        "370 l Plast+MDK/Papir - Egenløsning (1 stk.)",
        "Papir/Plast og MDK 240 l - 2-kammer (1 stk.)",
        "Plast/papir, afstand over 5 meter (1 stk.)",
        "240 L - Plast og Papir (1 stk.)",
        "240L genbrug (1 stk.)",
        "240 l PMDK/PP 3 ugers tømning (1 stk.)",
        "240 liter - Plast, MDK, papir, pap – tømmes hver 2. uge (1 stk.)",
    ],
    "farligtaffald": [
        "",
    ],
    "farligtaffaldmiljoboks": [
        "Miljøkasse (1 stk.)",
        "Miljøboks",
        "Rød kasse henteordning (1 stk.)",
    ],
    "flis": [""],
    "jern": [
        "240 L metal (1 stk.)",
        "Metal, 660 liter (1 stk.)",
        "240 liter - Metal - Tømmes hver 8. uge (1 stk.)",
    ],
    "genbrug": [
        "Tekstiler",
        "Genbrug",
        "Genbrugsøer",
        "Genanvendeligt",
        "Genbrug 240 L",
        "Genbrugshal (1 stk.)",
    ],
    "papir": [
        "660 L papir (1 stk.)",
        "Papir, 660 liter (3 stk.)",
    ],
    "papirmetal": [
        "Metal og papir 240 L (ejer.kommune) (1 stk.)",
    ],
    "pap": [
        "Pap 240 L (villa) (1 stk.)",
        "240 l Pap Egenløsning (1 stk.)",
        "Pap 240 L (1 stk.)",
        "Pap 240 L (ejer:kommune) (h) (1 stk.)",
        "Pap - 240 l.  (1 stk.)",
        "Indsamling af pap (løst og beholder) (1 stk.)",
        "240 L - Pap - Skel (1 stk.)",
        "Beholder til pap (1 stk.)",
        "770 L pap (1 stk.)",
        "Pap, 660 liter (3 stk.)",
        "400 liter - Pap og papir - Tømmes hver 2. uge (1 stk.)",
    ],
    "plastmetal": [
        "Plast, småt metal & MDK - 240 l. (1 stk.)",
    ],
    "plastmdkglasmetal": [
        "240 L todelt genbrugsspand hver 4. uge (1 stk.)",
        "240L plast, MDK/metal, glas gl. (1 stk.)",
    ],
    "plast": [
        "Plast og MDK 240 L (ejer.kommune) (1 stk.)",
        "Plast, 660 liter (2 stk.)",
    ],
    "storskrald": [
        "Storskrald - fortovsindsamling (1 stk.)",
        "Storskrald (1 stk.)",
        "Storskrald enfamiliehus (1 stk.)",
        "Storskrald",
        "Stort elektronik",
        "Storskrald og genbrug",
        "Pap og Storskrald",
        "Storskrald distrikt 8 (1 stk.)",
    ],
    "storskraldogtekstilaffald": [""],
    "haveaffald": [
        "Gen-Skel 0-2 meter (1 stk.)",
        "Haveaffald henteordning (1 stk.)",
    ],
    "papirglas": [
        "Papir/glas - 240 l. fortovsindsamling (1 stk.)",
    ],
    "plastmadkarton": [
        "Genbrugsbeholder PMDK/MG-240L/3uge (1 stk.)",
        "Genbrug henteordning (1 stk.)",
        "660 L plast, mad- og drikkekartoner (1 stk.)",
        "240 l genbrug - blåt låg (1 stk.)",
        "660 liter - Plast/MDK - Tømmes hver 2. uge (1 stk.)",
    ],
    "papirglasdaaser": [
        "240 L 2-delt Papir/glas-dåser en-familie (1 stk.)",
    ],
    "pappapirglasmetal": [
        "240L metal, glas, plast/papir gl. (1 stk.)",
        "240 l genbrug 2-kammer (2023) (1 stk.)",
        "4-kammer (240 l) (1 stk.)",
        "240 L 2-delt Papir/glas-dåser en-familie (1 stk.)",
        "240 l delt genbrug - grønt låg (1 stk.)",
    ],
    "plastmetalmadmdk": [""],
    "pappapir": [
        "Genbrugsbeholder PP-240L/6uge (1 stk.)",
        "240L papir, pap (1 stk.)",
    ],
    "tekstil": [
        "Tekstil pose (1 stk.)",
        "Tekstilpose tømning (1 stk.)",
        "Tekstilaffald (1 stk.)",
        "Tekstilpose 25 L (1 stk.)",
    ],
    "glasplast": [""],
    "plastmetalpapir": [""],
    "papirglasmetalplast": [
        "4-kammer (370 l) (1 stk.)",
        "Pap og papir/metal, glas og hård plast - 240 L (1 stk.)",
        "240 l genbrug låg i låg (1 stk.)"
    ],
    "madaffald": ["140 L madaffald (1 stk.)",],
    "restaffald": ["9505: 770 L restaffald uge (2 stk.)",],
}

ICON_LIST = {
    "batterier": "mdi:battery",
    "elektronik": "mdi:power-plug",
    "restaffaldmadaffald": "mdi:trash-can",
    "dagrenovation": "mdi:trash-can",
    "glas": "liquor",
    "metalglas": "mdi:glass-fragile",
    "pappi": "mdi:trash-can",
    "farligtaffald": "mdi:recycle",
    "farligtaffaldmiljoboks": "mdi:recycle",
    "flis": "mdi:tree",
    "genbrug": "mdi:recycle",
    "jern": "mdi:bucket",
    "papir": "mdi:file",
    "papirmetal": "mdi:delete-empty",
    "pap": "mdi:note",
    "plastmetal": "mdi:trash-can-outline",
    "storskrald": "mdi:table-furniture",
    "storskraldogtekstilaffald": "mdi:table-furniture",
    "haveaffald": "mdi:leaf",
    "papirglas": "mdi:greenhouse",
    "papirglasmetalplast": "mdi:trash-can",
    "plastmadkarton": "mdi:trash-can",
    "papirglasdaaser": "mdi:trash-can",
    "pappapirglasmetal": "mdi:trash-can",
    "plastmdkglasmetal": "mdi:trash-can",
    "plastmetalmadmdk": "mdi:trash-can",
    "pappapir": "mdi:file",
    "tekstil": "mdi:recycle",
    "glasplast": "mdi:trash-can",
    "plastmetalpapir": "mdi:trash-can",
    "plast": "mdi:trash-can",
    "madaffald": "mdi:trash-can",
    "restaffald": "mdi:trash-can",
}

NAME_LIST = {
    "batterier": "Batterier",
    "elektronik": "Elektronik",
    "dagrenovation": "Dagrenovation",
    "farligtaffald": "Farligt affald",
    "farligtaffaldmiljoboks": "Farligt affald & Miljøboks",
    "flis": "Flis",
    "genbrug": "Genbrug",
    "glas": "Glas",
    "glasplast": "Glas, Plast & Madkartoner",
    "haveaffald": "Haveaffald",
    "jern": "Metal",
    "madaffald": "Madaffald",
    "metalglas": "Metal & Glas",
    "pap": "Pap",
    "papir": "Papir",
    "papirglas": "Papir, Pap & Glas",
    "papirglasdaaser": "Papir, Glas & Dåser",
    "papirglasmetalplast": "Papir, Glas, Metal & Plast",
    "papirmetal": "Papir & Metal",
    "pappapir": "Pap & Papir",
    "pappapirglasmetal": "Pap, Papir, Glas & Metal",
    "pappi": "Papir & Plast",
    "plast": "Plast",
    "plastmadkarton": "Plast & Madkarton",
    "plastmdkglasmetal": "Plast, Madkarton, Glas & Metal",
    "plastmetal": "Plast & Metal",
    "plastmetalmadmdk": "Plast, Metal, Mad & Drikkekartoner",
    "plastmetalpapir": "Plast, Metal & Papir",
    "restaffald": "Restaffald",
    "restaffaldmadaffald": "Rest & Madaffald",
    "storskrald": "Storskrald",
    "storskraldogtekstilaffald": "Storskrald & Tekstilaffald",
    "tekstil": "Tekstilaffald",
}

NAME_ARRAY = list(NAME_LIST.keys())

MUNICIPALITIES_LIST = {
    "Aabenraa": "aabenraa",
    "Aalborg": "aalborg",
    "Albertslund": "albertslund",
    "Allerød": "allerod",
    "Billund": "billund",
    "Brøndby": "brondby",
    "Brønderslev": "bronderslev",
    "Dragør": "dragoer",
    "Egedal": "egedal",
    "Esbjerg": "esbjerg",
    "Faxe": "faxe",
    "Fredensborg": "fredensborg",
    "Frederiksberg": "frederiksberg",
    "Frederikssund": "frederikssund",
    "Gentofte": "gentofte",
    "Gladsaxe": "gladsaxe",
    "Glostrup": "glostrup",
    "Greve": "greve",
    "Gribskov": "gribskov",
    "Halsnæs": "halsnaes",
    "Hedensted": "hedensted",
    "Helsingør": "helsingor",
    "Herlev": "herlev",
    "Hillerød": "hillerod",
    "Hjørring": "hjoerring",
    "Horsens": "horsens",
    "Hvidovre": "hvidovre",
    "Høje-Taastrup": "htk",
    "Hørsholm": "hoersholm",
    "Jammerbugt": "jammerbugt",
    "Kerteminde": "kerteminde",
    "Køge": "koege",
    "Lejre": "lejre",
    "Lyngby-Taarbæk": "ltf",
    "Mariagerfjord": "mariagerfjord",
    "Næstved": "naestved",
    "Odsherred": "odsherred",
    "Randers": "randers",
    "Ringkøbing-Skjern": "rksk",
    "Ringsted": "ringsted",
    "Roskilde": "roskilde",
    "Rudersdal": "rudersdal",
    "Rødovre": "rk",
    "Samsø": "samsoe",
    "Slagelse": "slagelse",
    "Solrød": "solrod",
    "Sorø": "soroe",
    "Stevns": "stevns",
    "Svendborg": "svendborg",
    "Sønderborg": "sonderborg",
    "Tårnby": "taarnby",
    "Varde": "varde",
    "Vejen": "vejen",
    "Vordingborg": "vordingborg",
}

MUNICIPALITIES_ARRAY = list(MUNICIPALITIES_LIST.keys())

WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
WEEKDAYS_SHORT = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
