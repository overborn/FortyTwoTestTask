from django.shortcuts import render
from t1_contact.models import Person
import logging

logger = logging.getLogger(__name__)


def index(request, template='index.html'):
    person = Person.objects.first()
    if not person:
        logger.info('No person was found')
    return render(request, template, {'person': person})
