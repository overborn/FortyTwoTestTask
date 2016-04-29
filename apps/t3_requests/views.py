from django.shortcuts import render
from t3_requests.models import Request
from jsonview.decorators import json_view
import logging

logger = logging.getLogger(__name__)


@json_view
def requests(request, template='requests.html'):
    order = request.GET.get('order', None) or 'created'
    requests = Request.objects.order_by('-' + order)[:10]
    logger.info(requests)
    if request.is_ajax():
        requests = [{
            'id': r.id,
            'created': r.created.strftime('%Y-%m-%d %H:%M:%S'),
            'method': r.method,
            'path': r.path,
            'query': r.query,
            'priority': r.priority,
            'user': unicode(r.user),
        } for r in requests]
        return {'requests': requests}
    return render(request, template, {'requests': requests})


@json_view
def change_priority(request):
    value = request.GET.get('value')
    request_id = request.GET.get('id')
    request = Request.objects.get(pk=request_id)
    request.priority += int(value)
    request.save()
    logger.info(request)
    return {'status': 'ok'}
