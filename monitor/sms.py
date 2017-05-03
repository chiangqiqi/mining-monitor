import configparser
import requests
from urllib.parse import urlencode

class SMSSender(object):
    def __init__(self, apikey):
        "init with a key"
        self.key = apikey
        self.url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send(self, tele, content):
        """
        发送短信
        tele: 手机号
        content: 要发送的内容
        """
        if not isinstance(tele, str):
            raise ValueError("telephone number need to be a string")

        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"}

        params = urlencode({"apikey":self.key,"text": content,'mobile': tele})
        res = requests.post(self.url,params,
                            headers=headers)
        return res

    def send_warning(self, tele, msg):
        return self.send(tele, '【云片网】您的验证码是' + msg)
