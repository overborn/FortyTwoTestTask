from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from t5_edit.forms import PersonForm
from t1_contact.models import Person


def edit(request, template='edit.html'):
    person = get_object_or_404(Person, pk=1)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
        else:
            return render(request, 'edit.html', {'form': form})
    form = PersonForm(instance=person)
    return render(request, template, {'form': form})
