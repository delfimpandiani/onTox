import pyshacl
from rdflib import Graph

# Load the SHACL shapes file and your KG data
shapes_file = "shacl_shapes_val.ttl"
# kg_data_file = "../ontology/ont_ontox_kg.ttl"
kg_data_file = "../2_kg_population/ontox_kg.ttl"

shapes_graph = Graph().parse(shapes_file, format="turtle")
kg_graph = Graph().parse(kg_data_file, format="turtle")

# Execute SHACL validation
conforms, results_graph, results_text = pyshacl.validate(
    data_graph=kg_graph,
    shacl_graph=shapes_graph,
    ont_graph=None,
    inference='rdfs',
    abort_on_error=False,
    meta_shacl=False,
    advanced=False,
    js=False
)

# Check if the KG conforms to the SHACL shapes
if conforms:
    print("KG data conforms to the SHACL shapes.")
else:
    print("KG data does not conform to the SHACL shapes.")
    for result in results_graph:
        print(result)