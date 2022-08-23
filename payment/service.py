import stripe
from twaask_app.models import *
from .checksum import *


try:
    from flexoffice.local import HOST
    HOST = HOST
except:
    from flexoffice.production import HOST
    HOST = HOST


Publishable_key = 'pk_test_P2OV6eHhyuSnugUl03wcHOQL00Sg2KufQY'
Secret_key = 'sk_test_mO2KSDNsEX7ogTgFDTMpzNJE00w39EiFt'
stripe.api_key = 'sk_test_mO2KSDNsEX7ogTgFDTMpzNJE00w39EiFtp'
Merchant_ID = 'WorldP64425807474247'
Merchant_Key = 'kbzk1DSbJiV_O3p5'

# Merchant_ID = 'qUlJnU46183963471905'
# Merchant_Key = 'NXdDSXm7qXh5SaA_'


#create stripe detail for stripe payment.....
def get_screte(id):

    if Package.objects.filter(id=id).exists():

        package_obj = Package.objects.get(id=id)
        amount = int(package_obj.package_price) * 100
        intent = stripe.PaymentIntent.create(amount=amount,currency='usd',payment_method_types=['card'],
                                             description="Software development services",
                                             receipt_email='gaurav@snakescript.com',
                                             shipping={
                                                 'name': 'Gaurav Mandhotra',
                                                 'address': {
                                                     'line1': '510 Townsend St','postal_code': '98140',
                                                     'city': 'San Francisco','state': 'CA','country': 'US',
                                                 }
                                             }
                                             )
        return intent
    return None


#create unique_orderid for paytm....
def unique_orderid():

    Strings = string.ascii_uppercase + string.ascii_lowercase
    newiD = 'TWAASK-' + ''.join(random.choice(Strings) for object in Strings)[:12]
    while PaymentMethod.objects.filter(paytm_orderid=newiD).exists():
        newiD = 'TWAASK-' + ''.join(random.choice(Strings) for object in Strings)[:12]
    return newiD

# def initiate_transaction():
#     paytmParams = {}
#
#
#     paytmParams['body'] = {
#
#         'requestType': 'Payment',
#         'mid': 'qUlJnU46183963471905',
#         'websiteName': 'WEBSTAGING',
#         'orderId': orderid,
#         'callbackUrl': 'http://127.0.0.1:8000/payment/handlerequest/',
#         'txnAmount': {
#             'value': '500',
#             'currency': 'INR',
#         },
#         'userInfo': {
#             'custId': 'gaurav@snakescript.com',
#         },
#     }
#     checksum = generate_checksum_by_str(json.dumps(paytmParams['body']), 'NXdDSXm7qXh5SaA_')
#     paytmParams['head'] = {
#         'signature': checksum
#     }
#     post_data = json.dumps(paytmParams)
#     url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=qUlJnU46183963471905&orderId="+orderid
#     response = requests.post(url, data=post_data, headers={'Content-type': 'application/json'}).json()
#
#     return response

def get_discount(week, month, package_acount):
    data = {}
    if week == 1 and month == 0:
        percent = get_percentage('w')

        discount_acount = package_acount/percent
        total_amount = package_acount-discount_acount
        data['total_amount'] = total_amount
        data['discount_acount'] = discount_acount

    elif week > 1 and month == 0 and week < 4:
        percent = get_percentage('b')
        discount_acount = (package_acount*week) / percent
        total_amount = (package_acount*week) - discount_acount
        data['total_amount'] = total_amount
        data['discount_acount'] = discount_acount

    elif month > 0 and month < 3:
        percent = get_percentage('m')
        week_amu = package_acount * week
        month_amu = (package_acount * month)*4
        discount_acount = (month_amu + week_amu)/percent
        total_amount = (month_amu + week_amu) - discount_acount
        data['total_amount'] = total_amount
        data['discount_acount'] = discount_acount

    elif month > 2 and month < 6:
        percent = get_percentage('q')
        week_amu = package_acount * week
        month_amu = (package_acount * month)*4
        discount_acount = (month_amu + week_amu) / percent
        total_amount = (month_amu + week_amu) - discount_acount
        data['total_amount'] = total_amount
        data['discount_acount'] = discount_acount


    elif month > 5 and month < 12:
        percent = get_percentage('h')
        week_amu = package_acount * week
        month_amu = (package_acount * month)*4
        discount_acount = (month_amu + week_amu) / percent
        total_amount = (month_amu + week_amu) - discount_acount
        data['total_amount'] = total_amount
        data['discount_acount'] = discount_acount

    elif month == 12:
        percent = get_percentage('y')
        week_amu = package_acount * week
        month_amu = (package_acount * month)*4
        discount_acount = (month_amu + week_amu) / percent
        total_amount = (month_amu + week_amu) - discount_acount
        data['total_amount'] = total_amount
        data['discount_acount'] = discount_acount

    return data

def get_percentage(discount_name):
    if DiscountPackage.objects.filter(discount_name=discount_name).exists():
        discount_obj = DiscountPackage.objects.filter(discount_name=discount_name).first()
        dis_percentage = discount_obj.discount_percentage
    else:
        dis_percentage = 0
    return dis_percentage
