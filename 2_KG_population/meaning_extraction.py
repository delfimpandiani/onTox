"""
Script: meaning_extraction.py

This script performs natural language processing to extract synsets and named entities from given paragraphs. It utilizes NLTK for tokenization, part-of-speech tagging, lemmatization, and WordNet for synset extraction. Named entities are resolved using spaCy and queried against Wikidata for additional metadata.

Dependencies:
- `requests`: For querying Wikidata.
- `nltk`: For natural language processing tasks including tokenization, tagging, and lemmatization.
- `WordNet`: Lexical database for English language words.
- `spacy`: For named entity recognition.

Usage:
- Load the symbol data from `ontox_dict.json`.
- Run the script to generate a linked dictionary of OnTox symbols with extracted synsets and named entities.

Inputs:
- JSON file (`ontox_dict.json`): Contains symbol data with descriptions.

Outputs:
- JSON file (`linked_ontox_dict.json`): Contains structured data with extracted synsets and named entities for each input paragraph.

"""
import json
import spacy
import requests
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

nlp = spacy.load('en_core_web_sm')

def get_wikidata_info(entity_label):
    """
    Function to query Wikidata API for a given entity label and return its QID and name.

    Args:
    - `entity_label` (str): Label of the entity to be queried.
    
    Returns:
    - `str`: QID of the entity.
    - `str`: Name of the entity.
    
    Dependencies:
    - `requests`: For querying Wikidata API.
    
    Output:
    - Returns the QID and name of the entity if found, otherwise returns `None`.
    
    """
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": entity_label
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['search']:
        qid = data['search'][0]['id']
        name = data['search'][0]['label']
        return qid, name
    else:
        return None, None


def create_linked_ontox_dict(ontox_dict):
    """
    Function to create a linked dictionary of OnTox symbols with their respective synsets and named entities.

    Args:
    - `ontox_dict` (dict): Input dictionary containing symbol data with descriptions.

    Returns:
    - `dict`: Dictionary (`linked_ontox_dict`) structured with symbol IDs as keys and their corresponding synsets and named entities as values.

    Dependencies:
    - `spacy`: For named entity recognition.
    - `nltk`: For tokenization, part-of-speech tagging, and lemmatization.
    - `requests`: For querying Wikidata API.
    - `WordNet`: Lexical database for English language words.

    Inner Functions:
    - `get_named_entities(paragraph)`: Extracts named entities from a given paragraph using spaCy and resolves them against Wikidata for additional metadata.
    - `extract_synsets(paragraph)`: Identifies relevant synsets (semantic groupings) from a paragraph's tokens using NLTK's WordNet.

    Output:
    - Saves `linked_ontox_dict` to '../data/linked_ontox_dict.json'.
    - Returns `linked_ontox_dict` containing structured symbol data with extracted synsets and named entities.
    """

    def get_named_entities(paragraph):
        doc = nlp(paragraph)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        unique_entities = set(entities)
        entity_info = []
        for entity, entity_type in unique_entities:
            qid, name = get_wikidata_info(entity)
            if qid and name:
                entity_info.append((qid, name))
        return sorted(entity_info, key=lambda x: x[0])

    def extract_synsets(paragraph):
        tokens = word_tokenize(paragraph)
        tagged_tokens = pos_tag(tokens)
        relevant_synsets = set()
        lemmatizer = WordNetLemmatizer()
        for token, tag in tagged_tokens:
            if tag.startswith('NN') or tag.startswith('VB') or tag.startswith('JJ') or tag.startswith('RB'):
                lemma = lemmatizer.lemmatize(token)
                synsets = wn.synsets(lemma)
                if synsets:
                    synset = synsets[0]
                    relevant_synsets.add((synset.name(), synset.definition()))
        return sorted(list(relevant_synsets), key=lambda x: x[0])

    linked_ontox_dict = {}
    for symbol_id, symbol_data in ontox_dict.items():
        description = symbol_data['Description']
        synsets = extract_synsets(description)
        named_entities = get_named_entities(description)
        linked_ontox_dict[symbol_id] = {
            "extracted_synsets": [{"name": synset[0], "definition": synset[1]} for synset in synsets],
            "extracted_ne_qids": [{"qid": entity[0], "name": entity[1]} for entity in named_entities]
        }

        
    # Write the dictionary to linked_ontox_dict.json
    with open('../data/linked_ontox_dict.json', 'w', encoding='utf-8') as f:
        json.dump(linked_ontox_dict, f, indent=2, ensure_ascii=True)

    return linked_ontox_dict

def main():
    """
    Main execution function to load symbol data, process it to create a linked dictionary of OnTox symbols, and save the result.

    Usage:
    - Loads symbol data from '../data/ontox_dict.json'.
    - Calls `create_linked_ontox_dict` to generate a linked dictionary (`linked_ontox_dict`) with extracted synsets and named entities.
    - Saves the resulting `linked_ontox_dict` to '../data/linked_ontox_dict.json'.
    """
    ontox_dict = json.load(open('../data/ontox_dict.json', 'r'))
    linked_ontox_dict = create_linked_ontox_dict(ontox_dict)

if __name__ == "__main__":
    main()