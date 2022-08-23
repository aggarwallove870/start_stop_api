from django.contrib import messages
from django.http import request
from flexoffice_app.options import LEAVE_CHOICES, STATUS_CHOICES, LEAVE_PAID_STATUS, ABSENT, FULL_DAY, UNPAID_LEAVE
from django.db import models
from django.dispatch import receiver
from accounts.models import User, Employee
from datetime import datetime, date
from django.db.models.signals import post_save
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

today = datetime.now()


# Create your models here.

STATUS = (
    ('morning','MORNING'),
    ('evening', 'EVENING'),
)
class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, )
    employe_name = models.ForeignKey(Employee, on_delete=models.CASCADE, default='')
    attended_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='Created_by')
    leave_type = models.CharField(max_length=2, default=FULL_DAY, choices=LEAVE_CHOICES, blank=True, null=True)
    leave_status = models.CharField(max_length=2, default=UNPAID_LEAVE, choices=LEAVE_PAID_STATUS, blank=True,
                                    null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=ABSENT)
    note = models.TextField(blank=True, null=True)
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    attendance_date = models.DateField(default=datetime.now)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    month = models.IntegerField(default=today.month)

    def employe_name_data(self):
        return Employee.objects.get(first_name=self.employe_name.first_name)

    def leaves(self):
        taken_leaves = {'short_leave': Attendance.objects.filter(employee__id=self.employee.id, leave_type='s',
                                                                 created_at__month=datetime.now().month,
                                                                 created_at__year=datetime.now().year).count(),
                        'half_leave': Attendance.objects.filter(employee__id=self.employee.id, leave_type='h',
                                                                created_at__month=datetime.now().month,
                                                                created_at__year=datetime.now().year).count(),
                        'full_leave': Attendance.objects.filter(employee__id=self.employee.id, leave_type='f',
                                                                created_at__month=datetime.now().month,
                                                                created_at__year=datetime.now().year).count()}
        return taken_leaves

    def __str__(self):
        return f"{self.employe_name}"



class AttendanceSheet(models.Model):
    attendance_date = models.DateField(default=datetime.now, unique=True)
    is_holiday = models.BooleanField(default=False)
    sheet_opened = models.ManyToManyField(Attendance, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.attendance_date}"


@receiver(post_save, sender=AttendanceSheet)
def create_attendance(sender, instance, **kwargs):
    # emp_obj = User.objects.filter(Q(user_type='H') | Q(user_type='E') | Q(is_active=True)).exclude(user__isnull=True, user__exact=True)

    emp_obj = User.objects.filter(Q(user_type='H') | Q(user_type='E'), is_active=True).exclude(is_superuser=True, )

    if emp_obj:
        for employee in emp_obj:

            if Attendance.objects.filter(employee=employee, attendance_date=instance.attendance_date).exists():

                attend_obj = Attendance.objects.get(employee=employee, attendance_date=instance.attendance_date)

            else:

                attend_obj = Attendance.objects.create(employee=employee, attendance_date=instance.attendance_date)
                attend_obj.save()
            instance.sheet_opened.add(attend_obj.id)


class Salary(models.Model):
    employee_table = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_amount = models.DecimalField(decimal_places=2, max_digits=15)
    # old_salary = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=15)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_table}"


class SalaryBonus(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_link = models.ForeignKey(Employee, on_delete=models.CASCADE)
    bonus_amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(default=datetime.now)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee}"

    def total_salary(self):
        paid_salary = SalaryDetail.objects.filter(employeid=self.employee).values_list('paid_salary', flat=True)
        return sum(list(paid_salary))

    def year_salary(self):
        yearly_salary = SalaryDetail.objects.filter(employeid=self.employee, created_at__year=self.year)
        return sum(list(yearly_salary))


class SalaryDetail(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    employeid = models.ForeignKey(User, on_delete=models.CASCADE)
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total_leave_day = models.CharField(max_length=2)
    paid_leave_day = models.CharField(max_length=2)
    unpaid_leave_day = models.CharField(max_length=2)
    bonus_amount = models.IntegerField(default=0)
    paid_leave_amount = models.CharField(max_length=2)
    unpaid_leave_amount = models.CharField(max_length=2)
    paid_salary = models.CharField(max_length=20000)
    deducted_salary = models.CharField(max_length=100)
    half_leave = models.CharField(max_length=20,default=0)
    month = models.IntegerField(default=today.month-1)
    year = models.IntegerField(default=today.year)




class BidDetail(models.Model):
    project = (('F', 'Fixed'), ('H', 'Hourly'))
    contractURL = models.CharField(max_length=100)
    jobtitle = models.CharField(max_length=200)
    jobdescription = models.TextField()
    clientcountry = models.CharField(max_length=20)
    Proposal = models.TextField()
    connectsused = models.IntegerField()
    projecttype = models.CharField(choices=project, max_length=2)
    priceofproject = models.IntegerField()
    clientreplied = models.CharField(max_length=200)
    Comments = models.CharField(max_length=200)
    Converted = models.CharField(max_length=100)
    BidBy = models.CharField(max_length=100)


class Reports(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    tasks = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='morning')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
