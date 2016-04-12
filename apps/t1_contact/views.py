from django.shortcuts import render, get_object_or_404
from t1_contact.models import Person


def index(request, template='index.html'):
    person = get_object_or_404(Person, pk=1)
    return render(request, template, {'person': person})
