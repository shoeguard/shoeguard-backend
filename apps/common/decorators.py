from functools import wraps

from apps.common.utils import check_partner_available
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


def check_partner_available_function_view(function: callable) -> callable:
    @wraps(function)
    def decorated(request: Request, *args, **kwargs):
        check_partner_available(request.user)
        return_value = function(request, *args, **kwargs)
        return return_value

    return decorated


def check_partner_available_class_view(function: callable) -> callable:
    @wraps(function)
    def decorated(
        self: GenericViewSet,
        request: Request,
        *args,
        **kwargs,
    ):
        check_partner_available(request.user)
        return_value = function(self, request, *args, **kwargs)
        return return_value

    return decorated
