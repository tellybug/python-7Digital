import py7D
import json

def artist_search(*args, **kwargs):

    kwargs['page'] = str(kwargs.get('page', 1))
    kwargs['pageSize'] = str(kwargs.get('pageSize', 10))

    results = py7D.request('artist', 'search', **kwargs)
    return results['response']['searchResults']

if __name__ == "__main__":
    print json.dumps(artist_search(q="Pink", pageSize=3),
                     indent=4)
