import httplib2
import os
import urllib
import re
import urlparse
import xmltodict
import collections

import oauth7digital as oa7D
import api_settings

__name__ = 'py7D'
__doc__ = 'A lightweight python interface to 7Digital web service'
__author__ = 'Jason Rubenstein'
__version__ = '0.1.0'
__maintainer__ = 'Jason Rubenstein'
__email__ = 'jasondrubenstein@gmail.com'
__status__ = 'Beta'

API_VERSION = '1.2'
API_URL = 'https://api.7digital.com/%s' % API_VERSION
PREVIEW_URL = '%s/track/preview?oauth_consumer_key=%s&trackid=%s&' % (
                                                    API_URL, "%s", "%s")

class APIServiceException(Exception):
    pass


class APIClientException(Exception):
    pass


def _assemble_url(host, method, function, oauth, **kwargs):
    data = []

    for k,v in kwargs.iteritems():
        if isinstance(v, (int, float, long)):
            kwargs[k] = str(v)

    quote = lambda _param_name: urllib.quote_plus(
                        _param_name.replace('&amp;', '&').encode('utf8')
    )

    for name in kwargs.keys():
        data.append('='.join((name, quote(kwargs[name]))))

    data = '&'.join(data)

    url = os.path.join(host, method)
    if function:
        url = os.path.join(url, function)

    if not oauth:
        url = "%s%s" % (url, '?oauth_consumer_key=%s&country=%s' % (
                                                        api_settings.oauthkey,
                                                        api_settings.country)
                       )
    if data:
        url += "&%s" % data

    return url


def _execute(method, function, access_token=None, **kwargs):
    oauth = True if access_token else False

    dc = kwargs.pop('dict_constructor', None) or collections.OrderedDict

    url = _assemble_url(API_URL, method, function, oauth, **kwargs)

    if access_token:
        http_response, content = oa7D.request(url, access_token)
        api_response = xmltodict.parse(
            content, xml_attribs=True, dict_constructor=dc)
    else:
        http_response, content = httplib2.Http().request(url)
        api_response = xmltodict.parse(
            content, xml_attribs=True, dict_constructor=dc)

    if api_response['response']['@status'] == "error":
        raise APIServiceException('Error code %s: %s' % (
                api_response['response']['error']['@code'],
                api_response['response']['error']['errorMessage']
                )
        )

    api_response['http_headers'] = http_response
    return api_response


def request(method, function, **kwargs):
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

    return _execute(method, function, **kwargs)


def oauth_request(method, function, access_token, **kwargs):
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

    return _execute(method, function, access_token, **kwargs)


def preview_url(track_id):
    ''' construct a preview url for a track identified by its
        track_id.

        Input:
            valid track_id

        Output:
            The preview URL for that track (str)
    '''
    return PREVIEW_URL % (api_settings.oauthkey, track_id)
