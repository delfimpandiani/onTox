import os 
import json
from meaning_extraction import get_wikidata_info

def extract_context_qid_map(data):
    """
    Extracts labels for ideological context (ideologies) and geographical context (locations) from a JSON dictionary of symbol data, and creates a dictionary that maps the strings used to their Wikidata QIDs.
    
    Args:
    - `data` (dict): Input dictionary containing symbol data with descriptions.

    Returns:
    - `dict`: Dictionary (`contexts_qid_map`) structured with ideologies and locations as keys and their corresponding Wikidata QIDs and names as values.

    Dependencies:
    - `json`: For reading and writing JSON files.
    - `get_wikidata_info`: Function to query Wikidata API for a given entity label and return its QID and name.

    Output:
    - Saves `contexts_qid_map` to '../data/contexts_qid_map.json'.
    - Returns `contexts_qid_map` containing extracted ideologies and locations mapped to their Wikidata QIDs.

    """
    ideologies = set()
    locations = set()
    contexts_qid_map = {}
    contexts_qid_map["ideologies"] = {}
    contexts_qid_map["locations"] = {}

    for key, value in data.items():
        # Collect all ideologies into a list
        ideology_list = value['Ideology'].split(', ')
        ideologies.update(ideology_list)
        locations.update(value['Location'].split(', '))
    
    # Convert ideologies set to a sorted list
    ideologies = sorted(list(ideologies))
    locations = sorted(list(locations))
    
    # Get Wikidata info for each ideology
    for ideology in ideologies:
        qid, name = get_wikidata_info(ideology)
        contexts_qid_map["ideologies"][ideology] = (qid, name)
    for location in locations:
        qid, name = get_wikidata_info(location)
        contexts_qid_map["locations"][location] = (qid, name)
        
    # Write the dictionary to context_mappings.json
    with open('../data/contexts_qid_map.json', 'w', encoding='utf-8') as f:
        json.dump(contexts_qid_map, f, indent=2, ensure_ascii=True)

    return contexts_qid_map



def create_ontox_dict_context_linked(symbol_dict, mapping_dict):
    """
    Maps ideologies and locations to their corresponding QIDs in the symbol dictionary.
    
    Args:
    - `symbol_dict` (dict): Input dictionary containing symbol data with descriptions.
    - `mapping_dict` (dict): Dictionary containing ideologies and locations mapped to their Wikidata QIDs.
    
    Returns:
    - `dict`: Dictionary (`ontox_dict_context_linked`) structured with symbol IDs as keys and their corresponding ideologies and locations as values.

    Dependencies:
    - `json`: For reading and writing JSON files.

    Output:
    - Saves `ontox_dict_context_linked` to '../data/ontox_dict_context_linked.json'.
    - Returns `ontox_dict_context_linked` containing symbol data with ideologies and locations mapped to their Wikidata QIDs.
    """
    ontox_dict_context_linked = {}
    for symbol_id, symbol_data in symbol_dict.items():
        ideologies = symbol_data.get("Ideology")
        if ideologies:
            ideologies = [ideology.strip() for ideology in ideologies.split(',')]
            ideology_qids = []
            for ideology in ideologies:
                if ideology in mapping_dict["ideologies"]:
                    ideology_qids.append(mapping_dict["ideologies"][ideology])
            symbol_data["ideology_qids"] = ideology_qids
        else:
            symbol_data["ideology_qids"] = []

        location = symbol_data.get("Location")
        location_qids = []
        if location:
            locations = [loc.strip() for loc in location.split(',')]
            for loc in locations:
                if loc in mapping_dict["locations"]:
                    location_qids.append(mapping_dict["locations"][loc])
        symbol_data["location_qids"] = location_qids
        ontox_dict_context_linked[symbol_id] = symbol_data

    with open('../data/ontox_dict_context_linked.json', 'w', encoding='utf-8') as f:
        json.dump(ontox_dict_context_linked, f, indent=2, ensure_ascii=True)

    return ontox_dict_context_linked



def main():
    """
    Main execution function to extract context QID mappings and create linked OnTox dictionary.
    """
    symbol_dict = json.load(open('../data/ontox_dict.json', 'r', encoding='utf-8'))
    if os.path.exists('../data/corrected_contexts_qid_map.json'):
        mapping_dict = json.load(open('../data/corrected_contexts_qid_map.json', 'r', encoding='utf-8'))
    else:
        mapping_dict = extract_context_qid_map(symbol_dict)
    create_ontox_dict_context_linked(symbol_dict, mapping_dict)

if __name__ == "__main__":
    main()
