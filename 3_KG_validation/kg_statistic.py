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
wordnet_mappings_noun = 0
wordnet_mappings_verb = 0
wordnet_mappings_adjective = 0

wordnet_mappings = 0
for symbol_entity in g.subjects(rdf.type, ontox.PotentiallyToxicSymbol):
    related_entities_count[symbol_entity] += len(list(g.objects(symbol_entity, ontox.relatedToConcept)))
    for related_entity in g.objects(symbol_entity, ontox.relatedToConcept):
        if str(related_entity).startswith(str("http://www.wikidata.org/")):
            wikidata_mappings += 1
    for related_entity in g.objects(symbol_entity, ontox.relatedToConcept):
        if str(related_entity).startswith(str("https://w3id.org/framester/wn/wn30/")):
            if str(related_entity).endswith(".n.01"):
                wordnet_mappings_noun += 1
            elif str(related_entity).endswith(".v.01"):
                wordnet_mappings_verb += 1
            elif str(related_entity).endswith(".a.01"):
                wordnet_mappings_adjective += 1
            wordnet_mappings += 1


mean_wiki_entities_per_symbol = wikidata_mappings / num_symbols
mean_wordnet_entities_per_symbol = wordnet_mappings / num_symbols
mean_wordnet_entities_per_symbol_noun = wordnet_mappings_noun / num_symbols
mean_wordnet_entities_per_symbol_verb = wordnet_mappings_verb / num_symbols
mean_wordnet_entities_per_symbol_adjective = wordnet_mappings_adjective / num_symbols

if related_entities_count:
    mean_entities_per_symbol = sum(related_entities_count.values()) / len(related_entities_count)
    max_entities_per_symbol = max(related_entities_count.values())
    min_entities_per_symbol = min(related_entities_count.values())


# Print out the statistics

print(f"Number of Potentially Toxic Symbols: {num_symbols}")
print(f"Number of Triples: {num_triples}")
print(f"Number of Unique Entities: {num_unique_entities}")
print(f"Number of Wikidata Mappings: {num_wikidata_mappings}")
print(f"Number of WordNet Mappings: {num_wordnet_mappings}")

print(f"Mean Wikidata Entities per Symbol: {mean_wiki_entities_per_symbol}")
print(f"Mean WordNet Entities per Symbol: {mean_wordnet_entities_per_symbol}")

print(f"Mean Entities per Symbol: {mean_entities_per_symbol}")
print(f"Maximum Entities per Symbol: {max_entities_per_symbol}")
print(f"Minimum Entities per Symbol: {min_entities_per_symbol}")

print(f"Mean WordNet Noun Entities per Symbol: {mean_wordnet_entities_per_symbol_noun}")
print(f"Mean WordNet Verb Entities per Symbol: {mean_wordnet_entities_per_symbol_verb}")
print(f"Mean WordNet Adjective Entities per Symbol: {mean_wordnet_entities_per_symbol_adjective}")



top_10_ideologies = [
    ("http://www.wikidata.org/entity/Q110441926", "white nationalist", 499),
    ("http://www.wikidata.org/entity/Q126096643", "neo-Nazi", 266),
    ("http://www.wikidata.org/entity/Q1969722", "nativism", 243),
    ("http://www.wikidata.org/entity/Q33487", "Homophobia", 150),
    ("http://www.wikidata.org/entity/Q15954665", "antisemite", 108),
    ("http://www.wikidata.org/entity/Q486296", "Islamophobia", 100),
    ("http://www.wikidata.org/entity/Q4481595", "fascist", 97),
    ("http://www.wikidata.org/entity/Q159535", "conspiracy theory", 63),
    ("http://www.wikidata.org/entity/Q5109957", "Christian Nationalism", 43),
    ("http://www.wikidata.org/entity/Q64717200", "anti-gender movement", 26)
]

top_10_locations = [
    ("http://www.wikidata.org/entity/Q30", "United States of America", 263),
    ("http://www.wikidata.org/entity/Q142", "France", 141),
    ("http://www.wikidata.org/entity/Q46", "Europe", 92),
    ("http://www.wikidata.org/entity/Q159", "Russia", 55),
    ("http://www.wikidata.org/entity/Q183", "Germany", 55),
    ("http://www.wikidata.org/entity/Q16", "Canada", 49),
    ("http://www.wikidata.org/entity/Q13780930", "worldwide", 47),
    ("http://www.wikidata.org/entity/Q212", "Ukraine", 46),
    ("http://www.wikidata.org/entity/Q45", "Portugal", 37),
    ("http://www.wikidata.org/entity/Q38", "Italy", 34)
]

top_10_entities = [
    ("http://www.wikidata.org/entity/Q126096643", "neo-Nazi", 154),
    ("http://www.wikidata.org/entity/Q574578", "Nazi", 134),
    ("http://www.wikidata.org/entity/Q846570", "Americans", 127),
    ("http://www.wikidata.org/entity/Q200", "2", 92),
    ("http://www.wikidata.org/entity/Q142", "France", 90),
    ("http://www.wikidata.org/entity/Q55281147", "December 2020", 89),
    ("http://www.wikidata.org/entity/Q30", "United States of America", 88),
    ("http://www.wikidata.org/entity/Q2914650", "identity politics", 73),
    ("http://www.wikidata.org/entity/Q150", "French", 67),
    ("http://www.wikidata.org/entity/Q486296", "Islamophobia", 64)
]


# Create a bar graph for the top 20 qid in which the labels are in the x axis, and the count in the y axis, starting form the top_10_ideologies list

import matplotlib.pyplot as plt

# Extract labels and counts for plotting
entities_labels = [label for qid, label, count in top_10_ideologies]  # Using qid as key here temporarily
entities_counts = [count for qid, label, count in top_10_ideologies]

plt.figure(figsize=(12, 8))  # Adjust figure size for better presentation
bars = plt.bar(entities_labels, entities_counts, color='skyblue', edgecolor='black')  # Use skyblue with black edges
plt.xlabel('Wikidata Entity', fontsize=12)  # Set xlabel with larger font size
plt.ylabel('Count', fontsize=12)  # Set ylabel with larger font size
plt.title('Top 10 Most Mentioned WikiData Entities by Count of Symbols', fontsize=14)  # Update title with larger font size
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for better readability
# Add grid lines
plt.grid(axis='y', linestyle='--', alpha=0.7)
# Add count labels above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, int(yval), ha='center', va='bottom', fontsize=8)
plt.tight_layout()  # Adjust layout
plt.show()


# do thr same for the top_10_locations list and the top_10_entities list

# Extract labels and counts for plotting
location_labels = [label for qid, label, count in top_10_locations]  # Using qid as key here temporarily
location_counts = [count for qid, label, count in top_10_locations]

plt.figure(figsize=(12, 8))  # Adjust figure size for better presentation
bars = plt.bar(location_labels, location_counts, color='skyblue', edgecolor='black')  # Use skyblue with black edges
plt.xlabel('Wikidata Entity', fontsize=12)  # Set xlabel with larger font size
plt.ylabel('Count', fontsize=12)  # Set ylabel with larger font size
plt.title('Top 10 Most Mentioned Locations by Count of Symbols', fontsize=14)  # Update title with larger font size
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for better readability
# Add grid lines
plt.grid(axis='y', linestyle='--', alpha=0.7)
# Add count labels above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, int(yval), ha='center', va='bottom', fontsize=8)
plt.tight_layout()  # Adjust layout
plt.show()

# Extract labels and counts for plotting
ideology_labels = [label for qid, label, count in top_10_ideologies]  # Using qid as key here temporarily
ideology_counts = [count for qid, label, count in top_10_ideologies]

plt.figure(figsize=(12, 8))  # Adjust figure size for better presentation
bars = plt.bar(ideology_labels, ideology_counts, color='skyblue', edgecolor='black')  # Use skyblue with black edges
plt.xlabel('Wikidata Entity', fontsize=12)  # Set xlabel with larger font size
plt.ylabel('Count', fontsize=12)  # Set ylabel with larger font size
plt.title('Top 10 Most Mentioned Ideologies by Count of Symbols', fontsize=14)  # Update title with larger font size
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for better readability
# Add grid lines
plt.grid(axis='y', linestyle='--', alpha=0.7)
# Add count labels above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, int(yval), ha='center', va='bottom', fontsize=8)
plt.tight_layout()  # Adjust layout
plt.show()
