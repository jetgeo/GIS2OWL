localPath = "C:\\DATA\\GitHub\\jetgeo\\GIS2OWL\\Python\\venv"

proxies = {'http': 'http://proxy.vegvesen.no:8080'}

url = "http://rdfspatial.vegdata.no:7200/repositories/nvdb"
# url = "http://localhost:7200/repositories/nvdb"
nvdbVoPath = "http://rdf.vegdata.no/nvdb/vegobjekt#"
nvdbOTLPath = "http://rdf.vegdata.no/nvdb/nvdb-owl#"


def get_nvdb_ft(vot_id):
    # SPARQL-oppslag på en vegobjekttype
    query = """PREFIX nvdb: <http://rdf.vegdata.no/nvdb/nvdb-owl#>
                SELECT DISTINCT ?uri ?sosinavn
                WHERE {
                ?uri rdfs:subClassOf+ nvdb:Vegobjekttype .
                ?uri nvdb:nvdb_id """ + vot_id + """ .
                ?uri nvdb:sosi_navn ?sosinavn .}"""
    r = requests.get(url, params={"Accept": "application/json", 'query': query}, proxies=proxies)
    return r


def get_nvdb_pt(vot_id):
    # SPARQL-oppslag på egenskapstyper for en objekttype
    query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX nvdb: <http://rdf.vegdata.no/nvdb/nvdb-owl#>
               PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
               SELECT DISTINCT ?uri ?nvdb_id
               WHERE {
                ?class rdfs:subClassOf+ nvdb:Vegobjekttype .
                ?class nvdb:nvdb_id """ + vot_id + """ .
                ?uri rdfs:domain ?class .
                ?uri nvdb:nvdb_id ?nvdb_id .
                }"""
    r = requests.get(url, params = {"Accept": "application/json", 'query': query}, proxies=proxies)
    return r

# Her begynner selve moroa!
import sys, requests
#if not [k for k in sys.path if localPath in k]:
#    print('Føyer', localPath, 'til søkestien')
#    sys.path.append(localPath)
from nvdbapi import nvdbFagdata

# Setter opp søket
sokeobjekt = nvdbFagdata(7)
sokeobjekt.addfilter_geo( {'kommune' : 403 }) # Hamar kommune

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD

# Leser NVDB-ontologien
#gOTL = Graph()
#nvdb_owl = gOTL.parse("https://raw.githubusercontent.com/vegvesen/NVDB-Datakatalogen/master/OWL/nvdb-owl.ttl",format="turtle")

if isinstance(sokeobjekt, nvdbFagdata):

    lagnavn = sokeobjekt.objektTypeDef['navn']

    # Oppslag i NVDB-OTL (SPAQRL) etter uri og navn for objekttypen
    sqres = get_nvdb_ft(str(sokeobjekt.objektTypeDef['id']))

    # Henter ut sosinavn og uri fra resultatet
    for result in sqres.json()["results"]["bindings"]:
        sosinavn = result["sosinavn"]["value"]
        sosinavn.encode(encoding='utf-8', errors='strict')
        uri = result["uri"]["value"]

    classURI = URIRef(uri)
    # Endre objekttypenavn
    print("Setter lagnavn: " + sosinavn + " (" + uri + ")")
    lagnavn = sosinavn

    # Slå opp egenskaps-urier i NVDB-OT (SPARQL)
    sqresEgenskaper = get_nvdb_pt(str(sokeobjekt.objektTypeDef['id']))

    # Initierer graf
    g = Graph()
    nvdb_ns_vo = Namespace(nvdbVoPath)
    nvdb_ns_otl = Namespace(nvdbOTLPath)
    g.bind("nvdb_vo", nvdb_ns_vo)
    g.bind("nvdb_otl",nvdb_ns_otl)

    objektet = sokeobjekt.nesteNvdbFagObjekt()
    count = 0
    while objektet:
        count += 1
        # Legger objektet inn i grafen
        objectURI = URIRef(nvdbVoPath + str(objektet.id))
        g.add((objectURI, RDF.type, classURI))

        # Her kommer prosessering av egenskaper!
        for egenskapen in objektet.egenskaper:
            if not egenskapen['datatype'] in [29,30]:
                print(egenskapen['navn'], " (", egenskapen['id'], ") =", egenskapen['verdi'])
            else:
                print(egenskapen['navn'], " (", egenskapen['id'], ") =", egenskapen['verdi'], " (", egenskapen['enum_id'], ")")

            # Slå opp egenskaps-uri i NVDB-OT (SPARQL)
            uri = ''
            for result in sqresEgenskaper.json()["results"]["bindings"]:
                print(result["nvdb_id"]["value"])
                if int(result["nvdb_id"]["value"]) == int(egenskapen['id']):
                    uri = result["uri"]["value"]
                    #Legger til egenskap i grafen
                    egenskapURI = URIRef(uri)
                    # TODO: Angi korrekt datatype for objektet i grafen
                    g.add((objectURI, egenskapURI, Literal(egenskapen['verdi'])))
                    # TODO: Dersom enum: slå opp enum-URI

        if count % 100 == 0 or count in [1, 10, 20, 50]:
            print('Prosessert ', count, 'av', sokeobjekt.antall, 'NVDB-objekter av objekttypen ', lagnavn)

        objektet = sokeobjekt.nesteNvdbFagObjekt()

    print('Prosessert ', count, 'av', sokeobjekt.antall, 'NVDB-objekter av objekttypen ', lagnavn)

    # Lister grafen
    print(g.serialize(format="turtle").decode())
    # Skriver til fil (turtle)
    g.serialize(destination=localPath + "\\" + lagnavn + ".ttl", format="turtle")

print('Ferdig')
