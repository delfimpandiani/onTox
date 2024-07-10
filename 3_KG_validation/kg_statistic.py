from rdflib import Graph, Namespace, URIRef
from collections import defaultdict

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

# Count unique entities
unique_entities = set()
for s, p, o in g:
    unique_entities.add(s)
    unique_entities.add(o) if isinstance(o, URIRef) else None

num_unique_entities = len(unique_entities)

# Count entities with mappings to Wikidata and WordNet
wikidata_mappings = set()
wordnet_mappings = set()

for s, p, o in g:
    if p == ontox.relatedToConcept:
        ## check if they are wikidata or wordnet mappings
        if str(o).startswith(str("http://www.wikidata.org/")):
            wikidata_mappings.add(o)
        else:
            wordnet_mappings.add(o)

num_wikidata_mappings = len(wikidata_mappings)
num_wordnet_mappings = len(wordnet_mappings)

# Calculate mean and maximum number of related entities per symbol
related_entities_count = defaultdict(int)



for symbol_entity in g.subjects(rdf.type, ontox.PotentiallyToxicSymbol):
    related_entities_count[symbol_entity] += len(list(g.objects(symbol_entity, ontox.relatedToConcept)))
    # check the mean number of wikidata vs wordnet related entities per symbol
    for related_entity in g.objects(symbol_entity, ontox.relatedToConcept):
        if str(related_entity).startswith(str("http://www.wikidata.org/")):
            wikidata_mappings.add(related_entity)
        else:
            wordnet_mappings.add(related_entity)
    mean_wiki_entities_per_symbol = sum(related_entities_count.values()) / len(wikidata_mappings)
    mean_wordnet_entities_per_symbol = sum(related_entities_count.values()) / len(wordnet_mappings)


num_symbols = len(list(g.subjects(rdf.type, ontox.PotentiallyToxicSymbol)))
wikidata_mappings = 0
wordnet_mappings = 0
for symbol_entity in g.subjects(rdf.type, ontox.PotentiallyToxicSymbol):
    related_entities_count[symbol_entity] += len(list(g.objects(symbol_entity, ontox.relatedToConcept)))
    for related_entity in g.objects(symbol_entity, ontox.relatedToConcept):
        if str(related_entity).startswith(str("http://www.wikidata.org/")):
            wikidata_mappings += 1
    for related_entity in g.objects(symbol_entity, ontox.relatedToConcept):
        if str(related_entity).startswith(str("https://w3id.org/framester/wn/wn30/")):
            wordnet_mappings += 1


mean_wiki_entities_per_symbol = wikidata_mappings / num_symbols
mean_wordnet_entities_per_symbol = wordnet_mappings / num_symbols

if related_entities_count:
    mean_entities_per_symbol = sum(related_entities_count.values()) / len(related_entities_count)
    max_entities_per_symbol = max(related_entities_count.values())
    min_entities_per_symbol = min(related_entities_count.values())


else:
    mean_entities_per_symbol = 0
    # max_entities_per_symbol = 0

# # Print out the statistics
print(f"Number of Triples: {num_triples}")
print(f"Number of Unique Entities: {num_unique_entities}")
print(f"Number of Wikidata Mappings: {num_wikidata_mappings}")
print(f"Number of WordNet Mappings: {num_wordnet_mappings}")

print(f"Mean Wikidata Entities per Symbol: {mean_wiki_entities_per_symbol}")
print(f"Mean WordNet Entities per Symbol: {mean_wordnet_entities_per_symbol}")

print(f"Mean Entities per Symbol: {mean_entities_per_symbol}")
print(f"Maximum Entities per Symbol: {max_entities_per_symbol}")
print(f"Minimum Entities per Symbol: {min_entities_per_symbol}")