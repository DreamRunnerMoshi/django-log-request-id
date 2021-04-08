from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests import Session as BaseSession

from nhst_log_request_id import DEFAULT_NO_REQUEST_ID, DEFAULT_REQUEST_ID_PROPERTY_NAME, OUTGOING_REQUEST_ID_HEADER_SETTING, REQUEST_ID_HEADER_SETTING, REQUEST_ID_PROPERTY_NAME_SETTING, local


class Session(BaseSession):
    def __init__(self, *args, **kwargs):
        if hasattr(settings, OUTGOING_REQUEST_ID_HEADER_SETTING):
            self.request_id_header = getattr(settings, OUTGOING_REQUEST_ID_HEADER_SETTING)
        elif hasattr(settings, REQUEST_ID_HEADER_SETTING):
            self.request_id_header = getattr(settings, REQUEST_ID_HEADER_SETTING)
        else:
            raise ImproperlyConfigured("The %s or %s settings must be configured in "
                                       "order to use %s" % (
                                           OUTGOING_REQUEST_ID_HEADER_SETTING,
                                           REQUEST_ID_HEADER_SETTING, __name__
                                       ))
        super(Session, self).__init__(*args, **kwargs)

    def prepare_request(self, request):
        """Include the request ID, if available, in the outgoing request"""
        try:
            request_id_property_name = getattr(settings, REQUEST_ID_PROPERTY_NAME_SETTING, DEFAULT_REQUEST_ID_PROPERTY_NAME)
            if self.request_id_header:
                request.headers[self.request_id_header] = getattr(local,request_id_property_name,DEFAULT_NO_REQUEST_ID)
        except AttributeError:
            pass

        return super(Session, self).prepare_request(request)
