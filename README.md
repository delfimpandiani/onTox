# OnTox: An Ontology-Based Toxic Symbology Knowledge Graph and its Use for Harmful Meme Exploration

## Overview
This repository contains the data, code, and content related to the paper "OnTox: Constructing and Leveraging an Ontology-Based Knowledge Graph of Toxic Symbols for Harmful Meme Exploration."
OnTox is an ontology designed to represent and expand data related to toxic symbology using multimodal approaches. This ontology is intended to facilitate the analysis and connection of toxic symbols and related online content, such as memes, by providing a formal and semantic framework.

## Data Source
The data for this project is sourced from the Global Extremist Symbols Database created by the Global Project Against Hate and Extremism (GPAHE). Launched in 2020 by Heidi Beirich and Wendy Via, GPAHE addresses transnational hate and far-right extremism, particularly focusing on U.S.-based activities that influence other countries. GPAHE aims to reduce violence associated with hate and extremism and address systemic problems rooted in hate in governments and societies. For more information about GPAHE, visit [their website](https://globalextremism.org).

### Global Extremist Symbols Database
The Global Extremist Symbols Database is an online resource compiling hate and extremist symbols from across the globe. It serves as a tool for identifying far-right actors, the narratives they push, and combating far-right hate and extremist violence. The database is intended for multiple stakeholders, including law enforcement, tech companies, policymakers, media, advocates, and the general public. For more information about the database, visit the [Global Extremist Symbols Database](https://globalextremism.org/global-extremist-symbols-database/).

## Repository Contents
This repository includes:

- **Data**: The datasets collected and used for creating the ontology and knowledge graph.
- **Ontology**: The OnTox ontology files.
- **Knowledge Graph**: Resources and files used for the creation and expansion of the OnToxKG Knowledge Graph.
- **Code**: Scripts and code for data scraping, ontology creation, knowledge graph creation and expansion, named entity recognition (NER), and entity linking to Wikidata and WordNet.
- **Use Cases**: Example use cases demonstrating the application of OnToxKG in meme toxicity detection.
  
## Using OnTox
OnTox captures the nuances of toxic symbology through the following high-level requirements:
1. **Model the metadata of the symbols:** Capture various attributes such as symbol types, original IDs, titles, descriptions, and contextual tags.
2. **Model the conceptual semantics of symbol descriptions:** Link symbols to named entities, external resources, and specific concepts using linguistic tools.
3. **Model the multimodal manifestation of potentially toxic symbology:** Represent symbols in various online manifestations, noting the type of representation (visual, textual, both).

### Contact
For any questions or inquiries, please contact Delfina at dsmp@cwi.nl.

### License
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgements
We acknowledge the Global Project Against Hate and Extremism (GPAHE) for creating and maintaining the Global Extremist Symbols Database, which serves as the primary data source for this project. 

*Dated: July 8, 2024*
