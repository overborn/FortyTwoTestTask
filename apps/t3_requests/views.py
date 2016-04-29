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
        requests = [{'id': r.id, 'string': str(r)} for r in requests]
        return {'requests': requests}
    return render(request, template, {'requests': requests})
