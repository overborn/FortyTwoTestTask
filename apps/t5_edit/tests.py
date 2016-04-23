# -*- coding: utf-8 -*-
import tempfile
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from t1_contact.models import Person
from copy import copy

PERSON = {
    "bio": """2015 - present: Programmer Analyst at Alfa Bank\r
2012 - 2015: Teacher of Economics at "Leader" lyceum\r
2009 - 2013: Bachelor's degree in Economic Cybernetics at\r
Taras Shevchenko National Univercity of Kyiv""",
    "first_name": "Kyrylo",
    "last_name": "Budko",
    "other_contacts": "phone: +380937123775",
    "date_of_birth": "1992-05-13",
    "skype": "kyrylo.budko",
    "jabber": "overborn@42cc.co",
    "email": "forkirill@i.ua"
}


class EditViewTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.person = copy(PERSON)

    def test_edit_view_renders_proper_template(self):
        """
        checks if template is correct
        """
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('edit.html')

    def test_edit_view_contains_persons_data(self):
        """
        checks if edit view contains proper data
        """
        response = self.client.get(reverse('index'))
        for key, value in self.person.iteritems():
            if '\r\n' in value:
                for line in value.split('\r\n'):
                    self.assertContains(response, line.strip(' \n\r'))
            else:
                self.assertContains(response, value)


class EditFormTests(TestCase):
    def setUp(self):
        self.person = copy(PERSON)

    def test_edit_post_saves_and_redirects(self):
        """
        checks if edit post request saves data and redirects to index
        """
        response = self.client.post(reverse('edit'), self.person, follow=True)
        person = Person.objects.get(pk=1)
        for field in self.person:
            self.assertEqual(self.person[field], str(getattr(person, field)))
        self.assertRedirects(response, reverse('index'))

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

    def test_edit_post_changes_data(self):
        """
        checks if edit view changes model data
        """
        old_name = self.person["first_name"]
        self.person["first_name"] = "name"
        self.client.post(reverse('edit'), self.person, follow=True)
        person = Person.objects.get(pk=1)
        self.assertNotEqual(person.first_name, old_name)
        self.assertEqual(person.first_name, "name")


class DatepickerTests(TestCase):
    fixtures = ['initial_data.json']

    def test_view_contains_proper_static(self):
        """
        checks if static files for displaying datepicker are in view
        """
        response = self.client.get(reverse('edit'))
        self.assertContains(response, "js/jquery-ui.js")
        self.assertContains(response, "js/datepicker.js")
        self.assertContains(response, "css/jquery-ui.css")


class PhotoTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.person = copy(PERSON)

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
