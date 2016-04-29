from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form
from t5_edit.forms import PersonForm
from t1_contact.models import Person
import logging

logger = logging.getLogger(__name__)


@login_required
def edit(request, template='edit.html'):
    person = Person.objects.first()
    if not person:
        logger.info('No person was found')
    form = PersonForm(instance=person)
    return render(request, template, {'form': form})


@json_view
def ajax_save(request):
    person = Person.objects.first()
    if not person:
        logger.info('No person was found')
    form = PersonForm(request.POST, request.FILES, instance=person)
    if form.is_valid():
        form.save()
        logger.info({field: form[field].value() for field in form.fields})
        return {'success': True}
    logger.info({e: form.errors[e] for e in form.errors})
    request_context = RequestContext(request)
    helper = form.helper
    helper.form_tag = False
    html = render_crispy_form(form, context=request_context, helper=helper)
    return {'success': False, 'form_html': html}


def logout_view(request):
    logout(request)
    return redirect('index')
