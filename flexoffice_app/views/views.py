from curses.ascii import HT
import re
from tkinter import N
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes,APIView
from django.contrib.auth import login as Login, logout as Logout
from accounts.mailer import *
import string
from django.contrib.sites.shortcuts import get_current_site
import random
from django.core.mail import EmailMessage
from flexoffice import settings
from accounts.forms import EmployeeForm
from flexoffice_app.models import *
from datetime import datetime
from accounts.models import *
from accounts.mailer import Mailgun_send_email, SalaryHTML, UrlText
import calendar
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password


# Create your views here.
def random_pwd():
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return str(res)


def salarycalucation(month, year, many=True, empid=False):
    if many == True:

        employee_obj = Employee.objects.all()

        for employee in employee_obj:
            try:
                if employee.user and employee.sal:
                    print("LOOK")
                    cal(employee, month, year)
            except:
                pass
        return employee_obj
    else:
        employee = Employee.objects.filter(id=empid)

        try:
            if employee.user and employee.sal:
                cal(employee, month, year)
        except:
            pass
        return employee


def cal(employee, month, year):
    print("Arrived")
    per_day_salary = employee.sal / 22
    print("dgfhgd", per_day_salary)

    att = employee.attendance_set.filter(created_at__month=month,
                                         created_at__year=year, employe=employee)
    print("att", att)

    try:
        mailsal = SalaryDetail.objects.get(created_at__month=datetime.now().month,
                                           created_at__year=datetime.now().year,
                                           employeid=employee)
        print("mailsal", mailsal)
    except SalaryDetail.DoesNotExist:
        mailsal = None

    if mailsal:
        employee.mailsent = True
    else:
        employee.mailsent = False
    mailsal = None
    paid_payment = 0
    unpaid_payment = 0
    absent = 0
    leave_dates = []

    for attendances in att:

        if attendances.status == 'L':

            leave_dates.append(attendances.created_at)
            if attendances.leave_type == 'h' and attendances.leave_stutus == 'p':
                paid_payment += per_day_salary / 2
            elif attendances.leave_type == 'h' and attendances.leave_stutus == 'u':
                unpaid_payment += per_day_salary / 2
            elif attendances.leave_type == 'f' and attendances.leave_stutus == 'p':
                paid_payment += per_day_salary
            elif attendances.leave_type == 'f' and attendances.leave_stutus == 'u':
                unpaid_payment += per_day_salary
            elif attendances.leave_type == 's' and attendances.leave_stutus == 'p':
                paid_payment += per_day_salary / 4
            elif attendances.leave_type == 's' and attendances.leave_stutus == 'u':
                unpaid_payment += per_day_salary / 4

        elif attendances.status == 'A':

            absent = absent + 1
            leave_dates.append(attendances.created_at)
            unpaid_payment += per_day_salary

    employee.paid_payment = paid_payment
    employee.unpaid_payment = unpaid_payment
    employee.paid_salary = employee.salary.salary_amount - unpaid_payment

    total_leaves = list(att.values_list('leave_stutus', flat=True, ))
    leave_status = list(att.values_list('leave_stutus', flat=True))
    leave_type = list(att.values_list('leave_type', flat=True))

    half_leave = [hleave if hleave == 'h' else None for hleave in leave_type]
    full_leave = [fleave if fleave == 'f' else None for fleave in leave_type]
    short_leave = [sleave if sleave == 's' else None for sleave in leave_type]
    paid_leave = [pleave if pleave == 'p' else None for pleave in leave_status]
    unpaid_leave = [uleave if uleave == 'u' else None for uleave in leave_status]

    # half_leave.remove(None) if None in half_leave else half_leave

    employee.total_leaves = len(total_leaves) - total_leaves.count(None)
    # if employee.total_leaves == 0 and absent == 0:
    #     employee.paid_salary = employee.salary.salary_amount + per_day_salary

    employee.paid_salary += per_day_salary

    employee.half_leave = len(half_leave) - half_leave.count(None)
    employee.full_leave = len(full_leave) - full_leave.count(None)
    employee.short_leave = len(short_leave) - short_leave.count(None)
    employee.paid_leave = len(paid_leave) - paid_leave.count(None)
    employee.unpaid_leave = len(unpaid_leave) - unpaid_leave.count(None)
    employee.per_day_salary = per_day_salary
    if absent != 0:
        employee.absent = absent
    else:
        employee.absent = 0


@login_required(login_url='login')
def dashboard(request):
    '''
    Call after login user and user want to go deshboard from anywhere but user login required for go to deshboard.

    Models and views are using in this View :

    **View and renders page.**
        * get all employee data from Employee table and render to deshboard page.
        * get attendancesheet data with filter today date and render to deshboard page.

        * Renders HTML Template (flex/dashboard.html)

    **Models :**
        * Project : :model:`flexoffice_app.models.Employee`
        * PeerApproval : :model:`flexoffice_app.models.AttendanceSheet`

    **Template:**

    :template:`flex/dashboard.html`

       '''
    if request.user.is_hr:
        data = Attendance.objects.filter(attendance_date=datetime.now()).all()
        print(data)
    else:
        data = Attendance.objects.filter(attendance_date=datetime.now(), employe_name__first_name=request.user)
        # data = AttendanceSheet.objects.filter(created_at=datetime.now())
        print(data)
        print("j", request.user)

    return render(request, 'flex/dashboard.html', {'employees': data})


@login_required(login_url='login')
def employeelist(request):
    emp_obj = Employee.objects.all()
    for k in emp_obj:
        print(k.image)
    return render(request, 'flex/employeelist.html', {'employees': emp_obj})


@login_required(login_url='login')
def attendancelist(request):
    employeeID = request.GET.get('check_leave_id')

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')

        if month and year:
            date = datetime.now()
            employee_obj = salarycalucation(date.month, date.year)
            data = {"empolyees": employee_obj}
            obj = Employee.objects.all()
            unpaid_leave_dic = {}
            half_leave_dic = {}
            full_leave_dic = {}
            paid_leave_dic = {}
            deduct_leave = {}
            total_salary_dict = {}
            total_halfleave_dict = {}
            total_present_dict = {}

            for k in obj:
                if Attendance.objects.filter(month=month).exists():
                    unpaid_leave = Attendance.objects.filter(status="L", employe_name=k.id, leave_status=UNPAID_LEAVE,
                                                             month=date.month).count()
                    unpaid_leave_dic[k.id] = unpaid_leave
                    half_leave = Attendance.objects.filter(employe_name=k.id, status="P", leave_status=UNPAID_LEAVE,
                                                           month=date.month).count()
                    half_leave_dic[k.id] = half_leave
                    full_leave = Attendance.objects.filter((Q(status="A") | Q(status="L")), employe_name=k.id,
                                                           month=date.month).count()
                    full_leave_dic[k.id] = full_leave
                    paid_leave = Attendance.objects.filter((Q(status="A") | Q(status="L")), employe_name=k.id,
                                                           leave_status="p",
                                                           month=date.month).count()
                    paid_leave_dic[k.id] = paid_leave

                    unpaid_leave_salary = Attendance.objects.filter((Q(status="A") | Q(status="L")), employe_name=k.id,
                                                                    leave_status=UNPAID_LEAVE,
                                                                    month=date.month).count()

                    ## Short Leave
                    total_half_leave = Attendance.objects.filter(employe_name=k.id, leave_status=UNPAID_LEAVE,
                                                                 leave_type="h",
                                                                 month=date.month).count()
                    total_halfleave_dict[k.id] = total_half_leave

                    ####
                    number_of_days = calendar.monthrange(date.year, date.month)[1]
                    print(number_of_days)
                    deduct_leave[k.id] = (k.sal / number_of_days * unpaid_leave_salary) + (
                            total_half_leave * k.sal / number_of_days / 2)

                    total_salary_dict[k.id] = k.sal - k.sal / number_of_days * unpaid_leave_salary

                    ## Total Present
                    total_present = Attendance.objects.filter(employe_name=k.id, status="P",
                                                              month=date.month).count()
                    total_present_dict[k.id] = total_present

        html = render_to_string('flex/partial_month_data.html',
                                {'empolyees': employee_obj, 'unpaid_leave_dic': unpaid_leave_dic,
                                 'half_leave_dic': half_leave_dic,
                                 'full_leave_dic': full_leave_dic, 'paid_leave_dic': paid_leave_dic,
                                 'deduct_leave': deduct_leave,
                                 'total_salary_dict': total_salary_dict, 'total_present_dict': total_present_dict,
                                 'total_halfleave_dict': total_halfleave_dict}, request)
        return JsonResponse({'html': html})


    elif employeeID and request.method == 'GET':
        month = request.GET.get('month')
        year = request.GET.get('year')
        if month and year:
            leave_check = Attendance.objects.filter(created_at__month=month,
                                                    created_at__year=year, employe_id=employeeID)
            leave_type = list(leave_check.values_list('leave_type', flat=True))
            half_leave = [hleave if hleave == 'h' else None for hleave in leave_type]
            full_leave = [fleave if fleave == 'f' else None for fleave in leave_type]
            short_leave = [sleave if sleave == 's' else None for sleave in leave_type]
            data = {}
            data['full_leave'] = len(full_leave) - full_leave.count(None)
            data['half_leave'] = len(half_leave) - half_leave.count(None)
            data['short_leave'] = len(short_leave) - short_leave.count(None)
            return JsonResponse(data)

    # data = AttendanceSheet.objects.filter(created_at__month=datetime.now().date().month,
    #                                  created_at__year=datetime.now().date().year).all()
    data1 = Attendance.objects.all()
    print(data1)

    return render(request, 'flex/attendancelist.html', {'attendances': data1})


@login_required(login_url='login')
def attendance(request):
    date = datetime.now()
    check_leave_id = request.GET.get('check_leave_id')

    if check_leave_id and request.method == 'GET':
        leaves = Attendance.objects.filter(pk=check_leave_id)[0].leaves()
        return JsonResponse(leaves)

    check_holidayid = request.POST.get('hilidayID')
    checked = request.POST.get('holidaycheck')
    if check_holidayid and checked:
        if checked == 'true':
            holiday = AttendanceSheet.objects.filter(pk=check_holidayid, )
            holiday.update(is_holiday=True)

        else:
            AttendanceSheet.objects.update(is_holiday=False)

    if request.method == 'POST' and not check_holidayid:
        id = request.POST.get('id')
        present = request.POST.get('present')
        leave = request.POST.get('leave')
        leavestatus = request.POST.get('leave_status')
        try:
            attten = Employee.objects.get(pk=id)
        except:
            pass
        obj = Attendance.objects.filter(id=id).last()

        #### change1 ###
        attendence_id = Attendance.objects.filter(id=id)

        if leavestatus == 'true':
            leave_type = request.POST.get('leavetype')
            obj = Attendance.objects.get(employe_name=attten, attendance_date=datetime.now())
            obj.leave_status = leave_type
            obj.save()

        if leave == 'true':
            status = 'L'
            try:
                atten = Attendance.objects.get(employe_name=request.POST.get('id'), attendance_date=datetime.now())
                atten.status = status
                atten.leave_type = 'f'
                atten.save()
            except:
                atten = Attendance.objects.create(employee_id=request.user.id, employe_name=attten,
                                                  attended_by_id=request.user.id, status=status, leave_type='f',
                                                  leave_status='u')


        elif leave == 'false':
            status = 'L'
            leave_type = request.POST.get('leavetype')
            if leave_type:
                id = request.POST.get('id')
                obj = Attendance.objects.get(employe_name=attten, attendance_date=datetime.now())
                obj.leave_type = leave_type
                obj.save()

            else:
                try:
                    atten = Attendance.objects.get(employe_name=attten)
                except:

                    atten = Attendance.objects.create(employee_id=request.user.id, employe_name=attten,
                                                      attended_by_id=request.user.id, status=status, leave_type='f',
                                                      leave_status='u')

        if not leave and not leavestatus:

            if present == 'true':
                try:
                    atten = Attendance.objects.get(employe_name=request.POST.get('id'), attendance_date=datetime.now())
                    atten.status = "P"
                    atten.leave_type = None
                    atten.leave_status = None
                    atten.save()
                except:
                    atten = Attendance.objects.create(employee_id=request.user.id, employe_name=attten,
                                                      attended_by_id=request.user.id, status="P", leave_type=None,
                                                      leave_status=None)

            if present != 'true':
                status = 'A'
                try:
                    atten = Attendance.objects.get(employe_name=request.POST.get('id'), attendance_date=datetime.now())
                    atten.status = status
                    atten.leave_type = None
                    atten.leave_status = None
                    atten.save()
                except:
                    atten = Attendance.objects.create(employee_id=request.user.id, employe_name=attten,
                                                      attended_by_id=request.user.id, status=status, leave_type=None,
                                                      leave_status=None)

        # leaves = attten[0].leaves()
        #
        # attten.shorted = leaves['short_leave']
        # attten.halfed = leaves['half_leave']
        # attten.fulled = leaves['full_leave']

        # if attten:
        aten = Attendance.objects.filter(id=atten.id)

        html = render_to_string('flex/partial_attendance_status.html', {'employe': aten})
        return JsonResponse({'html': html})

    else:

        if AttendanceSheet.objects.filter(created_at=datetime.now()).exists():
            AttendanceSheet.objects.update(sheet_opened=1)


        else:
            emp_obj = Employee.objects.filter(is_active=False).all()
            if emp_obj:
                # return HttpResponse("honkdem")
                # AttendanceSheet.objects.create(sheet_opened=1)
                Attendance.objects.all()
                # for employee in emp_obj:
                #
                #     if employee.user:
                #         print('here')
                #         # Attendance.objects.create(employe=employee,attendance_sheet=sheet_attend)

        # data = AttendanceSheet.objects.get(created_at=datetime.now())
        attendence_status = {}
        if Attendance.objects.filter(created_at=datetime.now()).exists():
            datas = Attendance.objects.filter(created_at=datetime.now()).all()
            for data in datas:
                attendence_status[data.employe_name_id] = data.status

        emp_data = Employee.objects.all()
        print(emp_data)

        return render(request, 'flex/attendance.html', {'employe': emp_data, 'attendence_status': attendence_status})


@login_required(login_url='login')
def calculatesalary(request):
    employee_obj = salarycalucation(datetime.now().date().month, datetime.now().date().year)
    data = {"empolyees": employee_obj}
    return render(request, 'flex/calculatesalary.html', data)


@login_required(login_url='login')
def addnote(request):
    if request.method == 'POST':
        id = request.POST.get('noteid')
        note = request.POST.get('note-text')
        Attendance.objects.filter(id=id).update(note=note)
        return JsonResponse({"status": True})

    id = request.GET.get('id')
    atten = Attendance.objects.get(id=id)
    data = {"note": atten.note}

    return JsonResponse(data)


@login_required(login_url='login')
def mailsalary(request):
    if request.method == 'POST':
        print("Check", request.POST.values)

        id = request.POST.get('id')

        employee = Employee.objects.get(id=id)
        print(employee)
        obj = User.objects.get(id=request.user.id)
        print(obj)

        Salary_obj = Salary(employee_table_id=employee.id, salary_amount=employee.sal)
        Salary_obj.save()

        sal_bonus = SalaryBonus(employee=obj, employee_link=employee)
        sal_bonus.save()

        if request.POST.get('bonus') and request.POST.get('bonus') != ' ':
            bonus = request.POST.get('bonus', 0)
        else:
            bonus = 0
        paid = request.POST.get('paid_salary', 0.00) + request.POST.get('bonus', 0.00)

        obj = SalaryDetail.objects.create(salary=Salary_obj, employeid=obj, employe=employee,
                                          total_leave_day=request.POST.get('total_leaves'),
                                          paid_leave_day=request.POST.get('paid_leave'),
                                          unpaid_leave_day=request.POST.get('unpaid_leave'),
                                          bonus_amount=bonus,
                                          paid_leave_amount=request.POST.get('paid_payment'),
                                          unpaid_leave_amount=request.POST.get('unpaid_payment'),
                                          paid_salary=paid,
                                          deducted_salary=request.POST.get('deducted_salary'),
                                          half_leave=request.POST.get('half_leave')

                                          )

        obj.save()
        Mailgun_send_email(employee.office_email, 'Salary Details', UrlText(request),
                           SalaryHTML(request, employee.office_email, obj))

        return JsonResponse({'data': id})

    else:
        date = datetime.now()
        employee_obj = salarycalucation(date.month - 1, date.year - 1)

        print(f"{date.year}-{date.month - 1}")

        data = {"empolyees": employee_obj}
        print("Check", employee_obj)

        obj = Employee.objects.all()
        unpaid_leave_dic = {}
        half_leave_dic = {}
        full_leave_dic = {}
        paid_leave_dic = {}
        deduct_leave = {}
        total_salary_dict = {}
        total_present_dict = {}
        total_halfleave_dict = {}
        for k in obj:
            unpaid_leave = Attendance.objects.filter(status="L", employe_name=k.id, leave_status=UNPAID_LEAVE,
                                                     month=date.month - 1).count()
            unpaid_leave_dic[k.id] = unpaid_leave
            half_leave = Attendance.objects.filter(employe_name=k.id, status="P", leave_status=UNPAID_LEAVE,
                                                   month=date.month - 1).count()
            half_leave_dic[k.id] = half_leave
            full_leave = Attendance.objects.filter((Q(status="A") | Q(status="L")), employe_name=k.id,
                                                   month=date.month - 1).count()
            full_leave_dic[k.id] = full_leave
            paid_leave = Attendance.objects.filter((Q(status="A") | Q(status="L")), employe_name=k.id, leave_status="p",
                                                   month=date.month - 1).count()
            paid_leave_dic[k.id] = paid_leave

            unpaid_leave_salary = Attendance.objects.filter((Q(status="A") | Q(status="L")), employe_name=k.id,
                                                            leave_status=UNPAID_LEAVE,
                                                            month=date.month - 1).count()

            ## Short Leave
            total_half_leave = Attendance.objects.filter(employe_name=k.id, leave_status=UNPAID_LEAVE, leave_type="h",
                                                         month=date.month - 1).count()
            total_halfleave_dict[k.id] = total_half_leave

            ####
            number_of_days = calendar.monthrange(date.year, date.month - 1)[1]
            print(number_of_days)
            deduct_leave[k.id] = (k.sal / number_of_days * unpaid_leave_salary) + (
                    total_half_leave * k.sal / number_of_days / 2)

            total_salary_dict[k.id] = k.sal - k.sal / number_of_days * unpaid_leave_salary

            ## Total Present
            total_present = Attendance.objects.filter(employe_name=k.id, status="P",
                                                      month=date.month - 1).count()
            total_present_dict[k.id] = total_present

    return render(request, 'flex/mailsalary.html',   
                  {'empolyees': employee_obj, 'unpaid_leave_dic': unpaid_leave_dic, 'half_leave_dic': half_leave_dic,
                   'full_leave_dic': full_leave_dic, 'paid_leave_dic': paid_leave_dic, 'deduct_leave': deduct_leave,
                   'total_salary_dict': total_salary_dict, 'total_present_dict': total_present_dict,
                   'total_halfleave_dict': total_halfleave_dict})


@login_required(login_url='login')
def salaryhistory(request):
    if request.method == 'POST':

        year = request.POST.get('year')
        month = request.POST.get('month')
        if not month:
            employees = SalaryDetail.objects.filter(year=year).all()

        else:
            employees = SalaryDetail.objects.filter(month=month).all()

        if month and year:
            employees = SalaryDetail.objects.filter(month=month, year=year).all()

        html = render_to_string('flex/partial_salary_history.html', {'employees': employees}, request)

        return JsonResponse({'html': html})

    else:

        employees = SalaryDetail.objects.all()
        data = {'employees': employees}

        return render(request, 'flex/salaryhistory.html', data)


def morning_report(request):
    date_dict = {}
    print(request.GET.get('name'))
    if request.method == 'POST':
        if not request.POST.get('hidden_employee') and Reports.objects.filter(user=request.user, date=datetime.now(),
                                                                              status=request.POST.get(
                                                                                      'status')).exists():
            messages.error(request, 'You can not add this status again')
            report = Reports.objects.filter(user=request.user)
            return render(request, 'flex/morning_report.html', {'reports': report})

        elif request.POST.get('hidden_employee'):
            obj = Reports.objects.get(id=request.POST.get('hidden_employee'))
            obj.tasks = request.POST.get('tasks')
            obj.status = request.POST.get('status')
            obj.save()
            messages.success(request, 'Successfully updated.')
            return redirect('morning_report')

        else:
            tasks = request.POST.get('tasks')
            status = request.POST.get('status')
            report = Reports.objects.create(user=request.user, tasks=tasks, status=status)
            messages.success(request, 'Successfully added.')
            return redirect('morning_report')
    else:
        if request.GET.get('id'):
            resp = list(Reports.objects.filter(id=request.GET.get('id')).values('tasks', 'status'))
            return JsonResponse({'data': resp}, safe=False)

        report = Reports.objects.filter(user=request.user)
        return render(request, 'flex/morning_report.html', {'reports': report})


def reports_all(request):
    # reports = Reports.objects.all()
    employee = Employee.objects.all()

    if request.method == "GET" and request.GET.get('ID'):
        reports = Reports.objects.filter(user=request.GET.get('ID'))
        print(reports)
        html = render_to_string('flex/report_all_filter.html', {'reports': reports}, request)
        return JsonResponse({'html': html})

    if request.method == "POST" and request.POST.get('modal'):
        obj = list(Reports.objects.filter(id=request.POST.get('ID')).values('tasks', 'status'))
        return JsonResponse({'data': obj}, safe=False)

    if request.method == "GET":
        reports = Reports.objects.all()
        # paginator = Paginator(reports, 3)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

    return render(request, "flex/report_all.html", {'reports': reports, 'employee': employee})


def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            password = random_pwd()
            user = User(username=request.POST.get('office_email'), password=make_password(password),
                        email=request.POST.get('office_email'))
            user.save()

            first_name = form.cleaned_data['first_name']
            office_email = form.cleaned_data['office_email']
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            image = form.cleaned_data['image']
            sal = form.cleaned_data['sal']
            permanent_address = form.cleaned_data['permanent_address']
            correspondence_address = form.cleaned_data['correspondence_address']
            department = form.cleaned_data['department']
            employe = Employee.objects.create(first_name=first_name, office_email=office_email, phone=phone, dob=dob,
                                              image=image, sal=sal, permanent_address=permanent_address,
                                              correspondence_address=correspondence_address, department=department)
            employe.user_id = user.id
            employe.save()

            mail_subject = 'Employee login detail'

            message = render_to_string('accounts/employee_email.html', {
                'username': request.POST.get('office_email'),
                'password': password,
                'name':form.cleaned_data['first_name']
            })
            recipient_list = request.POST.get('office_email')
            email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [recipient_list])
            email.send()
            # redirect to a new URL
            return redirect('employeelist')
    else:
        form = EmployeeForm()

    return render(request, 'flex/add_employee.html', {'form': form})


def image(request):
    image_data = open("/Users/mac/Downloads/flexoffice-branchmain/flexoffice_app/views/time.jpg", "rb").read()
    return HttpResponse(image_data, content_type="image/png")


