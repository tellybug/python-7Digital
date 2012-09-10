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
key name preceded by the '@' character. For example, the id attribute on the track node
would convert to {'track' : {'@id' : 123, ...}}


Usage
-----
    # set your oauth_consumer_key, oauth_consumer_secret, and country in the api_settings.py module.
    import py7D
    results = py7D.request(method, function, page=1, pageSize=10)
    results = py7D.request(method, function)

Examples
-------
    results = py7D.request('artist', 'search', q='black')
    results = py7D.request('artist', 'search', q='black', page=1, pageSize=20)
    results = py7D.request('tag', None)

    results = py7D.request('artist', 'details', artistId=263)
    
    OAuth signed request:
    py7D.oauth_request('user', 'locker', access_token)
    

OAuth
-----
The oauth7digital.py module included has been upgraded from it's original
to use python-oauth2 instead of python-oauth. It also looks for its settings in the api_settings module. 

The original oauth7digital.py can be found at 
git://github.com/7digital/python-7digital-api.git

Its usage to get an access token:

    import oauth7digital as oa7d
    token = oa7d.request_token()
    authorized = oa7d.authorize_request_token(token)
    access_token = oa7d.request_access_token(token)
 
Example Output
--------------
    resp = py7D.request('artist', 'search', q='pink', pageSize=3)
    >>> resp.keys()
    [u'response', 'http_headers']
    
    print json.dumps(resp['response'], indent=4)

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

    >>> pprint(resp['http_headers'])
    {'accept-ranges': 'bytes',
     'access-control-allow-origin': '*',
     'age': '0',
     'cache-control': 'private, max-age=60',
     'connection': 'Keep-Alive',
     'content-length': '1388',
     'content-location': 'https://api.7digital.com/1.2/artist/search?....', #edited for README
     'content-type': 'text/xml; charset=utf-8',
     'date': 'Sat, 08 Sep 2012 18:44:11 GMT',
     'expires': 'Sat, 08 Sep 2012 18:45:11 GMT',
     'last-modified': 'Sat, 08 Sep 2012 18:44:06 GMT',
     'server': 'nginx/0.7.67',
     'set-cookie': ...', #edited for README
     'status': '200',
     'x-7dig': 'aw0',
     'x-aspnet-version': '4.0.30319',
     'x-cdn': 'Served by WebAcceleration',
     'x-ratelimit-current': '24',
     'x-ratelimit-limit': '4000',
     'x-ratelimit-reset': '18953'}
        