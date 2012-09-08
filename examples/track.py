import py7D
import json

def track_previews():

    response = py7D.request('track', 'search', q='Aja', pageSize=3)
    tracks = response['response']['searchResults']['searchResult']
    

    for track in tracks:
        print track
        track['preview'] = py7D.preview_url(track['track']['@id'])
    
    return tracks

if __name__ == "__main__":
    print json.dumps(track_previews(), indent=4)
