from django.core.urlresolvers import reverse
from django.test import TestCase
from t3_requests.models import Request
from bs4 import BeautifulSoup


class RequestTests(TestCase):
    def test_request_creates_request_object(self):
        '''
        checks if http requests are saved
        '''
        self.assertFalse(Request.objects.exists())
        self.client.get('/path', {'query': 'foo'})
        self.assertTrue(Request.objects.exists())
        req = Request.objects.get(pk=1)
        self.assertEqual(req.method.upper(), 'GET')
        self.assertEqual(req.path, '/path')
        self.assertEqual(req.query, 'query=foo')

    def test_https_requests_are_not_saved(self):
        '''
        checks if https requests are not saved
        '''
        self.assertFalse(Request.objects.exists())
        self.client.get('/path',  {'query': 'foo'}, secure=True)
        self.assertFalse(Request.objects.exists())

    def test_requests_page_renders_requests(self):
        for i in range(10):
            self.client.get('/path/', {'query': i})
        response = self.client.get(reverse('requests'))
        soup = BeautifulSoup(str(response), 'html.parser')
        print response
        for i, p in enumerate(soup.find_all('p')):
            assert 'query={}'.format(i+1) in p.string

        self.assertNotIn('query=0', response)
