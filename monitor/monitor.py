import requests
import json
import logging
from threading import Thread
from time import sleep

from .utils import send_warning
from .config import accounts_tab

class WaterPool(object):
    url='https://eth.waterhole.io:8080/api/accounts/{0}'
    def __init__(self, account=''):
        "获取账户对应的worker 信息"
        # self.account = account
        pass

    def _get_minor_info(self, account):
        """
        得到矿机运行信息
        """
        accurl = self.url.format(account)
        res = requests.get(accurl,timeout=2)
        return res

    def work_info(self, account):
        try:
            resp = self._get_minor_info(account)
        except requests.exceptions.ConnectionError as e:
            logging.warning(e)
            return None

        if resp.status_code is 200:
            resp_parsed = json.loads(resp.text)
            return resp_parsed['workers']
        else:
            return None

    def get_workers(self, account):
        """
        返回在线矿工和离线矿工列表
        """
        workers = self.work_info(account)

        logging.info('workers list {0}'.format(workers))
        if workers:
            offline_workers = [w for w, v in workers.items()
                               if v['offline']]
            online_workers = [w for w, v in workers.items()
                              if not v['offline']]

            return ",".join(offline_workers), ",".join(online_workers)
        else:
            return None, None

class Monitor:
    def __init__(self):
        """
        监控运行
        """
        self.pool = WaterPool()
        # self.tele = tele

    def check_status(self, account, tele):
        offline, online = self.pool.get_workers(account)
        if offline is not None:
            pattern = "【矿机监控】{0}矿机运行中, {1}掉线"
            res = send_warning(tele,
                               pattern.format(str(online),
                                              str(offline)[:10]+'...'))
            print(res.text)
            
    def run(self, jiange):
        while(1):
            cur = accounts_tab.find()
            for acc in cur:
                logging.info('checking account {0} status'.format(acc['account']))
                try:
                    res = self.check_status(acc['account'], acc['tele'])
                except:
                    logging.warning('checking status error')
            sleep(jiange)
