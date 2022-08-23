from django.contrib import admin
from .models import *
# Register your models here.


class AttendanceSheetAdmin(admin.ModelAdmin):
    fields = ['attendance_date', 'sheet_opened', 'is_holiday']
    list_display = ('attendance_date',  'is_holiday' )

    # def get_sheet_opened(self, obj):
    #     return "\n".join([s.sheet_opened for s in obj.sheet_opened.first()])


class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('id','employee','employe_name', 'leave_type', 'attendance_date', 'status', 'leave_status', 'created_at',)
    list_filter = ['employee', 'leave_type', 'status', 'created_at', 'updated_at']
    search_fields = ['employee', 'leave_type', 'status', 'created_at', 'updated_at']


class SalaryAdmin(admin.ModelAdmin):
    # fields = ['employeid', 'salary_amount',]
    list_display = ('employee_table', 'salary_amount', 'created_at')
    list_filter = [ 'salary_amount', 'created_at']
    search_fields = ['employee', 'salary_amount', 'created_at']


class SalaryDetailAdmin(admin.ModelAdmin):
    fields = ['salary','employeid', 'employe', 'total_leave_day', 'paid_salary', 'paid_leave_day', 'unpaid_leave_day', 'bonus_amount',
              'paid_leave_amount', 'unpaid_leave_amount','month','year']
    list_display = ('salary', 'employeid', 'employe', 'total_leave_day', 'paid_leave_day', 'unpaid_leave_day', 'bonus_amount',
              'paid_leave_amount', 'unpaid_leave_amount', 'paid_salary')
    list_filter = ['salary', 'total_leave_day', 'paid_leave_day', 'unpaid_leave_day', 'bonus_amount',
              'paid_leave_amount', 'unpaid_leave_amount']
    search_fields = ['salary', 'total_leave_day', 'paid_leave_day', 'unpaid_leave_day', 'bonus_amount',
              'paid_leave_amount', 'unpaid_leave_amount']

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id',  'date', 'tasks' )

admin.site.register(AttendanceSheet, AttendanceSheetAdmin)
admin.site.register(SalaryDetail, SalaryDetailAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(SalaryBonus)
admin.site.register(Reports,ReportAdmin)

