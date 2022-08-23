from django.db.models import Count
from accounts.models import Timer, User
from rest_framework import serializers
from accounts.serializers import UserSerializer
from flexoffice_app.models import AttendanceSheet, Attendance, Salary, SalaryBonus


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    attended_by = serializers.SerializerMethodField()

    def get_employee(self, obj):
        employee = User.objects.get(id=obj.employee.id)
        return UserSerializer(employee).data

    def get_attended_by(self, obj):
        if obj.attended_by:
            attended_by = User.objects.get(id=obj.attended_by.id)
            return UserSerializer(attended_by).data
        return

    class Meta:
        model = Attendance
        fields = "__all__"


class AttendanceSheetSerializer(serializers.ModelSerializer):
    sheet_opened = serializers.SerializerMethodField()

    def get_sheet_opened(self, obj):
        # attendance = Attendance.objects.filter(created_at=obj.attendance_date, check_in__isnull=False).order_by('id',)
        attendance = Attendance.objects.filter(attendance_date=obj.attendance_date, check_in__isnull=False).order_by('id',)
        return AttendanceSerializer(attendance, many=True).data

    class Meta:
        model = AttendanceSheet
        fields = "__all__"


def get_attendance_status_filter(month, year, status, employee):
    total_data = Attendance.objects.filter(attendance_date__month=month, employee=employee,
                                           attendance_date__year=year, status=status)
    return total_data.aggregate(status=Count('status'))


def get_attendance_leave_filter(month, year, leave_type, employee):
    total_data = Attendance.objects.filter(attendance_date__month=month, employee=employee,
                                           attendance_date__year=year, status='L', leave_type=leave_type)
    return total_data.aggregate(leave_type=Count('leave_type'))


def get_attendance_leave_status_filter(month, year, leave_status, employee):
    total_data = Attendance.objects.filter(attendance_date__month=month, employee=employee,
                                           attendance_date__year=year, status='L', leave_status=leave_status)
    return total_data.aggregate(leave_status=Count('leave_status'))


def get_unpaid_leave_filter(month, year, leave_status, employee):
    total_data = Attendance.objects.filter(attendance_date__month=month, employee=employee,
                                           attendance_date__year=year, status='L', leave_status=leave_status)
    return total_data.aggregate(leave_status=Count('leave_status'))


def get_unpaid_calculation(month, year, leave_status, employee, leave_type):
    total_data = Attendance.objects.filter(attendance_date__month=month, employee=employee, leave_type=leave_type,
                                           attendance_date__year=year, status='L', leave_status=leave_status)
    return total_data.aggregate(leave_status=Count('leave_status'))


def get_calculated_salary(full_day, half_day, total_absent, employee,  month, year):
    paid_salary = 0
    total_salary = 0
    bonus = 0
    if Salary.objects.filter(employee=employee).exists():
        obj = Salary.objects.get(employee=employee)
        total_salary = obj.salary_amount
        one_day_salary = int(total_salary / 22)
        half_day_salary = int(one_day_salary/2)
        absent_deduce = one_day_salary*total_absent['status']
        half_deduce = half_day_salary*half_day['leave_status']
        full_deduce = one_day_salary*full_day['leave_status']
        paid_salary = total_salary - full_deduce - half_deduce - absent_deduce

        if SalaryBonus.objects.filter(employee=employee, date__month=month, date__year=year).exists():
            bonus = SalaryBonus.objects.filter(employee=employee, date__month=month,
                                               date__year=year).last().bonus_amount
            paid_salary += bonus

    return "₹{:,.2f}".format(paid_salary), "₹{:,.2f}".format(total_salary), "₹{:,.2f}".format(bonus)


class AttendanceDetailSerializer(serializers.ModelSerializer):
    attendance_data = serializers.SerializerMethodField()
    # salary = serializers.SerializerMethodField()

    def get_attendance_data(self, obj):
        month = self.context.get('month')
        year = self.context.get('year')
        total_leaves = get_attendance_status_filter(month, year, 'L', obj)
        total_absent = get_attendance_status_filter(month, year, 'A', obj)
        total_presents = get_attendance_status_filter(month, year, 'L', obj)
        total_full_day = get_attendance_leave_filter(month, year, 'f', obj)
        total_half_day = get_attendance_leave_filter(month, year, 'h', obj)
        total_short_day = get_attendance_leave_filter(month, year, 's', obj)
        unpaid_leave = get_attendance_leave_status_filter(month, year, 'u', obj)
        paid_leave = get_attendance_leave_status_filter(month, year, 'p', obj)
        full_day_unpaid_leave = get_unpaid_calculation(month, year, 'u', obj, 'f')
        half_day_unpaid_leave = get_unpaid_calculation(month, year, 'u', obj, 'h')
        paid_salary, total_salary, bonus = get_calculated_salary(full_day_unpaid_leave, half_day_unpaid_leave, total_absent, obj, month, year)

        context = {"leaves": total_leaves, "absent": total_absent, 'present': total_presents,
                   "full_day": total_full_day, "half_day": total_half_day, 'short_day': total_short_day, 'bonus':bonus,
                   "unpaid_leave": unpaid_leave, "paid_leave": paid_leave, 'total_salary': total_salary, 'paid_salary': paid_salary}
        return context


    class Meta:
        model = User
        fields = ["id", "username", 'full_name', 'email', 'attendance_data']


class SalarySerializer(serializers.ModelSerializer):

    employee_detail = serializers.SerializerMethodField()
    
    def get_employee_detail(self, obj):
        employee = User.objects.get(id=obj.employee.id)
        return UserSerializer(employee).data

    class Meta:
        model = Salary
        fields = "__all__"


class SalaryBonusSerializer(serializers.ModelSerializer):

    employee_detail = serializers.SerializerMethodField()

    def get_employee_detail(self, obj):
        employee = User.objects.get(id=obj.employee.id)
        return UserSerializer(employee).data

    class Meta:
        model = SalaryBonus
        fields = "__all__"




