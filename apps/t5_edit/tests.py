# -*- coding: utf-8 -*-
import tempfile
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from t1_contact.models import Person
from t1_contact.tests import PERSON
from copy import copy
import HTMLParser


AUTH_CREDS = {'username': 'admin', 'password': 'admin'}


class EditViewTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.person = copy(PERSON)

    def test_edit_view_redirects_to_login_if_no_auth(self):
        """
        checks if template is correct
        """
        response = self.client.get(reverse('edit'), follow=True)
        self.assertRedirects(
            response, '{}?next=/edit/'.format(reverse('login')))
        self.assertTemplateUsed('login.html')

    def test_edit_view_contains_persons_data(self):
        """
        checks if edit view contains proper data
        """
        self.client.login(**AUTH_CREDS)
        response = self.client.get(reverse('edit'))
        response_text = HTMLParser.HTMLParser().unescape(response.content)
        for key, value in self.person.iteritems():
            if '\r\n' in value:
                for line in value.split('\r\n'):
                    self.assertIn(line.strip(' \n\r'), response_text)
            else:
                self.assertContains(response, value)


class EditFormTests(TestCase):
    def setUp(self):
        self.person = copy(PERSON)
        self.client.login(**AUTH_CREDS)

    def test_ajax_post_saves_person(self):
        """
        checks if ajax post saves person and returns {'success': True}
        """
        self.assertTrue(Person.objects.count(), 0)
        response = self.client.post(reverse('ajax_save'), self.person)
        person = Person.objects.get(pk=1)
        for field in self.person:
            self.assertEqual(self.person[field], str(getattr(person, field)))
        data = json.loads(response.content)
        self.assertEqual(data['success'], True)

    def test_ajax_changes_person(self):
        """
        checks if ajax post changes person and returns {'success': True}
        """
        self.person['first_name'] = 'name'
        response = self.client.post(reverse('ajax_save'), self.person)
        person = Person.objects.get(pk=1)
        for field in self.person:
            self.assertEqual(self.person[field], str(getattr(person, field)))
        data = json.loads(response.content)
        self.assertEqual(data['success'], True)

    def test_ajax_post_validate_broken_data(self):
        """
        checks if ajax post don't save broken data and returns form with errors
        """
        self.person['email'] = 'not_mail'
        self.person['first_name'] = ''
        response = self.client.post(reverse('ajax_save'), self.person)
        person = Person.objects.get(pk=1)
        self.assertNotEqual(self.person['email'], person.email)
        self.assertNotEqual(self.person['first_name'], person.first_name)
        data = json.loads(response.content)
        self.assertEqual(data['success'], False)
        self.assertIn('Enter a valid email address', data['form_html'])
        self.assertIn('This field is required', data['form_html'])


class DatepickerTests(TestCase):
    fixtures = ['initial_data.json']

    def test_view_contains_proper_static(self):
        """
        checks if static files for displaying datepicker are in view
        """
        self.client.login(**AUTH_CREDS)
        response = self.client.get(reverse('edit'))
        self.assertContains(response, "js/jquery-ui.js")
        self.assertContains(response, "js/datepicker.js")
        self.assertContains(response, "css/jquery-ui.css")


class PhotoTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.person = copy(PERSON)
        self.client.login(**AUTH_CREDS)

    def test_photo_is_rendered_when_added(self):
        """
        checks if photo is rendered in index and edit views when added to model
        """
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'No photo yet')
        self.assertNotContains(response, 'test.png')

        response = self.client.get(reverse('edit'))
        self.assertNotContains(response, 'test.png')

        person = Person.objects.get(pk=1)
        person.photo = tempfile.NamedTemporaryFile(suffix="test.png").name
        person.save()

        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'No photo yet')
        self.assertContains(response, 'test.png')
