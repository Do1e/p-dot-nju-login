import requests
import time
from lxml import etree

import getQR
import config
from clear import clear
from printInfo import printInfo

class login:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = config.headers

    def getStatus(self, qr: getQR.QR) -> str:
        url =config.statusURL % (qr.ts, qr.QRid)
        session = self.session
        status = session.get(url, timeout=config.getTimeout).text
        return status

    def testLogin(self, qr: getQR.QR) -> int:
        first0, first2 = False, False
        for _ in range(20):
            status = self.getStatus(qr)
            if status == '0' and not first0:
                print('请扫描上述二维码')
                first0 = True
            elif status == '2' and not first2:
                print('请在手机上确认登录')
                first2 = True
            elif status == '1':
                clear()
                print('登录成功')
                break
            time.sleep(1)
        if status != '1':
            print('登录超时请重试')
            return -1
        return 0

    def isLogin(self) -> bool:
        try:
            res = self.session.get(config.testURL, timeout=config.getTimeout)
            if res:
                return True
            else:
                return False
        except Exception:
            return False

    def login(self) -> int:
        if self.isLogin():
            print('已登录')
            return 0
        html = self.session.get(config.loginPURL, timeout=0.2).text

        qr = getQR.QR(self.session)
        clear()
        qr.printQR()
        if self.testLogin(qr) != 0:
            exit(-1)

        selector = etree.HTML(html)
        data = {
            'lt': selector.xpath('//input[@name="lt"]/@value')[0],
            'uuid': qr.QRid,
            'dllt': selector.xpath('//input[@name="dllt"]/@value')[0],
            'execution': selector.xpath('//input[@name="execution"]/@value')[0],
            '_eventId': selector.xpath('//input[@name="_eventId"]/@value')[0],
            'rmShown': selector.xpath('//input[@name="rmShown"]/@value')[0]
        }
        res = self.session.post(config.loginPURL, data=data, timeout=config.getTimeout)
        if res:
            printInfo(self.session)
            return 0
        else:
            return -1


if __name__ == '__main__':
    l = login()
    exit(l.login())
