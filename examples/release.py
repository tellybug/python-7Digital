import py7D
import json
from pprint import pprint

def find_release(search_string):
    ''' return JSON of a search for a release '''
    
    response = py7D.request('release', 'search', q=search_string, pageSize=5)
    
    headers = response['http_headers']
    results = response['response']['searchResults']['searchResult']
    
    return results


if __name__ == "__main__":
    print json.dumps(find_release("aja"),
                     indent=4)
