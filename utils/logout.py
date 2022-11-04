import requests
import json

from . import config

def logout() -> None:
    session = requests.Session()
    session.headers.update(config.headers)
    try:
        res = session.post(config.logoutURL, data='{"domain":"default"}', **config.getkwargs)
        data = json.loads(res.text)
        assert data['reply_code'] == 0
        print('已退出')
    except Exception:
        print('退出失败')

if __name__ == '__main__':
    logout()