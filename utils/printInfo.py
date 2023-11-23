import json
import requests
import time
import pandas as pd

from . import config

def int2ipv4(ip: int) -> str:
    l = [ip >> 24 & 0xff, ip >> 16 & 0xff, ip >> 8 & 0xff, ip & 0xff]
    return '.'.join([str(i) for i in l])

def printUserInfo(session: requests.session) -> None:
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

def printUseTime(session: requests.session) -> None:
    try:
        res = session.get(config.idURL % int(time.time() * 1000), \
            timeout=config.getTimeout)
        if res:
            data = json.loads(res.text)
            service_id = data['results']['service'][0]['id']
        else:
            print('获取service_id失败')
            return
    except Exception:
        print('获取service_id失败')
        return
    month = int(time.strftime('%m', time.localtime()))
    ts = int(time.time() * 1000)
    try:
        res = session.get(config.useTimeURL % (month, service_id, ts), \
            timeout=config.getTimeout)
        if res:
            data = json.loads(res.text)
            useTime = data['results']['use_volume'] / 60
            h, m = divmod(useTime, 60)
            print('已使用时长: %d小时%d分钟' % (h, m))
        else:
            print('获取使用时长失败')
    except Exception:
        print('获取使用时长失败')

def printOnlineList(session: requests.session) -> None:
    try:
        res = session.get(config.onListURL, **config.getkwargs)
        if res:
            data = json.loads(res.text)
            dataFrame = pd.DataFrame(data['results']['rows'])
            print('在线设备:')
            dataFrame[['acctstarttime']] = dataFrame[['acctstarttime']].map( \
                lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))
            dataFrame[['user_ipv4']] = dataFrame[['user_ipv4']].map(int2ipv4)
            dataFrame = dataFrame[['acctstarttime', 'user_ipv4', 'mac']]
            dataFrame.columns = ['login time', 'IP addr', 'MAC addr']
            print(dataFrame.to_string(index=False))
            return dataFrame
        else:
            print('获取在线设备失败')
    except Exception:
        print('获取在线设备失败')

def printQuickLoginInfo(session: requests.session) -> None:
    try:
        res = session.get(config.quickLoginInfoURL, **config.getkwargs)
        if res:
            data = json.loads(res.text)
            if data['reply_code'] == 404:
                print('没有启用无感认证的设备')
                return None
            else:
                print('无感认证设备:')
                dataFrame = pd.DataFrame(data['results']['rows'])
                dataFrame = dataFrame[['device', 'mac', 'id']]
                dataFrame.columns = ['device name', 'MAC addr', 'device id']
                print(dataFrame.to_string(index=False))
                return dataFrame
        else:
            print('获取无感认证设备失败')
    except Exception:
        print('获取无感认证设备失败')

def printInfo(session: requests.session) -> None:
    printUserInfo(session)
    printUseTime(session)
    printOnlineList(session)
    printQuickLoginInfo(session)

if __name__ == '__main__':
    session = requests.session()
    session.headers = config.headers
    printInfo(session)
