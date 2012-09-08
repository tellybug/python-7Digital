import py7D

''' 
    How to get an access token:
        import oauth7digital as oa7d
        token = oa7d.request_token()
        authorized = oa7d.authorize_request_token(token)
        access_token = oa7d.request_access_token(token)
'''

def get_locker(access_token):
    resp = py7D.oauth_request('user', 'locker', access_token=access_token)
    return resp
