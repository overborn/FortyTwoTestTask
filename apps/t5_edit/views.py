from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template import RequestContext
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form
from t5_edit.forms import PersonForm
from t1_contact.models import Person


@login_required
def edit(request, template='edit.html'):
    person = Person.objects.filter(pk=1).first()
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
        else:
            return render(request, 'edit.html', {'form': form})
    form = PersonForm(instance=person)
    return render(request, template, {'form': form})


@json_view
def ajax_save(request):
    person = Person.objects.filter(pk=1).first()
    form = PersonForm(request.POST, request.FILES, instance=person)
    if form.is_valid():
        form.save()
        return {'success': True}
    request_context = RequestContext(request)
    helper = form.helper
    helper.form_tag = False
    html = render_crispy_form(form, context=request_context, helper=helper)
    return {'success': False, 'form_html': html}


def logout_view(request):
    logout(request)
    return redirect('index')
