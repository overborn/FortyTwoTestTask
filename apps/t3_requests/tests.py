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

    def requests_page_renders_proper_template(self):
        """
        checks if template is correct
        """
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('requests.html')

    def test_requests_page_renders_last_requests(self):
        """
        checks if last requests are rendered
        """
        for i in range(10):
            self.client.get('/path/', {'query': i})
        response = self.client.get(reverse('requests'))
        soup = BeautifulSoup(str(response), 'html.parser')
        for i, p in enumerate(soup.find_all('p')[1:], start=1):
            self.assertIn('query={}'.format(10-i), p.string)

        self.assertNotIn('query=0', response)
        last_requests = Request.objects.order_by('-created')[:10]
        for req in last_requests:
            self.assertContains(response, str(req))
