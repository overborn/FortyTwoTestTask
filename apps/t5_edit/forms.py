from django.core.urlresolvers import reverse
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, HTML
from t1_contact.models import Person
from t5_edit.widgets import Datepicker

PHOTO_HTML = '''
{% if form.photo.value %}
    <img src="{{ MEDIA_URL }}{{ form.photo.value }}">
{% endif %}
'''


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'date_of_birth': Datepicker
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        photo_layout = Layout(
            'photo',
            HTML(PHOTO_HTML)
        )
        self.helper.layout = Layout(
            Div(
                Div('first_name', css_class='col-md-6 col-xs-12'),
                Div('email', css_class='col-md-6 col-xs-12'),
                css_class='row'
            ),
            Div(
                Div('last_name', css_class='col-md-6 col-xs-12'),
                Div('skype', css_class='col-md-6 col-xs-12'),
                css_class='row'
            ),
            Div(
                Div('date_of_birth', css_class='col-md-6 col-xs-12'),
                Div('jabber', css_class='col-md-6 col-xs-12'),
                css_class='row'
            ),
            Div(
                Div(photo_layout, css_class='col-md-6 col-xs-12'),
                Div('other_contacts', 'bio', css_class='col-md-6 col-xs-12'),
                css_class='row'
            ),
            HTML('''
            <input type="submit" class="btn btn-primary" value="Save">
            <a href="{% url 'index' %}" class="btn btn-default">cancel</a>
            ''')

        )
        self.helper.form_action = reverse('ajax_save')
        self.helper.form_id = 'personForm'
