import datetime as dtime
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

try:
    from flexoffice.local import HOST
except:
    from flexoffice.production import HOST
host = HOST

def Mailgun_send_email(to,subject,text,html):

    from_email = 'Snake Script Pvt. Ltd.'
    msg = EmailMultiAlternatives(subject, text, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()


def TEXT(secret,request):
    return f'{host}/accounts/create/password/{secret}'
    # return f'http://{request.get_host()}/create-password/{secret}'

def UrlText(request):

    return f'{host}'


def HTML(secret,request,username,employee_uid):

    return  f'Your username is <b>{username}</b> and Your employee id is <b>{employee_uid}</b>' \
            f'<h5><a href="{host}/accounts/create/password/{secret}">Click here to create password</a></h5>'

def createdHTML(secret,request):

    return  f'<h5>Your password has been created. you can login our flax office website</h5>'

def SalaryHTML(request,office_email,object):

    today = datetime.today()
    first = today.replace(day=1)
    lastMonth = first - dtime.timedelta(days=1)
    data ={}
    data['object'] = object
    data['Month'] = lastMonth.month
    data['Year'] = lastMonth.year

    return render_to_string('accounts/render_salarymail.html', data)


    # return f'Hello <b> {object.employeid.first_name}  {object.employeid.last_name}<br>'\
    #        f'<b>EmployeeID - {object.employeid}</b>'\
    #        f' your salary detail for {datetime.now().date().month}  {datetime.now().date()}:<br>'\
    #        f'your total salary = {object.salary.salary_amount}<br>'\
    #        f'your total leave day = {object.total_leave_day}<br>'\
    #        f'your paid leave day = {object.paid_leave_day}<br>' \
    #        f'your unpaid leave day = {object.unpaid_leave_day}<br>'\
    #        f'your bonus = {object.bonus_amount}<br>'\
    #        f'your paid leave amount = {object.paid_leave_amount}<br>'\
    #        f'your unpaid leave amount = {object.unpaid_leave_amount}<br>'\
    #        f'your total paid salary = {object.paid_salary[str(object.paid_leave_amount.find(".")+2):str(object.paid_leave_amount.find(".")+4)]}<br>' \
    #        f'Comments - <br>'\
    #        f'HR, <br>'\
    #        f'Snakescript Solutions LLP <br>'





    # return f'<h5><a href="{request.get_host()}/create-password/{secret}">Click here to create password</a></h5>'

# def ResetTEXT(secret):
#     return f'http://127.0.0.1:8000/accounts/reset_password/{secret}'
#
# def ResetHTML(secret):
#     return f'<h5><a href="http://127.0.0.1:8000/accounts/reset_password/{secret}">Click here to reset yourpassword</a></h5>'
