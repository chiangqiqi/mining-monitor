from pymongo import MongoClient

__all__ = ['sms_log_tab', 'accounts_tab']

# 短信发送记录
mc = MongoClient()

sms_log_tab = mc['monitor']['sms_log']
accounts_tab = mc['monitor']['accounts']

apikey = '579e02***2bdfc0c23723edbbba2bd9b'
