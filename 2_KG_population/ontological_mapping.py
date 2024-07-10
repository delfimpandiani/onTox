import json
from rdflib import Graph, Namespace, Literal, URIRef, XSD
from rdflib.namespace import XSD


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

# Create an RDF graph
g = Graph()

database = "GPAHE"
g.add((ontox[database], rdf.type, ontox.Database))
### Create triples for Annotation Situations
with open('../data/merged_ontox_dict.json', 'r') as json_file:
    # Load the JSON data into a Python dictionary
    data = json.load(json_file)

    for symbol_id, details in data.items():
        pt_symbol = str(symbol_id) .lower()
        g.add((ontox[pt_symbol], rdf.type, ontox.PotentiallyToxicSymbol))
        g.add((ontox[pt_symbol], ontox.hasOriginalDatabase, ontox[database]))
        for detail_key, detail_value in details.items():
            if detail_key == "Title":
                g.add((ontox[pt_symbol], rdfs.label, Literal(detail_value, datatype=XSD.string)))
            elif detail_key == "GPAHE_ID":
                g.add((ontox[pt_symbol], ontox.hasOriginalId, Literal(detail_value, datatype=XSD.string)))
            elif detail_key == "OnTox_ID":
                g.add((ontox[pt_symbol], ontox.hasOnToxId, Literal(detail_value, datatype=XSD.string)))
            elif detail_key == "ideology_qids":
                for qid in detail_value: 
                    g.add((wiki[qid[0]], rdf.type, ontox.Ideology))
                    g.add((wiki[qid[0]], rdf.type, ontox.WikiConcept))
                    g.add((wiki[qid[0]], rdfs.label, Literal(qid[1], datatype=XSD.string)))
                    g.add((ontox[pt_symbol], ontox.hasIdeologicalContext, wiki[qid[0]]))     
            elif detail_key == "location_qids":
                for qid in detail_value: 
                    g.add((wiki[qid[0]], rdf.type, ontox.Location))
                    g.add((wiki[qid[0]], rdf.type, ontox.WikiConcept))
                    g.add((wiki[qid[0]], rdfs.label, Literal(qid[1], datatype=XSD.string)))
                    g.add((ontox[pt_symbol], ontox.hasGeographicalContext, wiki[qid[0]]))
            elif detail_key == "Image_URL":
                g.add((ontox[pt_symbol], foaf.depiction, Literal(detail_value, datatype=XSD.string)))
                g.add((URIRef(detail_value), rdf.type, foaf.Image))
            elif detail_key == "Description":
                g.add((ontox[pt_symbol], rdfs.comment, Literal(detail_value, datatype=XSD.string)))
                symbol_description_id = pt_symbol + "_desc"
                g.add((ontox[symbol_description_id], rdf.type, ontox.SymbolDescription))
                g.add((ontox[symbol_description_id], rdfs.label, Literal(detail_value, datatype=XSD.string)))
                g.add((ontox[pt_symbol], ontox.hasDescription, ontox[symbol_description_id]))
            

            elif detail_key == "extracted_synsets":
                for synset in detail_value:
                    synset_name = synset["name"]
                    synset_def = synset["definition"]
                    g.add((wninst[synset_name], rdf.type, wn.Synset))
                    g.add((wninst[synset_name], rdf.type, ontox.Synset))
                    g.add((wninst[synset_name], rdfs.label, Literal(synset_name, datatype=XSD.string)))
                    g.add((wninst[synset_name], rdfs.comment, Literal(synset_def, datatype=XSD.string)))
                    g.add((ontox[pt_symbol], ontox.relatedToConcept, wninst[synset_name]))
                    g.add((ontox[symbol_description_id], ontox.mentionsConcept, wninst[synset_name]))
            elif detail_key == "extracted_ne_qids":
                for qid in detail_value:
                    g.add((wiki[qid["qid"]], rdf.type, ontox.WikiConcept))
                    g.add((wiki[qid["qid"]], rdfs.label, Literal(qid["name"], datatype=XSD.string)))
                    g.add((ontox[pt_symbol], ontox.relatedToNamerelatedToConceptdEntity, wiki[qid["qid"]]))
                    g.add((ontox[symbol_description_id], ontox.mentionsConcept, wiki[qid["qid"]]))
# Serialize the RDF graph to Turtle format
turtle_data = g.serialize(format="turtle")

# Print the Turtle data
print(turtle_data)

# Save the Turtle RDF data to a file
# with open("toy_kg.ttl", "w") as outfile:  # Open in regular text mode (not binary mode)
#     outfile.write(turtle_data)

with open("ontox_kg.ttl", "w") as outfile:  # Open in regular text mode (not binary mode)
    outfile.write(turtle_data)

