data = '''0101: København
0147: Frederiksberg
0151: Ballerup
0153: Brøndby
0155: Dragør
0157: Gentofte
0159: Gladsaxe
0161: Glostrup
0163: Herlev
0165: Albertslund
0167: Hvidovre
0169: Høje-Taastrup
0173: Lyngby-Taarbæk
0175: Rødovre
0183: Ishøj
0185: Tårnby
0187: Vallensbæk
0190: Furesø
0201: Allerød
0210: Fredensborg
0217: Helsingør
0219: Hillerød
0223: Hørsholm
0230: Rudersdal
0240: Egedal
0250: Frederikssund
0253: Greve
0259: Køge
0260: Halsnæs
0265: Roskilde
0269: Solrød
0270: Gribskov
0306: Odsherred
0316: Holbæk
0320: Faxe
0326: Kalundborg
0329: Ringsted
0330: Slagelse
0336: Stevns
0340: Sorø
0350: Lejre
0360: Lolland
0370: Næstved
0376: Guldborgsund
0390: Vordingborg
0400: Bornholm
0410: Middelfart
0411: Christiansø
0420: Assens
0430: Faaborg-Midtfyn
0440: Kerteminde
0450: Nyborg
0461: Odense
0479: Svendborg
0480: Nordfyns
0482: Langeland
0492: Ærø
0510: Haderslev
0530: Billund
0540: Sønderborg
0550: Tønder
0561: Esbjerg
0563: Fanø
0573: Varde
0575: Vejen
0580: Aabenraa
0607: Fredericia
0615: Horsens
0621: Kolding
0630: Vejle
0657: Herning
0661: Holstebro
0665: Lemvig
0671: Struer
0706: Syddjurs
0707: Norddjurs
0710: Favrskov
0727: Odder
0730: Randers
0740: Silkeborg
0741: Samsø
0746: Skanderborg
0751: Aarhus
0756: Ikast-Brande
0760: Ringkøbing-Skjern
0766: Hedensted
0773: Morsø
0779: Skive
0787: Thisted
0791: Viborg
0810: Brønderslev
0813: Frederikshavn
0820: Vesthimmerlands
0825: Læsø
0840: Rebild
0846: Mariagerfjord
0849: Jammerbugt
0851: Aalborg
0860: Hjørring'''


MUNICIPALITIES_IDS = {line.split(':')[1].strip().lower(): int(line.split(':')[0]) for line in data.splitlines()}


MUNICIPALITIES_LIST = {
    "Aabenraa": ["aabenraa", "6"],
    "Aalborg": ["aalborg", "6"],
    "Aarhus": ["aarhus", "3"],
    "Albertslund": ["albertslund", "6"],
    "Allerød": ["allerod", "6"],
    "Ballerup": ["ballerup", "5"],
    "Billund": ["billund", "6"],
    "Bornholm": ["bofa", "6"],
    "Brøndby": ["brondby", "6"],
    "Brønderslev": ["bronderslev", "6"],
    "Dragør": ["dragoer", "6"],
    "Egedal": ["egedal", "6"],
    "Esbjerg": ["esbjerg", "6"],
    "Faxe": ["faxe", "5"],
    "Fredensborg": ["fredensborg", "6"],
    "Frederiksberg": ["frederiksberg", "6"],
    "Frederikssund": ["frederikssund", "5"],
    "Gentofte": ["gentofte", "6"],
    "Gladsaxe": ["gladsaxe", "5"],
    "Glostrup": ["glostrup", "6"],
    "Greve": ["greve", "5"],
    "Gribskov": ["gribskov", "5"],
    "Guldborgsund": ["guldborgsund", "5"],
    "Halsnæs": ["halsnaes", "5"],
    "Hedensted": ["hedensted", "6"],
    "Helsingør": ["helsingor", "6"],
    "Herlev": ["herlev", "6"],
    "Hillerød": ["hillerod", "5"],
    "Hjørring": ["hjoerring", "6"],
    "Horsens": ["horsens", "5"],
    "Hvidovre": ["hvidovre", "5"],
    "Høje-Taastrup": ["htk", "5"],
    "Hørsholm": ["hoersholm", "6"],
    "Jammerbugt": ["jammerbugt", "6"],
    "Kalundborg": ["kalundborg", "5"],
    "Kerteminde": ["kerteminde", "6"],
    "København": ["kk", "4"],
    "Køge": ["koege", "5"],
    "Lejre": ["lejre", "6"],
    "Lolland": ["lolland", "5"],
    "Lyngby-Taarbæk": ["ltf", "6"],
    "Mariagerfjord": ["mariagerfjord", "6"],
    "Næstved": ["naestved", "5"],
    "Odense": ["odense", "2"],
    "Odsherred": ["odsherred", "5"],
    "Randers": ["randers", "6"],
    "Ringkøbing-Skjern": ["rksk", "5"],
    "Ringsted": ["ringsted", "6"],
    "Roskilde": ["roskilde", "5"],
    "Rudersdal": ["rudersdal", "6"],
    "Rødovre": ["rk", "6"],
    "Samsø": ["samsoe", "6"],
    "Slagelse": ["slagelse", "5"],
    "Solrød": ["solrod", "6"],
    "Stevns": ["stevns", "5"],
    "Svendborg": ["svendborg", "6"],
    "Sønderborg": ["sonderborg", "6"],
    "Tårnby": ["taarnby", "5"],
    "Varde": ["varde", "6"],
    "Vejen": ["vejen", "5"],
    "Vordingborg": ["vordingborg", "6"],
}


MUNICIPALITIES_ARRAY = list(MUNICIPALITIES_LIST.keys())
