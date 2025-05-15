"""Constants for the pyaffalddk integration."""


GH_API = b'NDc5RDQwRjQtQjNFMS00MDM4LTkxMzAtNzY0NTMxODhDNzRD'


NON_SUPPORTED_ITEMS = [
    'Asbest',
    'Beholderservice',
    'Beholderudbringning',
    'Bestil afhentning',
    'Bestillerordning',
    'Farligt affald (skal bestilles)',
    'Farligt affald - tilmeld',
    'Haveaffald (skal bestilles)',
    'Henteordning for grene',
    'Ingen tømningsdato fundet!',
    'Skal tilmeldes',
    'Storskrald (skal bestilles)',
    'Trærødder og stammer'
]


SUPPORTED_ITEMS = {
    "batterier": ["Batterier"],
    "dagrenovation": ["Dagrenovation"],
    "elektronik": ["Elektronik"],
    "farligtaffald": [
        "Farligt affald",
        "Miljøkasser",
        "Farligt Affald, Rød boks",
        "Genbrugsbilen",
    ],
    "farligtaffaldmiljoboks": [
        "Farligt affald/Miljøboks",
        "Miljøboks",
    ],
    "flis": [
        "Flis",
        "Flishugning",
    ],
    "genbrug": [
        'Genanvendeligt',
        'Genbrug',
        'Genbrug 240 L',
        'Genbrugshal',
        'Genbrugsøer'
    ],
    "glas": [
        "Industri Genbrugeligt",
        "Glas",
    ],
    "glasplast": [
        "Glas/Plast og MDK",
    ],
    "haveaffald": [
        "Haveaff.",
    ],
    "jern": [
        "Jern",
        "Metal",
    ],
    "juletrae": [
        "Juletræ",
    ],
    "madaffald": [
        "Madaffald",
        "Bioposer",
        "Mad",
    ],
    "metalglas": [
        "Glas/Metal",
        "Glas / Metal",
        "Glas og metal",
        "Metal/glas",
        "Metal-Glas",
        "Metal og Glas",
    ],
    "pap": [
        "Pap",
    ],
    "papir": [
        "Papir",
        "Papir 660 L",
        "Papir // Tekstilaffald",
    ],
    "papirglas": [
        "Papir og pap/Glas",
        "Glas-papir",
        "Papir, Pap/Glas",
        "Papir & glas",
    ],
    "papirglasdaaser": [
        "Papir og glas/dåser",
    ],
    "papirmetal": [
        "Papir & Metal",
        "Papir/metal",
        "Metal/papir",
        "Papir og Metal",
        "Pap & metal",
    ],
    "pappapir": [
        "Pap/Papir",
        "Papir/Pap",
        "Papir og Pap",
        "Papir, pap og tekstilaffald",
    ],
    "pappapirglasmetal": [
        "4delt beholder",
        "Genbrug - grønt låg",
        "Grønt låg",
        "Pap, papir, tekstil & metal og glas",
        "Papir/pap og glas/metal",
        "Plast og drikkekarton - Glas og metal",
        "Ressourcebeholder",
    ],
    "pappi": [
        "Papir/Plast og kartoner",
        "Papir- Plast/Mad- og Drikkekartoner",
        "Papir & Pap / Plast & MDK",
        "PAPPI",
        "Plast/MD-karton/PP",
        "Plast/Papir",
        "Plast, Mad- og drikkekartoner, Småt Pap og Papir",
        "Plast & MD-Karton / PP",
        "Plast og Mad- & drikkekartoner/Papir",
        "Plast MDK og papir",
    ],
    "plast": [
        "Plast - Obligatorisk min. 1 spand",
        "Plast",
    ],
    "plastmadkarton": [
        "Plast/MDK",
        "Plast & mad- og drikkekartoner",
        "Plast/ Mad- og drikkekartoner",
        "Plast og MDK",
        "Genbrug - blåt låg",
    ],
    "plastmdkglasmetal": [
        "Plast og drikkekarton – Glas og metal",
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
    "plastmetalmadmdk": [
        "Plast/Metal/Mad- & drikkekartoner",
        "Plast, mad- og drikkekartoner og metal",
    ],
    "plastmetalpapir": [
        "Plast/Metal/Papir",
        "Genbrugsspand - Obligatorisk min. 1 spand",
    ],
    "restaffald": [
        "Industri Restaffald",
        "Restaffald",
        "Restaffald // Batterier og Småt Elektronik",
        "Rest",
    ],
    "restaffaldmadaffald": [
        "Restaffald-Madaffald",
        "Rest/mad",
        "Rest - Mad",
        "Rest-/Madaffald",
        "Mad- og restaffald",
        "Mad/rest",
        "Rest-/madaffald",
        "Mad/Rest",
        "Mad og restaffald",
        "Mad- og restaffald",
        "Mad-/ og restaffald",
        "Rest / Mad",
        "Rest Mad",
        "Energispand - Obligatorisk min. 1 spand",
        "Rest/madaffald",
        "Energibeholder",
        "Rest- og Madaffald",
    ],
    "restplast": [
        "Rest + plast/MDK",
    ],
    "storskrald": [
        "Storskrald",
        "Stort elektronik",
        "Storskrald og genbrug",
        "Pap og Storskrald",
        "Stort indbo og Indendørs træ",
    ],
    "storskraldogtekstilaffald": [
        "Storskrald og tekstilaffald",
    ],
    "tekstil": [
        "Tekstiler",
        "Standplads",
        "Tekstilaffald",
        "Miljøkasse/tekstiler",
        "Tekstil",
        "Tekstilposer",
    ],
}


NON_MATERIAL_LIST = [
    'Pap bundtet, havebolig',
]

MATERIAL_LIST = {
    "batterier": [
        "Batterier i pose på låg",
    ],
    "dagrenovation": [
        "container 1 x ugentligt",
        "Dag",
    ],
    "elektronik": [
        "Småt elektronik i pose på låg",
    ],
    "farligtaffald": [
        "Farligt Affald",
    ],
    "farligtaffaldmiljoboks": [
        "Miljøboks",
        "Miljøkasse",
        "Miljøskab",
        "Rød kasse",
        "Rød miljøboks",
    ],
    "flis": [
    ],
    "genbrug": [
        "Gen",
        "Gen-Skel",
        "Genanvendeligt",
        "Genbrug",
        "Genbrug 240 l",
        "Genbrugshal",
        "Genbrugsøer",
    ],
    "glas": [
        "Cube 1500 L",
        "Glas",
    ],
    "glasplast": [
    ],
    "haveaffald": [
        "Have",
        "Haveaffald",
        "Havespand",
    ],
    "jern": [
        "Metal",
    ],
    "juletrae": [
        "Juletræ",
        "Juletræer",
    ],
    "madaffald": [
        "Madaffald",
        "Mad",
    ],
    "metalglas": [
        "Glas/Metal",
        "glas & metal",
        "Metal og Glas",
        "Glas/metal, afstand over 5 meter",
        "Metal/glas",
    ],
    "pap": [
        "Pap og papir",
        "Beholder til pap",
        "Indsamling af pap",
        "Pap",
        "Papbeholder",
    ],
    "papir": [
        "Papir",
    ],
    "papirglas": [
        "Papir/glas",
        "Papir og Glas",
        "Papir og pap/Glas",
    ],
    "papirglasdaaser": [
        "Papir/glas-dåser",
    ],
    "papirglasmetalplast": [
        'genbrug låg i låg',
        '4-kammer',
        'Pap og papir/metal, glas og hård plast',
        'plast/metal/drikkekartoner og papir/pap',
        'plast/metal/MDK/papir/pap',
    ],
    "papirmetal": [
        "Metal og papir",
    ],
    "pappapir": [
        "papir, pap",
        "Genbrugsbeholder PP-240L/6",
        "pap/papir",
        "papir/pap",
        "Papir/Papspand",
    ],
    "pappapirglasmetal": [
        "Genbrug - grønt låg",
        'glas/metal og pap/papir',
        'Glas & metal og papir & småt pap',
        "Grønt låg",
        'metal, glas, plast/papir',
        'pap, papir, tekstil & metal og glas',
        'papir/pap + glas/metal',
    ],
    "pappi": [
        'Papir & småt pap',
        'papir/plast og kartoner',
        'Papir/Plast og MDK',
        'Plast/papir',
        'Plast/papir, afstand over 5 meter',
        'Plast+MDK/Papir',
        'Plast, MDK, papir, pap',
        'plast og mad- & drikkekartoner/papir',
        'Plast og Papir',
        'PMDK/PP',
        'PP/MDK-plast',
    ],
    "plast": [
        "Plast",
        "Plastaffald",
    ],
    "plastmadkarton": [
        "blåt låg",
        "Genbrugsbeholder PMDK/MG-240L/3",
        "Genbrug henteordning",
        "Mad- og drikkekartoner",
        "plast, mad- og drikkekartoner",
        "Plast/MDK",
        "Plast og MDK",
        'plast & mad- og drikkekartoner',
        "Plast og mad- & drikkekartoner",
        "PMD",
    ],
    "plastmetal": [
        "Metal og Plast",
        "Plast, småt metal & MDK",
        "Plast/Metal",
    ],
    "plastmetalmadmdk": [
    ],
    "plastmetalpapir": [
        "grøn",
    ],
    "plastmdkglasmetal": [
        "Genbrugsbeholder",
        "genbrugsspand",
        "plast, MDK/metal, glas",
    ],
    "restaffald": [
        "rest",
        "Restaffald",
    ],
    "restaffaldmadaffald": [
        "(M/R)",
        "energi",
        "Mad- og restaffald",
        "mad/rest",
        "mad/restaffald",
        "Rest/Mad",
        "rest/madaffald",
        "Restaffald/Madaffald",
        "Rest og Mad",
        "rød",
        "skraldespand",
    ],
    "restplast": [
        "Rest + plast/MDK",
    ],
    "storskrald": [
        "Elektronik, stort metal, keramik og porcelæn",
        "Møbler/indbo",
        "Pap og Storskrald",
        "Småt brændbart",
        "Storskrald",
        "Storskrald og genbrug",
        "Stort elektronik",
    ],
    "storskraldogtekstilaffald": [
    ],
    "tekstil": [
        "Tekstil pose",
        "Tekstilaffald",
        "Tekstilpose",
        "Tekstiler",
    ],
}

SPECIAL_MATERIALS = {
    '240 l genbrug 2-kammer': 'pappapirglasmetal',
    'haveaffald': 'haveaffald',
    '4-kammer (370 l)': 'papirglasmetalplast',
    '4-kammer (240 l)': 'pappapirglasmetal',
    '240L genbrug': 'pappi',
    'genbrug - blåt låg': 'plastmadkarton',
    'Genbrug henteordning': 'plastmadkarton',
}


ICON_LIST = {
    "batterier": "mdi:battery",
    "dagrenovation": "mdi:trash-can",
    "elektronik": "mdi:power-plug",
    "farligtaffald": "mdi:recycle",
    "farligtaffaldmiljoboks": "mdi:recycle",
    "flis": "mdi:tree",
    "genbrug": "mdi:recycle",
    "glas": "mdi:bottle-soda",
    "glasplast": "mdi:trash-can",
    "haveaffald": "mdi:leaf",
    "jern": "mdi:bucket",
    "juletrae": "mdi:pine-tree",
    "madaffald": "mdi:trash-can",
    "metal": "mdi:anvil",
    "metalglas": "mdi:glass-fragile",
    "pap": "mdi:note",
    "pappapir": "mdi:file",
    "pappapirglasmetal": "mdi:trash-can",
    "pappi": "mdi:trash-can",
    "papir": "mdi:file",
    "papirglas": "mdi:greenhouse",
    "papirglasdaaser": "mdi:trash-can",
    "papirglasmetalplast": "mdi:trash-can",
    "papirmetal": "mdi:delete-empty",
    "plast": "mdi:trash-can",
    "plastmadkarton": "mdi:trash-can",
    "plastmdkglasmetal": "mdi:trash-can",
    "plastmetal": "mdi:trash-can-outline",
    "plastmetalmadmdk": "mdi:trash-can",
    "plastmetalpapir": "mdi:trash-can",
    "restaffald": "mdi:trash-can",
    "restaffaldmadaffald": "mdi:trash-can",
    "restplast": "mdi:trash-can",
    "storskrald": "mdi:table-furniture",
    "storskraldogtekstilaffald": "mdi:table-furniture",
    "tekstil": "mdi:recycle",
}

NAME_LIST = {
    "batterier": "Batterier",
    "bioposer": "Bioposer",
    "dagrenovation": "Dagrenovation",
    "elektronik": "Elektronik",
    "farligtaffald": "Farligt affald",
    "farligtaffaldmiljoboks": "Farligt affald & Miljøboks",
    "flis": "Flis",
    "genbrug": "Genbrug",
    "glas": "Glas",
    "glasplast": "Glas, Plast & Madkartoner",
    "haveaffald": "Haveaffald",
    "jern": "Metal",
    "juletrae": "Juletræer",
    "madaffald": "Madaffald",
    "metal": "Metal",
    "metalglas": "Metal & Glas",
    "pap": "Pap",
    "pappapir": "Pap & Papir",
    "pappapirglasmetal": "Pap, Papir, Glas & Metal",
    "pappi": "Papir & Plast",
    "papir": "Papir",
    "papirglas": "Papir, Pap & Glas",
    "papirglasdaaser": "Papir, Glas & Dåser",
    "papirglasmetalplast": "Papir, Glas, Metal & Plast",
    "papirmetal": "Papir & Metal",
    "plast": "Plast",
    "plastmadkarton": "Plast & Madkarton",
    "plastmdkglasmetal": "Plast, Madkarton, Glas & Metal",
    "plastmetal": "Plast & Metal",
    "plastmetalmadmdk": "Plast, Metal, Mad & Drikkekartoner",
    "plastmetalpapir": "Plast, Metal & Papir",
    "restaffald": "Restaffald",
    "restaffaldmadaffald": "Rest & Madaffald",
    "restplast": "Restaffald & Plast/Madkartoner",
    "storskrald": "Storskrald",
    "storskraldogtekstilaffald": "Storskrald & Tekstilaffald",
    "tekstil": "Tekstilaffald",
}

SUPPORTED_ITEMS2 = {key: [] for key in NAME_LIST}
for key, vals in SUPPORTED_ITEMS2.items():
    vals += SUPPORTED_ITEMS.get(key, [])
    vals += MATERIAL_LIST.get(key, [])

NAME_ARRAY = list(NAME_LIST.keys())
PAR_EXCEPTIONS = ['M/R']
STRIPS = [
        '25 l ', '140l ', '140 l ', '190l ', '190 l ', '190 ltr',
        '240l ', '240 l ', '240 l.', '(240 l)', '240 liter', ', 240l', ' 240 ltr',
        '370 l ', '370 liter ', '400 liter', '660 liter', '660 l ', '770 l ',
        'med 14-dages tømning ved helårshuse', '– tømmes hver 2. uge',
        '14. dags tømning', '14 dages tømning', '14-dags', '14 dags tømning', '14. dage skel', ' 14 dg',
        'todelt 4 ugers tømning', 'todelt 14 dages tøm', '3 ugers tømning', 'hver 4. uge', '4-ugers', 'hver 6. uge', '2 delt', '2-delt',
        'sommerhustømning', 'henteordning', 'beholder til', ' beh.', '1-kammer ', '2-kammer ', '1-rums', 'to-kammer', 'todelt',
        'egenløsning', 'en-familie', 'enfamiliehus', ' D1 ', ' gl.', 'sommer 32', 'm. sommertømning', 'villa', 'tømning',
        '-skel 0-2 meter', '- Stand', '- Skel', ' ?', 'uge ',
]
ODD_EVEN_ARRAY = ["lige", "ulige"]
WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag",
            "Torsdag", "Fredag", "Lørdag", "Søndag"]
WEEKDAYS_SHORT = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
