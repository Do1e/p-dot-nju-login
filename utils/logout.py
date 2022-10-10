import requests
import json

from . import config

def logout(session: requests.session) -> None:
    try:
        res = session.post(config.logoutURL, data='{"domain":"default"}', timeout=config.getTimeout)
        data = json.loads(res.text)
        assert data['reply_code'] == 0
        print('已退出')
    except Exception:
        print('退出失败')

if __name__ == '__main__':
    session = requests.session()
    session.headers = config.headers
    logout(session)