import py7D
import json
from pprint import pprint

def find_release(search_string):
    ''' return JSON of a search for a release '''

    client = py7D.APIClient(
        "your_oauth_customer_key",
        "your_ISO_country_code")
    
    response = client.execute('release', 'search', q=search_string ,pageSize=5)
    
    results = response['searchResults']['searchResult']
    
    results = json.dumps(results)
    
    #show me what I'm looking at
    pprint(json.loads(results))
    
    return results
