import py7D
import json

def track_previews():
    client = py7D.APIClient(
        "your_oauth_customer_key",
        "your_ISO_country_code")

    response = client.request('track', 'search', q='Aja')
    tracks = response['searchResults']['searchResult']
    

    for track in tracks:
        print track
        track['preview'] = client.preview_url(track['track']['@id'])
    
    return tracks

if __name__ == "__main__":
    print json.dumps(track_previews(), indent=4)
