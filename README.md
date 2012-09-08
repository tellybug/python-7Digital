python-7Digital (py7D)
===============
py7D - A lightweight client for the 7Digital API.

Prerequisites
-------------
 python-oath2 :   git://github.com/simplegeo/python-oauth2.git
 
 xmltodict :      pip install xmltodict or clone from git://github.com/martinblech/xmltodict.git
                

Description
-----------
py7D is a very lightweight API client for the 7Digital API.

The client is meant to provide a very thin layer of access to the 7Digital API
with which you can make any call to any of the valid methods and functions
described in the documentation. 

The documentation for the API is found here:
http://api.7digital.com/1.2/static/documentation/7digitalpublicapi.html

The response is converted from XML to a python Ordered Dict, and each 
node in the XML is converted to a key name. 

In the case of a node attribute, the attribute name is converted to a
key name preceded by the '@' character. For example, 
<track id=123>...</track>
would convert to {'track' : {'@id' : 123, ...}}


Usage
-----
    import py7D
    client = py7D.APIClient("your oauth_consumer_key", "an ISO country code")
    results = client.request(method, function, page=1, pageSize=10)
    results = client.request(method, function)

Examples
-------
    client = py7D.APIClient(oauth_consumer_key, 'USA')
    results = client.request('artist', 'search', q='black')
    results = client.request('artist', 'search', q='black', page=1, pageSize=20)
    results = client.request('tag', None)

    client = py7D.APIClient(oauth_consumer_key, 'GB')
    results = client.request('artist', 'details', artistId=263)
    
    OAuth signed request:
    client = py7D.APIClient(oauth_consumer_key, 'USA', secret=oauth_consumer_secret)
    client.oauth_request('user', 'locker', access_token)
    

OAuth
-----
The oauth7digital.py module included has been upgraded from it's original
to use python-oauth2 instead of python-oauth.

The original oauth7digital.py can be found at 
git://github.com/7digital/python-7digital-api.git

Its usage to get an access token remains the same:

    auth = Oauth7digital(CONSUMER_KEY, CONSUMER_SECRET)
    token = auth.request_token()
    authorized = auth.authorize_request_token(token)
    access_token = auth.request_access_token(token)
 
Example Output
--------------
    client.request('artist', 'search', q='pink', pageSize=3)
    print json.dumps(rc, indent=4)

    {
        "@status": "ok", 
        "@xsi:noNamespaceSchemaLocation": "http://api.7digital.com/1.2/static/7digitalAPI.xsd", 
        "@version": "1.2", 
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema", 
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", 
        "searchResults": {
            "page": "1", 
            "pageSize": "3", 
            "totalItems": "211", 
            "searchResult": [
                {
                    "type": "artist", 
                    "score": "2.898118", 
                    "artist": {
                        "@id": "447", 
                        "name": "Pink Floyd", 
                        "sortName": "Pink Floyd", 
                        "url": "http://www.7digital.com/artist/pink-floyd/?partner=3694", 
                        "image": "http://cdn.7static.com/static/img/artistimages/00/000/004/0000000447_150.jpg", 
                        "popularity": "0.73"
                    }
                }, 
                {
                    "type": "artist", 
                    "score": "2.4674335", 
                    "artist": {
                        "@id": "226", 
                        "name": "Pink", 
                        "sortName": "Pink", 
                        "url": "http://www.7digital.com/artist/pink/?partner=3694", 
                        "image": "http://cdn.7static.com/static/img/artistimages/00/000/002/0000000226_150.jpg", 
                        "popularity": "0.71"
                    }
                }, 
                {
                    "type": "artist", 
                    "score": "2.329452", 
                    "artist": {
                        "@id": "7522", 
                        "name": "Pink Martini", 
                        "sortName": "Pink Martini", 
                        "url": "http://www.7digital.com/artist/pink-martini/?partner=3694", 
                        "image": "http://cdn.7static.com/static/img/artistimages/00/000/075/0000007522_150.jpg", 
                        "popularity": "0.5"
                    }
                }
            ]
        }
    }
