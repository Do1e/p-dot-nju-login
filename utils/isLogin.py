import requests

from . import config

def isLogin() -> bool:
    session = requests.Session()
    session.headers.update(config.headers)
    try:
        res = session.get(config.testURL, **config.getkwargs)
        if res:
            return True
        else:
            return False
    except Exception:
        return False