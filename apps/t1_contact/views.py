from django.shortcuts import render
from t1_contact.models import Person


def index(request, template='index.html'):
    try:
        person = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        person = None
    return render(request, template, {'person': person})
