from django.conf import settings

from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.views import exception_handler
from rest_framework import status


def log_exception(exc):
    log_data = {}
    if hasattr(exc, 'log_data'):
        log_data = exc.log_data

    if settings.DEBUG:
        print("\n--- Exception ---")
        print(exc.detail, "\n log_data: ", log_data)
        print("")

    print(exc.detail, extra={"log_data": log_data})


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data.pop('detail')
        response.data['error'] = {
            'status_code': response.status_code,
            'detail': detail
        }

        if exc.detail_data is not None:
            response.data['error']['detail_data'] = exc.detail_data

        log_exception(exc)

    return response


class RecordNotFoundException(APIException):
    status_code = 500
    default_detail = 'Record not found.'
    default_code = 'record_not_found'


class DuplicateRemoteKeyException(APIException):
    status_code = 500
    default_detail = 'Remote key already exists.'
    default_code = 'duplicate_remote_key'


class BaseException(APIException):

    def __init__(self, detail=None, detail_data=None, code=None, log_data={}):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)
        self.detail_data = detail_data
        self.log_data = log_data


class RequestDataValidationException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Request data is invalid.'
    default_code = 'request_data_invalid'


class ServiceTimeoutException(BaseException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    default_detail = 'Service timed out.'
    default_code = 'service_time_out'


class ServiceUnauthorizedException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Service call unauthorized.'
    default_code = 'service_unauthorized'


class ServiceForbiddenException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Service call forbidden.'
    default_code = 'service_forbidden'


class ServiceNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Service not found.'
    default_code = 'service_not_found'


class ServiceErrorException(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Service has error response'
    default_code = 'service_error_response'


class ServiceDownException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Service has no response'
    default_code = 'service_down_response'


class ServiceUnhandledErrorException(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Service has unhandled internal error.'
    default_code = 'service_unhandled_error'


class ServiceResponseParseException(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Service response cannot be parsed.'
    default_code = 'cannot_parse_service_response'
