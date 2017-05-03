import requests
import json

class Monitor(object):
    url='https://eth.waterhole.io:8080/api/accounts/{0}'
    def __init__(self, account):
        "监控矿机运行"
        self.account = account
        
    def _get_minor_info(self):
        """
        得到矿机运行信息
        """
        accurl = self.url.format(self.account)
        res = requests.get(accurl)
        return res

    def work_info(self):
        try:
            resp = self._get_minor_info()
        except requests.exceptions.ConnectionError as e:
            print(e)
            return None

        if resp.status_code is 200:
            resp_parsed = json.loads(resp.text)
            return resp_parsed['workers']
        else:
            return None

    def get_offline_workers(self):
        workers = self.work_info()

        if workers:
            offline_workers = [w for w,v in workers.items() if v['offline']]

            if offline_workers:
                return ",".join(offline_workers)

    def get_online_workers(self):
        workers = self.work_info()
        
        online_workers = [w for w,v in workers.items() if not v['offline']]
        if online_workers:
            return ",".join(online_workers)
