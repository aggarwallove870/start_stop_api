from django.shortcuts import render,redirect
from accounts.models import *
from accounts.forms import EmployeeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as Login,logout as Logout
from accounts.mailer import *
import string
from django.contrib.sites.shortcuts import get_current_site  
import random
from django.core.mail import EmailMessage
from flexoffice import settings
from django.contrib.auth.hashers import make_password



# Create your views here.
def random_pwd():
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    print(res, 'resss')
    return str(res)


def login(request):

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        print(request.POST, '1')
        if form.is_valid():
            user = form.get_user()
            Login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html',{'fm': form})

    return render(request, 'accounts/login.html',{'form': "form"})


def registration(request):

    if request.method == 'POST':
        password =random_pwd()
        user = User(username=request.POST.get('office_email'), password=make_password(password), email=request.POST.get('office_email'))
        user.save()
        print(user)
        form = EmployeeForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            office_email= form.cleaned_data['office_email']
            phone=form.cleaned_data['phone']
            dob=form.cleaned_data['dob']
            image=form.cleaned_data['image']
            sal=form.cleaned_data['sal']
            permanent_address=form.cleaned_data['permanent_address']
            correspondence_address=form.cleaned_data['correspondence_address']
            department=form.cleaned_data['department']
            employe = Employee.objects.create(first_name=first_name, office_email=office_email,phone=phone,dob=dob,image=image,sal=sal,permanent_address=permanent_address,correspondence_address=correspondence_address,department=department)
            employe.user_id =user.id
            employe.save()
        
            mail_subject = 'Employee login detail'  
            
            print(password, 'passwordddd')
            message = render_to_string('accounts/employee_email.html', {  
                'email': form.cleaned_data['office_email'],   
                'password':password,
            })
            recipient_list =  request.POST.get('office_email')
            email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [recipient_list])  
            email.send() 
            # redirect to a new URL
            return redirect('login')
    else:
        form = EmployeeForm()

    return render(request,'accounts/registration.html',{'form': form})


def createpassword(request,secret):
    """
        Create user password by user when administration send user username and employee id
        on user email id.
        Call this function when user click on email url. url sent by flexoffice administration
        for create use paasword by user itself.

    Parameter:
        * :param request: request.POST
        * :param request: password = request.POST.get('password')
        * :param request: confirm_password = request.POST.get('confirm_password')
        * :param project: secret = secret token for check user request.

        if :var  request.method == POST

            * check user details is_valid or not.

            if : var password == confirm_password

                * check user password and confirm password is matched or not.

                if : var Employee.objects.filter(office_email=username).exists()

                    * check user email exists in employee table or not.

                    if : not User.objects.filter(username=username).exists()

                        * if user password not exists then create user password and sent mail to user for inform of user passowrd has been created.

                    else :
                        * render to accounts/registration.html and show error message to user(Your password already created please check your offce email or contact with office).

                else :
                    * render to accounts/registration.html and show error message to user(Email not match to your office email please check your email).

            else :
                * render to accounts/registration.html and show error message to user(Password not match please enter password again).

        else :
            * render to accounts/registration.html and show error message to user.

         Query = if not Employee.objects.filter(office_email = request.POST.get('office_email')).exists():

        Models and views are using in this View :

        1 View renders page.
            * Renders HTML Template ( accounts/create_password.html )

        1 Models :
            * Project : :model:`accounts.models.Employee`
            * PeerApproval : :model:`django.contrib.Auth.models.User`

        **Template:**

        :template:`accounts/create_password.html`
        """

    data = checkJWT(secret)
    username = data.get('username')
    if username:

        password_created = False
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if request.method == 'POST':
            if password == confirm_password:

                if Employee.objects.filter(office_email=username).exists():

                    if not User.objects.filter(username=username).exists():
                        user_obj = User.objects.create(username=username)
                        Employee.objects.filter(office_email=username).update(user=user_obj)
                        user_obj.set_password(password)
                        user_obj.save()
                        password_created = True
                        token = makesecret()
                        secret = makeJWT(username, token)
                        Mailgun_send_email(username, 'Your Password Created', TEXT(secret, request),
                                           createdHTML(secret, request))

                        return render(request, 'accounts/create_password.html',{'password_created': password_created})

                    else:
                        error = "Your password already created please check your offce email or contact with office"
                        return render(request, 'accounts/create_password.html', {'error': error,'password_created': password_created})
                else:
                    error = "Email not match to your office email please check your email"
                    return render(request, 'accounts/create_password.html', {'error': error,'password_created': password_created})
            else:
                error = "Password not match please enter password again"
                return render(request, 'accounts/create_password.html',
                              {'error': error, 'password_created': password_created})

        return render(request, 'accounts/create_password.html',{'password_created': password_created})
    else:

        user_error = 'username not found please wait for other email or contact your office'
        return render(request, 'accounts/create_password.html', {'user_error': user_error})

def logout(request):
    """
    logout user to website when user want to logout from webiste and send request for logout.

    """
    Logout(request)
    return redirect('login')


