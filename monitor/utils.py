from .sms import SMSDispatcher
from .config import apikey

sms = SMSDispatcher(apikey, 3600)

def send_warning(tele, msg):
    return sms.send_warning(tele, msg)
