# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.test import TestCase
from django.test.utils import override_settings
from django.template import Context, Template, TemplateSyntaxError
from StringIO import StringIO
from t1_contact.models import Person

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

    def test_admin_links_fails_if_used_with_inappropriate_object(self):
        """
        checks if AttributeError is raised if tag used with string or number
        """
        self.assertRaises(
            AttributeError,
            self.render_template,
            '{% load adminlinks %}'
            '{% edit_link "abc" %}'
        )
        self.assertRaises(
            AttributeError,
            self.render_template,
            '{% load adminlinks %}'
            '{% edit_link 123 %}'
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

    def call(self):
        self.out = StringIO()
        self.err = StringIO()
        return call_command('printmodels', stdout=self.out, stderr=self.err)

    def test_command_traces_deletion_of_instances(self):
        """
        chacks if command traces deletion of instances
        """
        count = Person.objects.count()
        self.call()
        self.assertIn(
            'model Person has {} instances'.format(count),
            self.out.getvalue()
        )
        self.assertIn(
            'error: model Person has {} instances'.format(count),
            self.err.getvalue()
        )
        Person.objects.get(pk=1).delete()
        count2 = Person.objects.count()
        self.assertEqual(count2, count - 1)
        self.call()
        self.assertIn(
            'model Person has {} instances'.format(count2),
            self.out.getvalue()
        )
        self.assertIn(
            'error: model Person has {} instances'.format(count2),
            self.err.getvalue()
        )

    def test_command_traces_addition_of_instances(self):
        """
        chacks if command traces addition of instances
        """
        count = Person.objects.count()
        self.call()
        self.assertIn(
            'model Person has {} instances'.format(count), self.out.getvalue())
        self.assertIn(
            'error: model Person has {} instances'.format(count),
            self.err.getvalue()
        )
        person = Person()
        person.save()
        count2 = Person.objects.count()
        self.assertEqual(count2, count + 1)
        self.call()
        self.assertIn(
            'model Person has {} instances'.format(count2), self.out.getvalue()
        )
        self.assertIn(
            'error: model Person has {} instances'.format(count2),
            self.err.getvalue()
        )


@override_settings(ENABLE_MODEL_LOGGING=True)
class ModelLoggingTests(TestCase):

    def test_saving_and_deleting_creates_model_log_entry(self):
        """
        checks if ModelLogEntry is created after save and delete actions
        """
        count = LogEntry.objects.count()
        person = Person()
        person.save()

        self.assertEqual(LogEntry.objects.count(), count + 1)
        entry = LogEntry.objects.order_by('action_time').last()
        self.assertEqual(entry.action_flag, ADDITION)
        self.assertEqual(
            entry.content_type_id,
            ContentType.objects.get_for_model(Person).id
        )
        person.first_name = 'Name'
        person.last_name = 'Surname'
        person.save()

        self.assertEqual(LogEntry.objects.count(), count + 2)
        entry = LogEntry.objects.order_by('action_time').last()
        self.assertEqual(entry.action_flag, CHANGE)
        self.assertEqual(
            entry.content_type_id,
            ContentType.objects.get_for_model(Person).id
        )
        self.assertEqual(entry.object_repr, 'Name Surname')
        person.delete()

        self.assertEqual(LogEntry.objects.count(), count + 3)
        entry = LogEntry.objects.order_by('action_time').last()
        self.assertEqual(entry.action_flag, DELETION)
        self.assertEqual(
            entry.content_type_id,
            ContentType.objects.get_for_model(Person).id
        )
        self.assertEqual(entry.object_repr, 'Name Surname')
