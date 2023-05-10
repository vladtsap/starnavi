import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class LastActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                request.user.last_activity = datetime.now()
                request.user.save()
            except Exception as e:
                logger.error(e)

        return response
