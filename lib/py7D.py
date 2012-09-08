import os
import urllib
import urllib2
import re
import urlparse
import xmltodict

from oauth7digital import Oauth7digital

__name__ = 'py7D'
__doc__ = 'A lightweight python interface to 7Digital web service'
__author__ = 'Jason Rubenstein'
__version__ = '0.0.1'
__maintainer__ = 'Jason Rubenstein'
__email__ = 'jason@mypono.com'
__status__ = 'Alpha'

API_VERSION = '1.2'
API_URL = 'https://api.7digital.com/%s' % API_VERSION
PREVIEW_URL = '%s/track/preview?oauth_consumer_key=%s&trackid=%s&' % (
                                                    API_URL, "%s", "%s")

class APIServiceExeption(Exception):
    pass

class APIClientException(Exception):
    pass

class APIClient(object):
    ''' The API client with which requests will be made.

        Input:
            OAUTHkey : your 7Digital oauth_consumer_key
            country  : the ISO code for your country, or None
    '''

    def __init__(self, OAUTHKey, country, **kwargs):
        '''  Requires:
                OAUTHKey    : your valid 7Digital consumer_oauth_key
                country     : an ISO country code.
        '''
        self.oauthkey = OAUTHKey
        self.country = country
        self.secret = kwargs.get('secret')

    def _assemble_url(self, host, method, function, oauth, **kwargs):
        data = []

        for k,v in kwargs.iteritems():
            if isinstance(v, (int, float, long)):
                kwargs[k] = str(v)

        quote = lambda _param_name: urllib.quote_plus(
                            _param_name.replace('&amp;', '&').encode('utf8'))

        for name in kwargs.keys():
            data.append('='.join((name, quote(kwargs[name]))))
        data = '&'.join(data)

        url = os.path.join(host, method)
        if function:
            url = os.path.join(url, function)

        if not oauth:
            url = "%s%s" % (url, '?oauth_consumer_key=%s&country=%s' % (
                                                                self.oauthkey,
                                                                self.country))
        if data:
            url += "&%s" % data

        return url

    def _execute(self, method, function, access_token=None, **kwargs):
        oauth = True if access_token else False
        url = self._assemble_url(API_URL, method, function, oauth, **kwargs)

        if access_token:
            oa7d = Oauth7digital(self.oauthkey,
                                 self.secret,
                                 access_token)
            response, content = oa7d.request(url)

            api_response = xmltodict.parse(content, xml_attribs=True)
        else:
            fd = urllib2.urlopen(url)
            api_response = xmltodict.parse(fd, xml_attribs=True)

        if api_response['response']['@status'] == "error":
            raise APIServiceExeption('Error code %s: %s' % (
                    api_response['response']['error']['@code'],
                    api_response['response']['error']['errorMessage'])
            )

        return api_response['response']

    def request(self, method, function, **kwargs):
        ''' Input:
                method      : a valid 7Digital method
                function    : a valid function for the method
                page        : an optional page number
                pageSize    : an optional page size

            Output:
                A python Ordered Dictionary of the results of the
                API, converted from XML.
        '''
        if kwargs.get('access_token'):
            raise APIClientException(
                "Please use oauth_request() for calls containing access_token")

        return self._execute(method, function, **kwargs)


    def oauth_request(self, method, function, access_token, **kwargs):
        ''' Input:
                method      : a valid 7Digital method
                function    : a valid function for the method
                access_token: if oauth is True, provide the access_token
                page        : an optional page number
                pageSize    : an optional page size

            Output:
                A python Ordered Dictionary of the results of the
                API, converted from XML.
        '''
        if not access_token:
            raise APIClientException("access_token required for oauth request")

        return self._execute(method, function, access_token, **kwargs)

    def preview_url(self, track_id):
        ''' construct a preview url for a track identified by its
            track_id.

            Input:
                valid track_id

            Output:
                The preview URL for that track (str)
        '''
        return PREVIEW_URL % (self.oauthkey, track_id)

