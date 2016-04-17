from django.core.urlresolvers import reverse
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


class EditViewTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.person = PERSON

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
        self.person = PERSON

    def test_edit_post_saves_and_redirects(self):
        """
        checks if edit post request saves data and redirects to index
        """
        response = self.client.post(reverse('edit'), self.person, follow=True)
        person = Person.objects.get(pk=1)
        for field in self.person:
            self.assertEqual(self.person[field], str(getattr(person, field)))
        self.assertRedirects(response, reverse('index'))

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
