from django.shortcuts import render
from t3_requests.models import Request


def requests(request, template='requests.html'):
    last_requests = Request.objects.order_by('-created')[:10]
    return render(request, template, {'requests': last_requests})
