import py7D
import unittest

class RequestTest(unittest.TestCase):

    def testApi(self):
        response = py7D.request('status', None)
        assert response['response']['@status'] == 'ok', (
                "API Status error. Response: %s" % response)
    
    def testArtistSearch(self):
        ''' test that the client works using an arbitrary API. 
            In this case, use artist search.
        '''
        response = py7D.request('artist', 'search', q='Pink')
        assert response['response']['@status'] == 'ok', (
                "API Status error. Response: %s" % response)        


if __name__ == '__main__':
    unittest.main()
