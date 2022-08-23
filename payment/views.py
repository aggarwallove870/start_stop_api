from .service import *
from django.http import JsonResponse
from twaask_app.service import *
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def create_payment_method(data):
    method_obj = PaymentMethod.objects.create(**data)
    method_obj.save()
    return method_obj
@login_required(login_url='selection')
def stripe_payment(request):
    packageid = request.GET.get('packageid')
    clinetid = request.GET.get('clientid')
    if request.method == 'POST':

        if ClientDetail.objects.filter(user__id=clinetid).exists() and Package.objects.filter(id=packageid).exists():
            client_obj = ClientDetail.objects.get(user__id=clinetid)
            package_obj = Package.objects.get(id=packageid)
            data = {}
            data['amount'] = request.POST.get('amount')
            data['currency'] = request.POST.get('currency')
            data['payment_id'] = request.POST.get('payment_id')
            data['client_secret'] = request.POST.get('client_secret')
            data['msg'] = request.POST.get('error_msg')
            data['payment_error_id'] = request.POST.get('errorid')

            status = request.POST.get('status')

            if status == 'True':

                method_obj = create_payment_method(data)

                purchage_obj = PurchasedHistory.objects.create(package=package_obj,client=client_obj,payment_method=method_obj)
                purchage_obj.save()

                return redirect('package')

            elif status == 'False':
                method_obj = create_payment_method(data)

                purchage_obj = PurchasedHistory.objects.create(package=package_obj, client=client_obj,payment_method=method_obj)
                purchage_obj.save()
            data = {}
            data['Unsuccess'] = 'Unsuccess'
            return JsonResponse(data)

    else:

        data = {}
        payment_intente = get_screte(packageid)
        data['client_secret'] = payment_intente.client_secret
        data['amount'] = payment_intente.amount/100

        return render(request, 'payment/collect_detail.html', data)

@login_required(login_url='selection')
def paytm_payment(request):
    """
    Call after client login for purchase service and package. If client wants to purchase package this function render package quantity selection page after selection of quantity with post request it
    calculate quantity of package after calculation it check package quantity if quantity is zero it will show message to client. If quantity is not zero  then it calculate discount package if discount
     is available and  add save all payment details in purchase history table and redirect client to paytm payment page. Where client can make a payment to package with call back url.
    If client wants to purchase service then it calculate discount of services automatically and save purchase detail in purchase history table. And redirect to paytm payment page with call back url.
    If payment is successful or failed. It redirect to handle request function with response of payment.


    Parameter:
          * :param request:  packageid = request.GET.get('packageid')
          * :param request:  serviceid = request.GET.get('serviceid')
          * :param request:  clinet = request.user
          * :param project:


    if :var  packageid

        * Get package details by packageid from package table and get package amount.get discount details of package.

        if : var request.method == 'POST'

            * calculate total amount of package with discount of table.
            * make cart with total amount and customer detail with unique order id.
            * save payment detail with unsuccess payment for make payment request

            if : week > 0 or  month > 0

            * check month and week is not 0.

            else :

                * note = 'Please select month or week'
                * render to twaask/package_quntity_selection.html with note message

        else :

        * render to twaask/package_quntity_selection.html with package amount

    else:
        * Get service details by service id.
        * calculate service discount amount.
        * make cart with total amount and customer detail with unique order id.
        * save payment detail with unsuccess payment for make payment request
        * render to twaask/package_quntity_selection.html with payment details

    Models and views are using in this View :

    1 View renders page.

    if packageid:

        * Calculation employee salary details
        * Renders HTML Template ( twaask/package_quntity_selection.html )

    else:
        * Renders HTML Template ( payment/paytm_payment.html )


    1 Models :

    * Project : :model:`twaask.models.ClientDetail`
    * PeerApproval : :model:`twaask.models.Package`
    * PeerApproval : :model:`twaask.models.WebProduct`

    **Template:**
    if packageid:

        :template:`twaask/package_quntity_selection.html`

    else:

        :template:`payment/paytm_payment.html`
    """

    packageid = request.GET.get('packageid')
    serviceid = request.GET.get('serviceid')
    clinet = request.user
    param_dict = {}
    if packageid:
        package_obj = Package.objects.get(id=packageid)
        package_acount = package_obj.package_price
        data = DiscountPackage.objects.all()
        if request.method == 'POST':
            week = int(request.POST.get('week', 0))
            month = int(request.POST.get('month', 0))
            if week > 0 or  month > 0:

                orderid = unique_orderid()
                if ClientDetail.objects.filter(user=clinet).exists() and Package.objects.filter(id=packageid).exists():
                    client_obj = ClientDetail.objects.get(user=clinet)

                    amount = get_discount(week, month, package_acount)
                    if amount.get('total_amount'):

                        if orderid:
                            data = {}
                            data['paytm_orderid'] = orderid
                            data['currency'] = 'INR'
                            data['amount'] = amount['total_amount']
                            data['discount_amount'] = amount['discount_acount']
                            method_obj = create_payment_method(data)

                            if method_obj:


                                purchage_obj = PurchasedHistory.objects.create(package=package_obj, client=client_obj,
                                                                               payment_method=method_obj)
                                purchage_obj.save()
                                url = '/payment/handlerequest/?packageid='+packageid+'&week='+str(week)+'&month='+str(month)

                                param_dict = {

                                            'MID': Merchant_ID,
                                            'ORDER_ID': orderid,
                                            'TXN_AMOUNT': str(amount['total_amount']),
                                            'CUST_ID': str(clinet.email),
                                            'INDUSTRY_TYPE_ID': 'Retail',
                                            'WEBSITE': 'WEBSTAGING',
                                            'CHANNEL_ID': 'WEB',
                                            'CALLBACK_URL':HOST+url,

                                    }
                                param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, Merchant_Key)
                    return render(request, 'payment/paytm_payment.html', {'param_dict': param_dict})
                else:
                    note = 'Please try again later'
                    return render(request, 'twaask/package_quntity_selection.html', {'note': note,'discounts':data, 'package_acount': package_acount})

            else:
                note = 'Please select month or week'
                return render(request, 'twaask/package_quntity_selection.html', {'note': note,'discounts':data, 'package_acount': package_acount})
        return render(request, 'twaask/package_quntity_selection.html', {'discounts':data, 'package_acount': package_acount})
    else:

        service_obj = WebProduct.objects.get(id=serviceid)

        if service_obj.discount_percentage:
            discount = service_obj.price / service_obj.discount_percentage
        else:
            discount = 0
        service_acount = service_obj.price - discount

        orderid = unique_orderid()

        if ClientDetail.objects.filter(user=clinet).exists() and WebProduct.objects.filter(id=serviceid).exists():
            client_obj = ClientDetail.objects.get(user=clinet)

            if orderid:
                    data = {}
                    data['paytm_orderid'] = orderid
                    data['currency'] = 'INR'
                    data['amount'] = service_acount
                    data['discount_amount'] = discount
                    method_obj  = create_payment_method(data)

                    if method_obj:
                        purchage_obj = PurchasedHistory.objects.create(sevice=service_obj, client=client_obj,
                                                                       payment_method=method_obj)
                        purchage_obj.save()
                        url = '/payment/handlerequest/?serviceid='+serviceid

                        param_dict = {

                            'MID': Merchant_ID,
                            'ORDER_ID': orderid,
                            'TXN_AMOUNT': str(service_acount),
                            'CUST_ID': str(clinet.email),
                            'INDUSTRY_TYPE_ID': 'Retail',
                            'WEBSITE': 'WEBSTAGING',
                            'CHANNEL_ID': 'WEB',
                            'CALLBACK_URL': HOST + url,

                        }
                        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, Merchant_Key)

        return render(request, 'payment/paytm_payment.html', {'param_dict': param_dict})

@csrf_exempt
def handlerequest(request):
    """
       Call after payment with a response of payment and save payment details in purchase history table.
       After getting response of payment it check checksum is if checksum is true it update the response of
       payment in purchase payment table of package or service. After update it create pdf of payment automatically and
       send email to client  and admin from website of all payment details.

        Parameter:
              * :param request:  packageid = request.GET.get('packageid')
              * :param request:  serviceid = request.GET.get('serviceid')
              * :param request:  form = request.POST
              * :param request:   week = int(request.GET.get('week'))
              * :param request:  int(request.GET.get('month'))

        if :var  packageid

            * Get package details by package id from package table.
            * calculate total week of package

        if : var serviceid

            * Get package details by service id from service table.

        * get all response data and checksum id from form.
        * verify data from checksum function with response data, merchant id and checksum code.

        if : var verify

              * create pdf of payment details and send to customer email id.
              * update puchage details in purhage history table.
              * render purchage details to payment/payment_done.html page

        else :

        * make payment unsuccess and update puchage history with order id.
        * render to payment/payment_cancle.html and show error message to user


        Models and views are using in this View :

        1 View renders page.



        1 Models :

        * Project : :model:`twaask.models.ClientDetail`
        * PeerApproval : :model:`twaask.models.Package`
        * PeerApproval : :model:`twaask.models.WebProduct`

        **Template:**

         if : var verify:

            :template:`payment/payment_done.html`

        else :

             :template:`payment/payment_cancle.html`

        """

    packageid = request.GET.get('packageid')
    serviceid = request.GET.get('serviceid')
    if packageid:
        package_obj = Package.objects.get(id=packageid)
        week = int(request.GET.get('week'))
        month  = int(request.GET.get('month')) * 4
        total_week = month + week
    if serviceid:
        service_obj = WebProduct.objects.get(id=serviceid)
    checksum = None
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict, Merchant_Key, checksum)

    if verify:

        if response_dict['RESPCODE'] == '01':

            if PaymentMethod.objects.filter(paytm_orderid=response_dict['ORDERID']).exists():
                obj = PaymentMethod.objects.filter(paytm_orderid=response_dict['ORDERID'])
                obj_user = obj[0].purchasedhistory_set.first().client.user
                filename = str(obj_user) + '_' + get_random_string(8) + '_tw.pdf'

                if not obj[0].pdf_name:

                    obj.update(payment_id=response_dict['TXNID'], payment_status='s', pdf_name=filename)

                    data = {}
                    if packageid:
                        data['total_week'] = total_week
                        data['package_obj'] = package_obj
                    if serviceid:
                        data['total_week'] = 1
                        data['service_obj'] = service_obj
                    data['total_amount'] = obj[0].amount + obj[0].discount_amount
                    data['user'] = obj_user
                    data['payment_amount'] = obj[0].amount
                    data['discount_amount'] = obj[0].discount_amount
                    data['payment_id'] = obj[0].payment_id
                    html_out = render_to_string('twaask/payment_pdf.html', data)
                    pdf_folder = '/payment_pdf/'
                    create_pdf(html_out, filename,pdf_folder)
                    client_email = obj_user.email
                    send_mail(filename,client_email,pdf_folder)

            return render(request, 'payment/payment_done.html', {'response': response_dict,'discount_amount':obj[0].discount_amount})
        else:
            if PaymentMethod.objects.filter(paytm_orderid=response_dict['ORDERID']).exists():
                obj = PaymentMethod.objects.filter(paytm_orderid=response_dict['ORDERID'])
                obj.update(payment_status='u',msg=response_dict['RESPMSG'])
    return render(request, 'payment/payment_cancle.html', {'response': response_dict})

def discount_detail(request):

    """
    Get package discount details.

    """
    detail = {}
    if request.method == "POST":
        month = int(request.POST.get('month',0))
        week = int(request.POST.get('week',0))
        amount = float(request.POST.get('amount',0))
        detail = get_discount(week, month, amount)

        return JsonResponse(detail)

    return JsonResponse(detail)





