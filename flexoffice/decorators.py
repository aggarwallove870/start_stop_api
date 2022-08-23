from django.shortcuts import redirect
from accounts.options import *


# def unauthenticatedonly(function):
#     def wrap(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('homepage')
#         else:
#             return function(request, *args, **kwargs)
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
#
#
# def customeronly(function):
#     def wrap(request, *args, **kwargs):
#         user = request.user
#         if user.is_authenticated and user.user_type == CUSTOMER:
#             return function(request, *args, **kwargs)
#         else:
#             return redirect('not_allowed', role=CUSTOMER)
#
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
#
#
# def vendorronly(function):
#     def wrap(request, *args, **kwargs):
#         user = request.user
#         if user.is_authenticated and user.user_type == VENDOR:
#             return function(request, *args, **kwargs)
#         else:
#             return redirect('not_allowed', role=VENDOR)
#
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap


def adminonly(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.user_type == STAFF or user.is_superuser or user.user_type == SELLER or user.user_type == BLOGGER:
                return function(request, *args, **kwargs)
            else:
                return redirect('not_allowed', role=user.user_type)
        else:
            return redirect('not_allowed', role=ADMIN)
    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
