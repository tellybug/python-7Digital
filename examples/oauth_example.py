import py7D

''' 
    How to get an access token: 
        auth = Oauth7digital(CONSUMER_KEY, CONSUMER_SECRET)
        token = auth.request_token()
        authorized = auth.authorize_request_token(token)
        access_token = auth.request_access_token(token)
'''

def get_locker(access_token):
    resp = py7D.oauth_request('user', 'locker', access_token=access_token)
    return resp
