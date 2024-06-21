import spacy
import requests
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
# Download necessary NLTK data
nlp = spacy.load('en_core_web_sm')


# Function to extract ideologies and locations from a JSON dictionary
def extract_and_link_ideologies_and_locations(data):
    ideologies = set()
    locations = set()
    
    for key, value in data.items():
        # Collect all ideologies into a list
        ideology_list = value['Ideology'].split(', ')
        ideologies.update(ideology_list)
        locations.update(value['Location'].split(', '))
    
    # Convert ideologies set to a sorted list
    ideologies = sorted(list(ideologies))
    locations = sorted(list(locations))
    
    # Get Wikidata info for each ideology
    ideology_qid_name = {ideology: get_wikidata_info(ideology) for ideology in ideologies}
    location_qid_name = {location: get_wikidata_info(location) for location in locations}
    
    return ideologies, locations, ideology_qid_name, location_qid_name









####### EXECUTION


# Example usage:
file_path = 'scraped_symbol_dict.json'  # Adjust the file path as per your directory structure
data = load_json(file_path)


# Transform the scraped symbols dictionary
transformed_symbols_dict = create_ontox_dict(data)



## Extract ideologies and locations with Wikidata links
# ideologies, locations, ideology_qid_name, location_qid_name = extract_ideologies_and_locations(scrabed_symbol_dict)
# print("Ideologies:")
# for ideology in ideologies:
#     qid, name = ideology_qid_name.get(ideology, (None, None))
#     print(f"{ideology}: QID={qid}, Name={name}")
# print("\nLocations:")
# for location in locations:
#     qid, name = location_qid_name.get(location, (None, None))
#     print(f"{location}: QID={qid}, Name={name}")