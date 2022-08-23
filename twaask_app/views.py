# from .models import *
# from .service import *
# from django.urls import reverse
# from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# from django.template.loader import render_to_string
# from django.utils.crypto import get_random_string
# from django.contrib.auth import login as Login, logout as Logout
# from django.shortcuts import render,redirect,HttpResponseRedirect
# from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,authenticate
#
# # Create your views here.
#
# def client_register(request):
#     """
#        Call when Customer want to purchage package or service.
#
#        Parameter:
#            * :param request: request.POST
#            * :param project:
#
#        if :var  request.method == POST
#            * check user details is_valid or not.
#            * if user is_valide then save the user details to employee table.
#            * redirect to package
#        else :
#            * render to twaask/registerclient.html and show error message to user.
#
#         Query = ClientDetail.objects.create(user=user)
#
#        Models and views are using in this View :
#
#        1 View renders page.
#            * Renders HTML Template ( twaask/registerclient.html )
#
#        1 Models :
#            * Project : :model:`django.contrib.Auth.models.User`
#            * PeerApproval : :model:`twaask.models.ClientDetail`
#
#        **Template:**
#
#        :template:`twaask/registerclient.html`
#        """
#
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#
#             client_obj = ClientDetail.objects.create(user=user)
#             client_obj.save()
#
#             return redirect('package')
#     else:
#
#         form = UserCreationForm()
#
#     return render(request, 'twaask/registerclient.html', {'form': form})
#
# def client_login(request,id):
#
#
#     '''
#     Calls when user purckage package or service and it's required for puchage package and service.
#
#     Parameter:
#     * :param request: request.GET.get('service')
#     * :param project: id
#
#
#     if :var  user.is_valid == POST
#         * check user login and login user to website
#
#         if :var  service
#
#             * redirect to paytm_payment with service id
#
#         else:
#
#             * redirect to paytm_payment with package id
#
#
#     Models and views are using in this View :
#
#     1 View renders page.
#         * Renders HTML Template ( twaask/loginclinet.html )
#
#     1 Models :
#         * Project : :model:`twaask.models.ClientDetail`
#         * PeerApproval : :model:`twaask.models.Package`
#         * PeerApproval : :model:`twaask.models.WebProduct`
#
#     **Template:**
#
#     :template:`twaask/loginclinet.html`
#
#     '''
#
#     service = request.GET.get('service')
#
#     data = {}
#     if request.method == 'POST':
#
#         form = AuthenticationForm(data=request.POST)
#         data['form'] = form
#         if form.is_valid():
#
#             user = form.get_user()
#             Login(request, user)
#
#             if not ClientDetail.objects.filter(user=user).exists():
#                 data = {}
#                 data['message'] = 'You have no access please register your account'
#                 return render(request, 'twaask/loginclinet.html', data)
#
#             if service:
#                 url = reverse('paytm_payment')
#                 return HttpResponseRedirect(url + "?serviceid=" + id)
#
#             else:
#                url = reverse('paytm_payment')
#                return HttpResponseRedirect(url + "?packageid=" + id)
#     else:
#         if  not request.user.is_authenticated:
#             form = AuthenticationForm()
#             data['form'] = form
#             if not service:
#                 package_obj = Package.objects.get(id=id)
#                 data['packages'] = package_obj
#             else:
#                 service_obj = WebProduct.objects.get(id=id)
#                 data['sevice'] = service_obj
#         else:
#             if service:
#                 url = reverse('paytm_payment')
#                 return HttpResponseRedirect(url + "?serviceid=" + id)
#
#             else:
#                 url = reverse('paytm_payment')
#                 return HttpResponseRedirect(url + "?packageid=" + id)
#
#     return render(request, 'twaask/loginclinet.html', data)
#
# def twaask_deshboard(request):
#
#     """
#     Render on website deshboard.
#
#     Models and views are using in this View :
#
#     **View**
#
#         * Renders HTML Template (twaask/deshboard.html)
#
#     **Template:**
#
#     :template:`twaask/deshboard.html`
#     """
#
#     return render(request, 'twaask/deshboard.html')
#
# def selection(request):
#     """
#       Render on website selection .
#
#       Models and views are using in this View :
#
#       **View**
#
#           * Renders HTML Template (twaask/selection.html)
#
#       **Template:**
#
#       :template:`twaask/selection.html`
#       """
#
#     return render(request, 'twaask/selection.html')
#
# def package(request):
#
#     '''
#     Show all package after selection of package option.
#
#     if :var  request.method == POST
#
#         Parameter:
#             * :param request: datas['expected_time'] = request.POST.get('date')
#             * :param request: datas['email'] = request.POST.get('email')
#             * :param request:  datas['comment'] = request.POST.get('comment')
#             * :param request: datas['quote_file'] = request.FILES.get('file')
#
#         * create customer details in CustomQuote table.
#
#         * Query =  CustomQuote.objects.create()
#
#     * Query =  Package.objects.all()
#
#     Models and views are using in this View :
#
#     1 View renders page.
#         * Get all package with get request.
#         * Create customer reqiurement detail in customquote tabel and after save data send mail to customer.
#         * Renders HTML Template ( twaask/package.html )
#
#     1 Models :
#         * Project : :model:`flexoffice_app.CustomQuote`
#
#     **Template:**
#
#     :template:`twaask/package.html`
#     '''
#
#     data = {}
#     if request.method == 'POST':
#         datas = {}
#         datas['expected_time'] = request.POST.get('date')
#         datas['email'] = request.POST.get('email')
#         datas['comment'] = request.POST.get('comment')
#         datas['quote_file'] = request.FILES.get('file')
#
#         quote_obj = CustomQuote.objects.create(**datas)
#         quote_obj.save()
#
#         filename = quote_obj.expected_time + '_' + get_random_string(8) + '_tw.pdf'
#         html_out = render_to_string('twaask/requirement_pdf.html', datas)
#         pdf_folder = '/requirement_pdf/'
#         create_pdf(html_out, filename, pdf_folder)
#         client_email = quote_obj.email
#         send_mail(filename, client_email,pdf_folder)
#
#         data['note'] = 'your detail saved. we will reach you in short time...'
#
#     package_obj = Package.objects.all()
#     data['packages'] = package_obj
#
#     return render(request, 'twaask/package.html', data)
#
# def service(request):
#     '''
#         Show all Service after selection of service option and make pagination of all service.
#
#         if :var  request.method == POST
#
#             Parameter:
#                 * :param request: request.POST.get('category')
#
#             if :var cat == 'All'
#
#             * Query =  WebProduct.objects.all()
#
#             else:
#
#                 * Query = WebProduct.objects.filter(web_category__website_category=cat)
#
#         * Query = WebsiteCategory.objects.all()
#
#         Models and views are using in this View :
#
#         1 View renders page.
#             * Get all services with get request.
#             * create pagination of service data.
#             * Renders HTML Template ( twaask/service.html )
#
#         1 Models :
#             * Project : :model:`flexoffice_app.WebProduct`
#
#         **Template:**
#
#         :template:`twaask/service.html`
#         '''
#
#     if request.method == "POST":
#
#         cat = request.POST.get('category')
#
#         if cat == 'All':
#             serv = WebProduct.objects.all()
#         else:
#             serv = WebProduct.objects.filter(web_category__website_category=cat)
#
#     else:
#         serv = WebProduct.objects.all()
#     paginator = Paginator(serv, 12)
#     page = request.GET.get('page',1)
#     serv = paginator.get_page(page)
#     categories = WebsiteCategory.objects.all()
#
#
#     return render(request, 'twaask/service.html', {'sevices': serv,'categories':categories})
#
#
# def logout(request):
#
#     """
#     Logout Customer from website
#
#     """
#
#     Logout(request)
#     return redirect('twaask')
#
#
