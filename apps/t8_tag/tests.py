from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.conf import settings
from django.test import TestCase
from django.template import Context, Template, TemplateSyntaxError
from StringIO import StringIO
from t1_contact.models import Person
import os
import time
import subprocess

LINK_TO_ADMIN = '<a href="/admin/auth/user/1/">edit (admin)</a>'

AUTH_CREDS = {'username': 'admin', 'password': 'admin'}


class AdminLinksTests(TestCase):
    fixtures = ['initial_data.json']

    def render_template(self, string, context={}):
        context = Context(context)
        return Template(string).render(context)

    def test_admin_links_rendered_correctly(self):
        """
        checks if admin link tag renders link to admin edit page
        """
        from django.contrib.auth.models import User
        user = User.objects.get(username='admin')
        rendered = self.render_template(
            '{% load adminlinks %}'
            '{% edit_link user %}',
            {'user': user}
        )
        self.assertEqual(rendered, LINK_TO_ADMIN)

    def test_admin_links_fails_if_used_without_object(self):
        """
        checks if TemplateSyntaxError is raised if tag contains no object
        """
        self.assertRaises(
            TemplateSyntaxError,
            self.render_template,
            '{% load adminlinks %}'
            '{% edit_link %}'
        )

    def test_link_is_shown_to_authenticated_users_only(self):
        """
        checks if link is displayed only to authenticated_users
        """
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, LINK_TO_ADMIN)
        self.client.login(**AUTH_CREDS)
        response = self.client.get(reverse('index'))
        self.assertContains(response, LINK_TO_ADMIN)


class CommandTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()

    def call(self):
        return call_command('printmodels', stdout=self.out, stderr=self.err)

    def test_command(self):
        self.call()
        self.assertIn('model Person has 1 instances', self.out.getvalue())
        self.assertIn(
            'error: model Request has 0 instances', self.err.getvalue())

    def test_command_traces_number_of_instances(self):
        count = Person.objects.count()
        self.call()
        self.assertIn(
            'model Person has {} instances'.format(count), self.out.getvalue())
        person = Person()
        person.save()
        count2 = Person.objects.count()
        self.assertEqual(count2, count + 1)
        self.out = StringIO()
        self.call()
        self.assertIn(
            'model Person has {} instances'.format(count2), self.out.getvalue()
        )

    def test_script_creates_file_with_stderr_output(self):
        """
        checks if bash script creates file with output of printmodels command
        """
        script = os.path.join(settings.BASE_DIR, "printmodels.sh")
        os.chmod(script, 0o755)
        subprocess.call(script)
        name = "{}.dat".format(time.strftime("%d-%m-%Y"))
        name = os.path.join(settings.BASE_DIR, name)
        self.assertTrue(os.path.isfile(name))
        count = Person.objects.count()
        self.assertIn(
            'error: model Person has {} instances'.format(count),
            open(name).read()
        )
