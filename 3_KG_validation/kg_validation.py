from rdflib import Graph, Namespace, URIRef
from collections import defaultdict
import matplotlib.pyplot as plt

# Load the RDF data from ontox_kg.ttl
g = Graph()
g.parse("../2_kg_population/ontox_kg.ttl", format="turtle")

# Namespaces
# Define namespaces for your prefixes
base = "https://w3id.org/ontox#"
dc = Namespace("http://purl.org/dc/elements/1.1/")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/dul.owl#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
frbr = Namespace("http://purl.org/vocab/frbr/core#")
fschema = Namespace("https://w3id.org/framester/schema/")
odang = Namespace("https://purl.archive.org/o-dang#")
ontolex = Namespace("http://www.w3.org/ns/lemon/ontolex#")
ontox = Namespace("https://w3id.org/ontox#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
terms = Namespace("http://purl.org/dc/terms/")
wiki = Namespace("http://www.wikidata.org/entity/")
wn = Namespace("https://w3id.org/framester/wn/wn30/schema/")
wninst = Namespace("https://w3id.org/framester/wn/wn30/instances/")
xml = Namespace("http://www.w3.org/XML/1998/namespace")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Count triples
num_triples = len(g)

# Count triples

# SPARQL query to check symbols without symbol descriptions
query_symbols_without_description = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol ontox:hasSymbolDescription ?description .
    }
} LIMIT 10
"""

# SPARQL query to check symbols without original title (rdfs:label)
query_symbols_without_label = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol rdfs:label ?label .
    }
} LIMIT 10
"""

# SPARQL query to check symbols with symbol descriptions missing textual labels
query_symbols_with_description_without_label = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    ?symbol ontox:hasSymbolDescription ?description .
    ?description rdf:type ontox:SymbolDescription .
    FILTER NOT EXISTS {
        ?description rdfs:label ?label .
    }
} LIMIT 10
"""

# SPARQL query to verify symbols without original ID or original database
query_symbols_without_id_or_database = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol ontox:originalID ?id .
        ?symbol ontox:hasOriginalDatabase ?database .
    }
} LIMIT 10
"""

# SPARQL query to check symbols without depiction
query_symbols_without_depiction = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol foaf:depiction ?depiction .
    }
} LIMIT 10
"""

# SPARQL query to ensure symbols have geographical and ideological contexts
query_symbols_without_contexts = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol ontox:hasGeographicalContext ?location .
        ?symbol ontox:hasIdeologicalContext ?ideology .
    }
} LIMIT 10
"""

# SPARQL query to check symbols without manifestation connection
query_symbols_without_manifestation = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol ontox:manifestedIn ?manifestation .
    }
} LIMIT 10
"""

# SPARQL query to ensure symbols have modality property
query_symbols_without_modality = """
SELECT DISTINCT ?symbol WHERE {
    ?symbol rdf:type ontox:PotentiallyToxicSymbol .
    FILTER NOT EXISTS {
        ?symbol ontox:hasModality ?modality .
    }
} LIMIT 10
"""

# List of SPARQL queries
sparql_queries = [
    query_symbols_without_description,
    query_symbols_without_label,
    query_symbols_with_description_without_label,
    query_symbols_without_id_or_database,
    query_symbols_without_depiction,
    query_symbols_without_contexts,
    query_symbols_without_manifestation,
    query_symbols_without_modality
]

for query in sparql_queries:
    results = g.query(query)

    # Process results as needed
    for row in results:
        print(row)
