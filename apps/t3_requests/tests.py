from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from t3_requests.models import Request
from bs4 import BeautifulSoup
import json


@override_settings(ENABLE_REQUEST_SAVING=True)
class RequestSaverTests(TestCase):
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
        self.client.get(reverse('index'))
        response = self.client.get(reverse('requests'))
        soup = BeautifulSoup(str(response), 'html.parser')
        for i, p in enumerate(soup.find(
                'div', class_='requests').find_all('p')[1:], start=1):
            self.assertIn('query={}'.format(10 - i), p.string)

        self.assertNotIn('query=0', response)
        last_requests = Request.objects.order_by('-created')[:10]
        for req in last_requests:
            self.assertContains(response, str(req))

    def test_https_requests_are_not_saved(self):
        """
        checks if https requests are not saved
        """
        self.assertFalse(Request.objects.exists())
        self.client.get('/', **{'wsgi.url_scheme': 'https'})
        self.assertFalse(Request.objects.exists())

    def test_ajax_request_for_last_requests_is_not_saved(self):
        """
        checks if 'ajax_requests' ajax call is not saved
        """
        self.assertFalse(Request.objects.exists())
        self.client.get(
            reverse('ajax_requests'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertFalse(Request.objects.exists())

    def test_ajax_request_initially_returns_last_requests(self):
        """
        checks if ajax request returns last requests
        """
        for i in range(10):
            self.client.get('/path/', {'query': i})
        response = self.client.get(
            reverse('ajax_requests'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = json.loads(response.content)
        requests = Request.objects.order_by('-created')[:10]
        for req, request in zip(requests, data['requests']):
            self.assertEqual(request['string'], str(req))

    def test_ajax_request_can_return_most_important_requests(self):
        """
        checks if ajax request returns most important requests if called with
        order=priority param
        """
        Request.objects.bulk_create([
            Request(method='GET', path='/', priority=10) for _ in range(10)
        ])
        Request.objects.bulk_create([
            Request(method='GET', path='/recent') for _ in range(10)
        ])
        response = self.client.get(
            reverse('ajax_requests') + '?order=priority',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertNotContains(response, '/recent')
        data = json.loads(response.content)
        requests = Request.objects.order_by('-priority')[:10]
        for req, request in zip(requests, data['requests']):
            self.assertEqual(request['string'], str(req))
