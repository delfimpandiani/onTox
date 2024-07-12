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
database = "OnTox_Case_Study"
g.add((ontox[database], rdf.type, ontox.Database))
### Create triples for Annotation Situations
with open('gpahe_process.json', 'r') as json_file:
    # Load the JSON data into a Python dictionary
    data = json.load(json_file)

    for meme_id, details in data.items():
        meme_id = meme_id.lower()
        text_desc_id = meme_id + "_text"
        visual_desc_id = meme_id + "_visual"
        mm_desc_id = meme_id + "_mm"
        g.add((ontox[meme_id], rdf.type, ontox.Meme))
        g.add((ontox[meme_id], ontox.hasOriginalDatabase, ontox[database]))
        g.add((ontox[meme_id], rdfs.label, Literal(meme_id, datatype=XSD.string)))
        for detail_key, detail_value in details.items():
            if detail_key == "Image_URL":
                g.add((ontox[meme_id], foaf.depiction, URIRef(detail_value)))
                g.add((URIRef(detail_value), rdf.type, foaf.Image))
            elif detail_key == "Meme_text":
                g.add((ontox[meme_id], ontox.haEmbeddedText, Literal(detail_value.replace('\n', ' ').replace('\\"', '"').replace('"', '').replace("'", ''), datatype=XSD.string)))
            elif detail_key == "Textual_description":
                g.add((ontox[text_desc_id], rdf.type, ontox.TextContentDescription))
                g.add((ontox[meme_id], ontox.hasTextContentDescription, ontox[text_desc_id]))
                g.add((ontox[text_desc_id], rdfs.label, Literal(detail_value.replace('\n', ' ').replace('\\"', '"').replace('"', '').replace("'", '')
, datatype=XSD.string)))
            elif detail_key == "Visual_description":
                g.add((ontox[visual_desc_id], rdf.type, ontox.VisualContentDescription))
                g.add((ontox[meme_id], ontox.hasVisualContentDescription, ontox[visual_desc_id]))
                g.add((ontox[visual_desc_id], rdfs.label, Literal(detail_value.replace('\n', ' ').replace('\\"', '"').replace('"', '').replace("'", '')
, datatype=XSD.string)))
            elif detail_key == "Combined_description":
                g.add((ontox[mm_desc_id], rdf.type, ontox.MultimodalContentDescription))
                g.add((ontox[meme_id], ontox.hasMultimodalContentDescription, ontox[mm_desc_id]))
                g.add((ontox[mm_desc_id], rdfs.label, Literal(detail_value.strip().replace('\n', ' ').replace('\\"', '"').replace('"', '').replace("'", '')
, datatype=XSD.string)))
            elif detail_key == "extracted_synsets":
                for mode, mode_details in detail_value.items():
                    if mode == "visual":
                        for synset in mode_details:
                            synset_name = synset["name"]
                            synset_def = synset["definition"]
                            g.add((wninst[synset_name], rdf.type, wn.Synset))
                            g.add((wninst[synset_name], rdf.type, ontox.Synset))
                            g.add((wninst[synset_name], rdfs.label, Literal(synset_name, datatype=XSD.string)))
                            g.add((wninst[synset_name], rdfs.comment, Literal(synset_def, datatype=XSD.string)))
                            g.add((ontox[meme_id], ontox.relatedToConcept, wninst[synset_name]))
                            g.add((ontox[visual_desc_id], ontox.mentionsConcept, wninst[synset_name]))
                    elif mode == "textual":
                        for synset in mode_details:
                            synset_name = synset["name"]
                            synset_def = synset["definition"]
                            g.add((wninst[synset_name], rdf.type, wn.Synset))
                            g.add((wninst[synset_name], rdf.type, ontox.Synset))
                            g.add((wninst[synset_name], rdfs.label, Literal(synset_name, datatype=XSD.string)))
                            g.add((wninst[synset_name], rdfs.comment, Literal(synset_def, datatype=XSD.string)))
                            g.add((ontox[meme_id], ontox.relatedToConcept, wninst[synset_name]))
                            g.add((ontox[text_desc_id], ontox.mentionsConcept, wninst[synset_name]))
                    elif mode == "combined":
                        for synset in mode_details:
                            synset_name = synset["name"]
                            synset_def = synset["definition"]
                            g.add((wninst[synset_name], rdf.type, wn.Synset))
                            g.add((wninst[synset_name], rdf.type, ontox.Synset))
                            g.add((wninst[synset_name], rdfs.label, Literal(synset_name, datatype=XSD.string)))
                            g.add((wninst[synset_name], rdfs.comment, Literal(synset_def, datatype=XSD.string)))
                            g.add((ontox[meme_id], ontox.relatedToConcept, wninst[synset_name]))
                            g.add((ontox[mm_desc_id], ontox.mentionsConcept, wninst[synset_name]))
            elif detail_key == "extracted_ne_qids":
                for mode, mode_details in detail_value.items():
                    if mode == "visual":
                        for qid in mode_details:
                            g.add((wiki[qid["qid"]], rdf.type, ontox.WikiConcept))
                            g.add((wiki[qid["qid"]], rdfs.label, Literal(qid["name"], datatype=XSD.string)))
                            g.add((ontox[meme_id], ontox.relatedToConcept, wiki[qid["qid"]]))
                            g.add((ontox[visual_desc_id], ontox.mentionsConcept, wiki[qid["qid"]]))
                    elif mode == "textual":
                        for qid in mode_details:
                            g.add((wiki[qid["qid"]], rdf.type, ontox.WikiConcept))
                            g.add((wiki[qid["qid"]], rdfs.label, Literal(qid["name"], datatype=XSD.string)))
                            g.add((ontox[meme_id], ontox.relatedToConcept, wiki[qid["qid"]]))
                            g.add((ontox[text_desc_id], ontox.mentionsConcept, wiki[qid["qid"]]))
                    elif mode == "combined":
                        for qid in mode_details:
                            g.add((wiki[qid["qid"]], rdf.type, ontox.WikiConcept))
                            g.add((wiki[qid["qid"]], rdfs.label, Literal(qid["name"], datatype=XSD.string)))
                            g.add((ontox[meme_id], ontox.relatedToConcept, wiki[qid["qid"]]))
                            g.add((ontox[mm_desc_id], ontox.mentionsConcept, wiki[qid["qid"]]))

# Serialize the RDF graph to Turtle format
turtle_data = g.serialize(format="turtle")

# Print the Turtle data
print(turtle_data)

# Save the Turtle RDF data to a file
# with open("toy_kg.ttl", "w") as outfile:  # Open in regular text mode (not binary mode)
#     outfile.write(turtle_data)

with open("meme_kg.ttl", "w") as outfile:  # Open in regular text mode (not binary mode)
    outfile.write(turtle_data)

