# OnTox: An Ontology-Based Toxic Symbology Knowledge Graph and its Use for Harmful Meme Exploration

## Overview
This repository contains the data, code, and content related to the paper "OnTox: Constructing and Leveraging an Ontology-Based Knowledge Graph of Toxic Symbols for Harmful Meme Exploration."

### Abstract
Online toxicity is a significant problem, manifesting increasingly through multimodal and semiotically complex forms such as memes. Given the sheer volume of data, content moderation systems require automated methods to detect and explain toxic content. Memes, however, rely on complex intertextual relationships, combining visual and textual elements to evoke implicit knowledge. Existing detection methods typically analyze content within the meme itself without incorporating essential background knowledge. Although recent works have started to include commonsense knowledge, it is not specific enough for effective toxicity detection in memes. Despite a wealth of expert knowledge on toxicity and toxic symbols, existing resources are underutilized and lack structured integration into automated systems.

This paper introduces the OnTox ontology and the OnToxKG Knowledge Graph (KG) to address these gaps, specifically focusing on meme toxicity. OnTox is an ontology representing the semantics of hateful, extremist, or otherwise potentially toxic symbols, including hate images, hand signs, hateful clothing, literature, media, music, military insignia, and textual symbols. OnToxKG is a multimodal knowledge graph that captures the semantics of over 800 toxic symbols and connects them to commonsense sources such as Wikidata, ConceptNet, and WordNet. We demonstrate the practical applications of OnToxKG through five use cases related to meme toxicity detection, showcasing how this structured approach enhances both the detection and explanation of toxic content in memes.

## Repository Contents
This repository includes:

- **Data**: The datasets collected and used for creating the ontology and knowledge graph.
- **Ontology**: The OnTox ontology files.
- **Knowledge Graph**: Resources and files used for the creation and expansion of the OnToxKG Knowledge Graph.
- **Code**: Scripts and code for data scraping, ontology creation, knowledge graph creation and expansion, named entity recognition (NER), and entity linking to Wikidata and WordNet.
- **Use Cases**: Example use cases demonstrating the application of OnToxKG in meme toxicity detection.

### Contact
For any questions or inquiries, please contact Your Name.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
