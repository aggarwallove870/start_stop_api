import re
import jwt
import random
import string
from datetime import datetime,date,timedelta
from .config import SECRET,RESET_PASSWORD_EXPIRY_TIME


def check_username(username):
    if re.match("^[A-Za-z0-9]*$", username):
        return True
    else:
        return False

def valid_date(token_date):
    current_date = datetime.now().date()
    striped_date = datetime.strptime(token_date, '%y, %m %d').date()
    Date = current_date-striped_date
    if not Date:
        return  True
    else:
        return False


def valid_time(token_time):
    current_time = datetime.now().time()
    stoken_time  = datetime.strptime(token_time, '%H,%M,%S').time()
    str_ctime    = str(current_time)
    str_Ttime    = str(stoken_time)
    stripd_Ctime = str_ctime[:str_ctime.rfind(':')]
    stripd_Ttime = str_Ttime[:str_Ttime.rfind(':')]

    ctH , ctM = stripd_Ctime[:stripd_Ctime.rfind(':')],stripd_Ctime[stripd_Ctime.rfind(':')+1:]
    TtH, TtM = stripd_Ttime[:stripd_Ttime.rfind(':')], stripd_Ttime[stripd_Ttime.rfind(':') + 1:]
    current = timedelta(hours=int(ctH),minutes=int(ctM))
    TOKEN_TIME = timedelta(hours=int(TtH),minutes=int(TtM))
    getTime = current - TOKEN_TIME
    hours_minutes = str(getTime)[:str(getTime).rfind(':')]
    Hours = int(hours_minutes[:hours_minutes.rfind(':')])
    Minutes = int(hours_minutes[hours_minutes.rfind(':')+1:])
    if Hours == 0 and Minutes <= RESET_PASSWORD_EXPIRY_TIME  :
        return True
    else:
        return False

def makesecret():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    random_letters = ''.join(random.choice(letters) for i in letters)
    secret = random_letters[:60]
    return secret

def secretMessage(messge):
    data = {'message':messge}
    return jwt.encode(data, SECRET, algorithm='HS256').decode('ascii')


def makeJWT(username,secret):
    data = {'key': secret,'username':username}
    return jwt.encode(data, SECRET, algorithm='HS256').decode('ascii')


def make_expiry_JWT(username,secret):
    d = datetime.now()
    data = {'key': secret, 'username': username,
            'time': d.time().strftime("%H,%M,%S"),
            'date': d.date().strftime('%y, %m %d')}

    return jwt.encode(data, SECRET, algorithm='HS256').decode('ascii')


def checkJWT(secret):
    try:
        token = jwt.decode(secret, SECRET, algorithms=['HS256'])
    except:
        token = {}
    return token

def checkExpiryJWT(secret):
    try:
        token = jwt.decode(secret, SECRET, algorithms=['HS256'])
        token_date = valid_date(token['date'])
        token_time = valid_time(token['time'])
        if token_date and token_time:
           return token
        else:
            token = {}
    except:
        token = {}
    return token


