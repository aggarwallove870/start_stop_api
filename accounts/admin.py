from django.contrib import admin
from .models import *

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):

    list_display = ('id','first_name', 'office_email', 'user',   'joining_date')


class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('id','department_name')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_superuser']


admin.site.register(User, UserAdmin)

# class CoverageAdmin(admin.ModelAdmin):
#     list_display = ['user', 'coverage_state', 'coverage_city']


# admin.site.register(VendorCoverage, CoverageAdmin)

class TimerAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'start', 'stop', 'user', 'timespent']


admin.site.register(Timer, TimerAdmin)