import json
from 2_meaning_extraction import get_wikidata_info

def extract_context_qids(data):
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