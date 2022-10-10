import requests
import json

from . import config

def bind(session: requests.session, name: str) -> None:
    data = ('{"device":"%s"}' % name).encode('utf-8')
    try:
        res = session.post(config.bindURL, data=data, timeout=config.getTimeout)
        data = json.loads(res.text)
        assert data['reply_code'] == 0
        print('已启用当前设备的无感认证')
    except Exception:
        print('启用当前设备的无感认证失败')

def unbind(session: requests.session, deviceID: int) -> None:
    data = '{"id":"%d"}' % deviceID
    try:
        res = session.post(config.unbindURL % deviceID, data='', timeout=config.getTimeout)
        data = json.loads(res.text)
        assert data['reply_code'] == 0
        print('已删除设备 %d 的无感认证' % deviceID)
    except Exception:
        print('删除设备 %d 的无感认证失败' % deviceID)

if __name__ == '__main__':
    session = requests.session()
    session.headers = config.headers
    unbind(session, 16653847324416)
    bind(session, 'Lenovo')