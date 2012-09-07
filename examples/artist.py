import py7D

def artist_search(*args, **kwargs):
    client = py7D.APIClient(
        "your_oauth_customer_key",
        "your_ISO_country_code")

    kwargs['page'] = str(kwargs.get('page', 1))
    kwargs['pageSize'] = str(kwargs.get('pageSize', 10))

    results = client.request('artist', 'search', **kwargs)
    return results['searchResults']

if __name__ == "__main__":
    print artist_search(q="Pink")
