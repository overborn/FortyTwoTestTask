from t3_requests.models import Request
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class RequestSaver(object):

    def process_request(self, request):
        if not getattr(settings, 'ENABLE_REQUEST_SAVING', False):
            return

        if request.is_ajax() or request.path in settings.IGNORE_URLS:
            return

        if request.is_secure():
            return

        req = Request(
            method=request.method,
            path=request.path,
            query=request.META.get('QUERY_STRING', '?'),
            user=request.user)
        req.save()
        logger.info(req)
