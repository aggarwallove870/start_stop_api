from django.contrib.auth.models import Permission
from accounts.models import User
from django.db.models import Q
from django.urls import resolve
# from accounts.options import *
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated

VIEW = 'view'
EDIT = 'edit'
DELETE = 'delete'


class HRAndAdminPermA(IsAuthenticated):
    # message = 'User access not allowed.'
    def has_permission(self, request, view):

        resp = super(HRAndAdminPermA, self).has_permission(request, view)
        return (getattr(request.user, "user_type", None) == "H" or getattr(request.user, "user_type", None) == "A" or request.user.is_superuser) and resp


class CreateUserPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'POST' or request.method == 'PUT':
            if request.data.get('user_type') == 'A':
                if request.user.user_type == 'A':
                    return True
                return False

        elif request.method == 'DELETE':
            if User.objects.filter(id=request.query_params.get('id')).exists():
                user_type = User.objects.get(id=request.query_params.get('id'))

                if request.user.user_type is user_type.user_type:
                    return False
                elif request.user.user_type == 'H' and user_type.user_type == 'A':
                    return False
                elif request.user.user_type == 'E' and user_type.user_type == 'H':
                    return False
        return True

    # def has_object_permission(self, request, view, obj):
    #     print(request.data, 'here')
    #     return True


def make_permission(page, ptype):
    return f'{ptype}___{page}'


employee_permission = (

    (make_permission('dashboard', VIEW), "Can view employee"),

    # Customer
    (make_permission('customer', VIEW), "Can view employee"),
    (make_permission('customer', EDIT), "Can add or edit employee"),
    (make_permission('customer', DELETE), "Can delete employee"),

)
#
permission_codes = [i[0] for i in employee_permission]


def employee_permissions():
    return Permission.objects.filter(codename__in=permission_codes).order_by('id')

#
# URLS = {
#
#     "admindashboard": {"name": 'dashboard', 'code': VIEW},
#
#     "adminvendors": {"name": 'vendor', 'code': VIEW},
#     "editvendor": {"name": 'vendor', 'code': EDIT},
#     "vendornew": {"name": 'vendor', 'code': EDIT},
#
#
#
#     "blog_list": {"name": 'blog_post', 'code': VIEW},
#     "create_blog": {"name": 'blog_post', 'code': EDIT},
#     "update_blog": {"name": 'blog_post', 'code': EDIT},
#
# }
#
#
# def permissionrequired(urlname, url):
#     if urlname == 'dynamiclist':
#         url = url.replace('/admin/', '')
#         return make_permission(url.replace('/', ''), VIEW)
#
#     elif urlname == 'dynamicdashboard_' or urlname == 'dynamicdashboard':
#         url = url.replace('/admin/', '')
#         return make_permission(url[:url.find('/')], EDIT)
#
#     elif urlname == 'dd':
#         url = url.replace('/admin/', '')
#         url = url[:url.find('/')]
#         return make_permission(url, DELETE)
#
#     elif urlname == 'delete':
#         url = url[url.find('=') + 1:]
#         return make_permission(url, DELETE)
#
#     elif urlname == 'reducedesellerlv':
#         url = url.replace('/admin/esellser/', '')
#         url = url[:url.find('/')]
#         name = URLS[f'{url}_lv']['name']
#         code = URLS[f'{url}_lv']['code']
#         return make_permission(name, code)
#
#     elif urlname == 'reducedeselleruv':
#         url = url.replace('/admin/esellser/', '')
#         url = url[:url.find('/')]
#         name = URLS[f'{url}_uv']['name']
#         code = URLS[f'{url}_uv']['code']
#         return make_permission(name, code)
#
#     elif urlname == 'reducedesellercv':
#         url = url.replace('/admin/esellser/', '')
#         url = url[:url.find('/')]
#         name = URLS[f'{url}_uv']['name']
#         code = URLS[f'{url}_uv']['code']
#         return make_permission(name, code)
#
#     elif urlname == 'reducedesellerdv':
#         url = url.replace('/admin/esellser/', '')
#         url = url[:url.find('/')]
#         name = URLS[f'{url}_dv']['name']
#         code = URLS[f'{url}_dv']['code']
#         return make_permission(name, code)
#
#     else:
#         url = URLS.get(urlname)
#
#         if url:
#             return make_permission(url['name'], url['code'])
#         return None
#
#
# def userpermissions(request):
#     groups = list(request.user.groups.all().values_list('id', flat=True))
#     userperms = list(request.user.user_permissions.all().values_list('id', flat=True))
#     return Permission.objects.filter(Q(group__in=groups) | Q(id__in=userperms)).values_list('codename', flat=True)
#
#
# def is_admin_url(url):
#     return url.startswith('/admin')
#
#
# def processpermission(request):
#     current_url = resolve(request.path_info).url_name
#     if is_admin_url(request.path_info):
#         if request.user.is_authenticated:
#             if request.user.is_superuser:
#                 return False
#             else:
#                 required_perm = permissionrequired(current_url, request.get_full_path())
#                 if required_perm:
#                     userperms = userpermissions(request)
#                     if required_perm not in userperms:
#                         return True
#
#
# def processpermissionfromurl(request, url):
#     current_url = resolve(url).url_name
#     if is_admin_url(url):
#         if request.user.is_authenticated:
#             if request.user.is_superuser:
#                 return False
#             else:
#                 required_perm = permissionrequired(current_url, url)
#                 if required_perm:
#                     userperms = userpermissions(request)
#                     if required_perm not in userperms:
#                         return True


HRPERMISSIONS = [
                        make_permission('user', VIEW),
                        make_permission('attendance', EDIT),
                        make_permission('attendancesheet', VIEW),
                        make_permission('salary', EDIT),
                        make_permission('salarydetail', DELETE),
                    ]

