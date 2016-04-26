from t3_requests.models import Request
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class RequestSaver(object):

    def process_request(self, request):
        if getattr(settings, 'ENABLE_REQUEST_SAVING', False):
            if (not request.is_ajax() and
                    request.path not in settings.IGNORE_URLS):
                if not request.is_secure():
                    req = Request(
                        method=request.method,
                        path=request.path,
                        query=request.META.get('QUERY_STRING', '?'),
                        user=request.user)
                    req.save()
                    logger.info(req)
        pass
