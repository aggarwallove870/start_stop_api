# from accounts.cities import cities

# CUSTOMER = 'C'
# VENDOR = 'V'
# SELLER = 'S'
ADMIN = 'A'
HR = 'H'
STAFF = 'F'
EMPLOYEE = 'E'
# BLOGGER = 'B'

user_types = (
    # (CUSTOMER, 'Customer'),
    # (SELLER, 'Seller'),
    # (VENDOR, 'Vendor'),
    (HR, 'HR Department'),
    (ADMIN, 'Admin'),
    (STAFF, 'Staff'),
    (EMPLOYEE, 'Employee'),
    # (BLOGGER, 'Blogger'),
)

# price_types = (
    # (CUSTOMER, 'Customer'),
    # (SELLER, 'Seller'),
    # (VENDOR, 'Vendor'),
    # (ADMIN, 'Admin')
# )

states = [
    ('1', 'Andaman and Nicobar Islands'),
    ('2', 'Andhra Pradesh'),
    ('3', 'Arunachal Pradesh'),
    ('4', 'Assam'),
    ('5', 'Bihar'),
    ('6', 'Chandigarh'),
    ('7', 'Chhattisgarh'),
    ('8', 'Dadra and Nagar Haveli'),
    ('9', 'Daman and Diu'),
    ('10', 'Delhi'),
    ('11', 'Goa'),
    ('12', 'Gujarat'),
    ('13', 'Haryana'),
    ('14', 'Himachal Pradesh'),
    ('15', 'Jammu and Kashmir'),
    ('16', 'Jharkhand'),
    ('17', 'Karnataka'),
    ('18', 'Kenmore'),
    ('19', 'Kerala'),
    ('20', 'Lakshadweep'),
    ('21', 'Madhya Pradesh'),
    ('22', 'Maharashtra'),
    ('23', 'Manipur'),
    ('24', 'Meghalaya'),
    ('25', 'Mizoram'),
    ('26', 'Nagaland'),
    ('27', 'Narora'),
    ('28', 'Natwar'),
    ('29', 'Odisha'),
    ('30', 'Paschim Medinipur'),
    ('31', 'Pondicherry'),
    ('32', 'Punjab'),
    ('33', 'Rajasthan'),
    ('34', 'Sikkim'),
    ('35', 'Tamil Nadu'),
    ('36', 'Telangana'),
    ('37', 'Tripura'),
    ('38', 'Uttar Pradesh'),
    ('39', 'Uttarakhand'),
    ('40', 'Vaishali'),
    ('41', 'West Bengal'),
]


# def citiestuple(sid):
#     return tuple([[i['id'], i['name']] for i in cities[sid]])
#
#
# def findcityname(c, sid):
#     for i in cities[sid]:
#         if c == i['id']:
#             return i['name']

# def citieschoices():
#     CITIES = [['', 'Select City']]
#     for i in states:
#         for c in i['cities']:
#             CITIES.append([c['id'], c['name']]),
#     return CITIES

# import requests
#
# def getcities(stateid):
#     url = f'https://www.swachhcycle.in/admin/config/functions_ajax.php?country=101&state={stateid}'
#     return requests.get(url).text

# for i in states:
# c = getcities(1)


# def createcitiesjson():
#     citiex = {}
#     for i in states:
#         stateid = i[0]+1
#         statecities = getcities(stateid)
#         statecities = statecities.strip()
#
#         statecities = statecities.replace('<select class="form-control" name="city" id="city">', '')
#         statecities = statecities.replace('</select>', '')
#         cts = []
#         for i in statecities.split('</option>'):
#             name = i.split('">')
#             try:
#                 actualname = name[1]
#                 if actualname != 'Select':
#                     for value in name:
#                         try:
#                            actualvalue = value.split('value="')[1]
#                            cts.append({'id':actualvalue, 'name': actualname})
#                         except:
#                             pass
#             except:
#                 pass
#         citiex[stateid] = cts
#
#     with open('cities.json', 'w+') as file:
#         file.write(str(citiex))
#
# createcitiesjson()
