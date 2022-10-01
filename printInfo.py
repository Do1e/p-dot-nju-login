import json
import requests
import time
import pandas as pd

import config

def int2ipv4(ip: int) -> str:
    l = [ip >> 24 & 0xff, ip >> 16 & 0xff, ip >> 8 & 0xff, ip & 0xff]
    return '.'.join([str(i) for i in l])

def printInfo(session: requests.session) -> None:
    try:
        res = session.get(config.userInfoURL % int(time.time() * 1000), \
            timeout=config.getTimeout)
        if res:
            data = json.loads(res.text)
            print(data['results']['rows'][0]['username'], end=' ')
            print(data['results']['rows'][0]['fullname'])
            print('余额: %.2f元' % (data['results']['rows'][0]['balance'] / 100))
        else:
            print('获取用户信息失败')
    except Exception:
        print('获取用户信息失败')

    try:
        res = session.get(config.onListURL, timeout=config.getTimeout)
        if res:
            data = json.loads(res.text)
            dataFrame = pd.DataFrame(data['results']['rows'])
            print('在线设备:')
            dataFrame[['acctstarttime']] = dataFrame[['acctstarttime']].applymap( \
                lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))
            dataFrame[['user_ipv4']] = dataFrame[['user_ipv4']].applymap(int2ipv4)
            dataFrame = dataFrame[['acctstarttime', 'user_ipv4', 'mac']]
            dataFrame.columns = ['login time', 'IP addr', 'MAC addr']
            print(dataFrame.to_string(index=False))
        else:
            print('获取在线设备失败')
    except Exception:
        print('获取在线设备失败')

if __name__ == '__main__':
    session = requests.session()
    session.headers = config.headers
    printInfo(session)