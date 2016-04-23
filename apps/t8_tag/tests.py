from django.core.urlresolvers import reverse
from django.test import TestCase
from django.template import Context, Template, TemplateSyntaxError

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
