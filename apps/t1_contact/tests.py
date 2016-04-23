# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from t1_contact.models import Person


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


class ViewTests(TestCase):

    def setUp(self):
        self.person = PERSON

    def test_index_uses_index_template(self):
        """
        checks if template is correct
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_index_contains_persons_data(self):
        """
        checks if index view contains proper data
        """
        response = self.client.get(reverse('index'))
        for key, value in self.person.iteritems():
            if '\r\n' in value:
                for line in value.split('\r\n'):
                    self.assertContains(response, line.strip(' \n\r'))
            else:
                self.assertContains(response, value)


class AdminTests(TestCase):
    fixtures = ['initial_data.json']

    def test_admin_is_created_from_fixtures(self):
        """
        check if admin exists with admin:admin credentials
        """
        user = User.objects.get(pk=1)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.check_password('admin'))


class ModelTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.person = PERSON

    def test_person_is_created_from_fixures(self):
        """
        check if person with given contacts exists
        """
        person = Person.objects.get(pk=1)
        for key, value in self.person.iteritems():
            self.assertEqual(value, str(getattr(person, key)))


class ModelViewTests(TestCase):
    fixtures = ['initial_data.json']

    def test_index_displays_proper_person_model(self):
        """
        checks if correct instance of person model is shown in view
        also checks if model accepts unicode
        """
        person = Person.objects.get(pk=1)
        old_name = person.first_name
        response = self.client.get(reverse('index'))
        self.assertContains(response, old_name)
        person.first_name = "New_name"
        person.save()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, old_name)
        self.assertContains(response, person.first_name)

    def test_model_and_view_work_with_unicode(self):
        """
        fails if unicode characters are not handled
        """
        person = Person.objects.get(pk=1)
        person.first_name = u"Юникод"
        person.save()
        response = self.client.get(reverse('index'))
        self.assertContains(response, person.first_name)

    def test_index_does_not_display_attrs_of_deleted_person(self):
        """
        checks that if person is deleted, none of its attrs will be displayed
        in index view
        """
        person = Person.objects.get(pk=1)
        person.delete()
        response = self.client.get(reverse('index'))
        for key in PERSON:
            self.assertNotContains(response, PERSON[key])

    def test_index_displays_attrs_of_certain_instance(self):
        """
        checks if attrs of proper instance are displayed in index, if more
        then one exists
        """
        person = Person.objects.get(pk=1)
        old_name = person.first_name
        person.pk = None
        person.first_name = "New_name"
        person.save()
        response = self.client.get(reverse('index'))
        self.assertContains(response, old_name)
        self.assertNotContains(response, "New_name")
