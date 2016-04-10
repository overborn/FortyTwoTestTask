from django.core.urlresolvers import reverse
from django.test import TestCase


PERSON = {
    "bio": """2015 - present: Programmer Analyst at Alfa Bank\r\n
        2012 - 2015: Teacher of Economics at \"Leader\" lyceum\r\n
        2009 - 2013: Bachelor's degree in Economic Cybernetics at\r\n
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
        """checks if template is correct"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_index_contains_persons_data(self):
        """checks if index view contains proper data"""
        response = self.client.get(reverse('index'))
        for key, value in self.person.iteritems():
            if '\r\n' in value:
                for line in value.split('\r\n'):
                    self.assertContains(response, line.strip(' \n\r'))
            else:
                self.assertContains(response, value)
