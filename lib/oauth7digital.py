import httplib
import logging
import os
import re
import sys

import oauth2 as oauth # https://github.com/simplegeo/python-oauth2

class Oauth7digital(object):
    key = None

    SERVER = 'api.7digital.com'
    VERSION = '1.2'
    REQUEST_TOKEN_URL = 'https://%s/%s/oauth/requesttoken' % (SERVER, VERSION)
    ACCESS_TOKEN_URL = 'https://%s/%s/oauth/accesstoken' % (SERVER, VERSION)
    AUTHORIZATION_URL = 'https://account.7digital.com/%s/oauth/authorise'
    LOGGER_NAME = 'Oauth7Digital.log'

    def __init__(self, key, secret, access_token = None,
                 log_dir=None, log_name=None, log_level=logging.DEBUG):
        self.key = key
        self.secret = secret
        self.access_token = access_token

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        if log_dir and log_name:
            log_fd = open(os.path.join(log_dir, log_name))
            self.logger.addHandler(logging.StreamHandler(log_fd))

    def _consumer(self):
        return oauth.Consumer(self.key, self.secret)

    def _token_from_response_content(self, content):
        key = re.search(
            "<oauth_token>(\w.+)</oauth_token>",
            content).groups()[0]
        secret = re.search(
            "<oauth_token_secret>(\w.+)</oauth_token_secret>",
            content).groups()[0]

        return oauth.Token(key, secret)

    def request_token(self):
        self.logger.info('\nOAUTH STEP 1')

        client = oauth.Client(self._consumer())
        response, content = client.request(
            self.REQUEST_TOKEN_URL,
            headers = {"Content-Type":"application/x-www-form-urlencoded"}
        )

        return self._token_from_response_content(content)

    def authorize_request_token(self, token):
        keyed_auth_url = self.AUTHORIZATION_URL % self.key
        self.logger.info('\nOAUTH STEP 2')
        auth_url="%s?oauth_token=%s" % (keyed_auth_url, token.key)

        # auth url to go to
        self.logger.info('Authorization URL:\n%s' % auth_url)
        oauth_verifier = raw_input('Please go to the above URL and authorize the app. Hit return when you have been authorized: ')
        return True

    def request_access_token(self, token):
        self.logger.info('\nOAUTH STEP 3')
        client = oauth.Client(self._consumer(), token=token)
        response, content = client.request(
                self.ACCESS_TOKEN_URL,
                headers={"Content-Type":"application/x-www-form-urlencoded"}
        )
        return self._token_from_response_content(content)

    def request(self, url):
        ''' Once you have an access_token authorized by a customer,
            execute a request on their behald
        '''
        client = oauth.Client(self._consumer(), token=self.access_token)
        response = client.request(
                url,
                headers={"Content-Type":"application/x-www-form-urlencoded"}
        )

        return response
