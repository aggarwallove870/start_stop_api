import string
import random
from django.db import models
from accounts.options import *
# from flexoffice.permissions import HRPERMISSIONS, employee_permission
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission


# Create your models here.


def unique_username():
    strings = string.ascii_uppercase + string.ascii_lowercase
    username = ''.join(random.choice(strings) for i in strings)[:6]
    while User.objects.filter(username=username).exists():
        username = ''.join(random.choice(strings) for i in strings)[:6]
    return username


class Department(models.Model):
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_name


class User(AbstractUser):
    user_type = models.CharField(max_length=1, choices=user_types, default=EMPLOYEE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    photo = models.ImageField(default='default/avatar.jpg')
    office_email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True, default='123456789')
    dob = models.DateField(verbose_name='Date of birth', blank=True, null=True, )
    joining_date = models.DateField(blank=True, null=True)
    permanent_address = models.TextField()
    correspondence_address = models.TextField(blank=True, null=True)
    resume = models.FileField(blank=True, null=True, upload_to='resume')
    documents = models.ImageField(blank=True, null=True, upload_to='documents')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    is_hr = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    # class Meta:
    #     permissions = employee_permission

    def get_user_type(self):

        return self.get_user_type_display()

    def save(self, *args, **kwargs):
        if self.user_type == HR:
            permissions = Permission.objects.filter(codename__in=HRPERMISSIONS)
            for perm in permissions:
                self.user_permissions.add(perm)
        if not self.username:
            self.username = unique_username()

        super(User, self).save(*args, **kwargs)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    office_email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=12)
    dob = models.DateField(verbose_name='Date of birth')
    joining_date = models.DateField(blank=True, null=True)
    permanent_address = models.TextField()
    correspondence_address = models.TextField(blank=True, null=True)
    resume = models.ImageField(blank=True, null=True, upload_to='resume')
    documents = models.ImageField(blank=True, null=True, upload_to='documents')
    image = models.ImageField(blank=True, null=True, upload_to='images')
    is_active = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sal = models.IntegerField(default=100)

    def __str__(self):
        return f"{str(self.first_name)}"

    # @receiver(post_save, sender=Employee)
    # # Create A instance Of Customer on user signup
    # def email_to_employee(sender, instance, created, **kwargs):
    #     if instance.office_email and instance.employee_uid:
    #         if not User.objects.filter(username=instance.office_email).exists():
    #             token = makesecret()
    #             secret = makeJWT(instance.office_email, token)
    #             Mailgun_send_email(instance.office_email, 'Create Your Password', TEXT(secret, request), HTML(secret, request,instance.office_email,instance.employee_uid))

# class CustomKey(models.Model):
#     key = models.CharField(max_length=100, unique=True)
#     value = models.CharField(max_length=100)
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    start = models.TimeField(auto_now=False)
    stop = models.TimeField(auto_now=False, null=True, blank=True)
    timespent =  models.CharField(max_length=100, null=True, blank=True)