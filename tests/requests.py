import py7D
import unittest

CONSUMER_OAUTH_KEY='' # your consumer oauth key here
COUNTRY = '' # your ISO country string here

class RequestTest(unittest.TestCase):
    def setUp(self):
        self.client = py7D.APIClient(CONSUMER_OAUTH_KEY, COUNTRY)

    def testApi(self):
        response = self.client.request('status', None)
        assert response['@status'] == 'ok', (
                "API Status error. Response: %s" % response)
    
    def testArtistSearch(self):
        ''' test that the client works using an arbitrary API. 
            In this case, use artist search.
        '''
        response = self.client.request('artist', 'search', q='Pink')
        assert response['@status'] == 'ok', (
                "API Status error. Response: %s" % response)        

    def tearDown(self):
        del self.client

if __name__ == '__main__':
    unittest.main()
