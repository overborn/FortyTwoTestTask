from t3_requests.models import Request
from django.conf import settings

IGNORE = (
    '/ajax_requests/',
    '/requests/'
)


class RequestSaver(object):

    def process_request(self, request):
        if getattr(settings, 'ENABLE_REQUEST_SAVING', False):
            if not (request.is_ajax() or request.path in IGNORE):
                if not request.is_secure():
                    req = Request(
                        method=request.method,
                        path=request.path,
                        query=request.META.get('QUERY_STRING', '?'))
                    req.save()
        pass
