from django import template
from django.core.urlresolvers import reverse

register = template.Library()


class EditLinkNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        obj = self.obj.resolve(context)
        link = reverse("admin:{}_{}_change".format(
            obj._meta.app_label,
            obj._meta.module_name
        ), args=(obj.id,))
        return '<a href="{}">edit ({})</a>'.format(link, obj)


@register.tag
def edit_link(parser, token):
    token = token.split_contents()
    try:
        obj = token[1]
    except IndexError:
        raise template.TemplateSyntaxError, \
            "{} tag requires an object as first argument".format(token[0])

    return EditLinkNode(obj)
