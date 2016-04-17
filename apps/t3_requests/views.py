from django.shortcuts import render
from t3_requests.models import Request
from jsonview.decorators import json_view


def requests(request, template='requests.html'):
    last_requests = Request.objects.order_by('-created')[:10]
    return render(request, template, {'requests': last_requests})


@json_view
def ajax_requests(request):
    requests = Request.objects.order_by('-created')[:10]
    requests = [{'id': r.id, 'string': str(r)} for r in requests]
    return {'requests': requests}
