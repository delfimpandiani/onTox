import json

def merge_dictionaries(ontox_dict, ontox_dict_context_linked, linked_ontox_dict):
    """
    Merges three dictionaries into one.

    Args:
    - `ontox_dict` (dict): Dictionary containing symbol data from GPAHE.
    - `ontox_dict_context_linked` (dict): Dictionary containing symbol ids with ideologies and locations mapped to their Wikidata QIDs.
    - `linked_ontox_dict` (dict): Dictionary containing symbol ids with synsets and named entities extracted from descriptions.

    Returns:
    - `dict`: Merged dictionary combining data from all three input dictionaries.
    
    Output:
    - Saves merged dictionary to '../data/merged_ontox_dict.json'.
    - Returns merged dictionary.
    """
    merged_dict = {}

    for symbol_id, symbol_data in ontox_dict.items():
        merged_dict[symbol_id] = symbol_data

        if symbol_id in ontox_dict_context_linked:
            merged_dict[symbol_id].update(ontox_dict_context_linked[symbol_id])
        
        if symbol_id in linked_ontox_dict:
            merged_dict[symbol_id].update(linked_ontox_dict[symbol_id])
    
    # Write the merged dictionary to a file
    with open('../data/merged_ontox_dict.json', 'w', encoding='utf-8') as f:
        json.dump(merged_dict, f, indent=2, ensure_ascii=False)

    return merged_dict


def main():
    """
    Main execution function to load dictionaries, merge them, and save the result.
    """
    # Load the dictionaries from their JSON files
    with open('../data/ontox_dict.json', 'r', encoding='utf-8') as f:
        ontox_dict = json.load(f)
    
    with open('../data/ontox_dict_context_linked.json', 'r', encoding='utf-8') as f:
        ontox_dict_context_linked = json.load(f)

    with open('../data/linked_ontox_dict.json', 'r', encoding='utf-8') as f:
        linked_ontox_dict = json.load(f)

    # Merge the dictionaries
    merged_dict = merge_dictionaries(ontox_dict, ontox_dict_context_linked, linked_ontox_dict)
    
    return merged_dict

if __name__ == "__main__":
    main()