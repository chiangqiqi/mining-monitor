"""短信相关工具"""

import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta
from .config import sms_log_tab


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

        params = urlencode({"apikey": self.key,
                            "text": content, 'mobile': tele})
        res = requests.post(self.url, params,
                            headers=headers)
        return res

    def send_warning(self, tele, msg):
        return self.send(tele, '【云片网】您的验证码是' + msg)


class SMSDispatcher(SMSSender):
    def __init__(self, apikey, lag):
        """
        短信发送，间隔时间

        lag: 两条之间的间隔
        """
        super().__init__(apikey)
        self.lag = lag

    def _log_sms(self, tele, msg):
        sms_log_tab.insert_one({'tele': tele, 'msg': msg,
                                'update_time': datetime.now()})

    def _last_msg(self, tele):
        cur = sms_log_tab.find({'tele': tele}).sort('_id', -1).limit(1)
        next((x for x in cur), None)

    def _shoud_send(self, tele):
        """
        是否需要发送短信
        """
        lag = timedelta(seconds=self.lag)
        last_sms = self._last_msg(tele)

        if last_sms is None:
            return True

        last_time = last_sms['update_time']
        return last_time+lag < datetime.now()

    def send_warning(self, tele, msg):
        """
        发送短信
        """
        if self._shoud_send(tele):
            super.send_warning(tele, msg)
