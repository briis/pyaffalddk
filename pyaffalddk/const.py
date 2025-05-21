"""Constants for the pyaffalddk integration."""
import importlib.resources as pkg_resources  # Python 3.7+
import json

GH_API = b'NDc5RDQwRjQtQjNFMS00MDM4LTkxMzAtNzY0NTMxODhDNzRD'


with pkg_resources.files('pyaffalddk').joinpath('supported_items.json').open('r', encoding='utf-8') as f:
    SUPPORTED_ITEMS = json.load(f)


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
    'Pap bundtet, havebolig',
    'Skal tilmeldes',
    'Storskrald (skal bestilles)',
    'Trærødder og stammer'
]


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

NAME_ARRAY = list(NAME_LIST.keys())
PAR_EXCEPTIONS = ['M/R']
STRIPS = [
        '25 l ', ' 25 l', '140l ', '140 l ', '140 ltr', '190l ', '190 l ', '190 ltr',
        '240l ', '240 l ', '240 l.', '(240 l)', '240 liter', ', 240l', '240 ltr',
        '370 l ', '370 liter ', '400 liter', '660 liter', '660 l ', '770 l ',
        'med 14-dages tømning ved helårshuse', '– tømmes hver 2. uge',
        '14. dags tømning', '14 dages tømning', '14-dags', '14 dags tømning', '14. dage skel', ' 14 dg.', ' 14 dg', '14.dg skel',
        '4. uge Skel', '8. uge skel', ' 4uge',
        'todelt 4 ugers tømning', 'todelt 14 dages tøm', '3 ugers tømning', 'hver 4. uge', '4-ugers', 'hver 6. uge', '2 delt', '2-delt',
        'sommerhustømning', 'henteordning', 'beholder til', ' beh.', '1-kammer ', '2-kammer ', '1-rums', 'to-kammer', 'todelt',
        'egenløsning', 'en-familie', 'enfamiliehus', ' D1 ', ' gl.', '26 tøm', 'sommer 32', 'm. sommertømning', 'villa', 'tømning',
        '-skel 0-2 meter', '- Stand', '- Skel', ' ?', 'uge ', ' beholder',
]
ODD_EVEN_ARRAY = ["lige", "ulige"]
WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag",
            "Torsdag", "Fredag", "Lørdag", "Søndag"]
WEEKDAYS_SHORT = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
