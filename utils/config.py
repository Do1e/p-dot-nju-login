getTimeout = 2

destURL = 'http://p.nju.edu.cn/cas/&renew=true'
pnjuURL = 'http://p.nju.edu.cn/portal/'
userInfoURL = 'http://p.nju.edu.cn/api/portal/v1/getinfo?_=%d'
onListURL = 'http://p.nju.edu.cn/api/selfservice/v1/online?page=1&limit=100&_=%d'
quickLoginInfoURL = 'http://p.nju.edu.cn/api/portal/v1/quicklogin/domain/default?_=%d'
bindURL = 'http://p.nju.edu.cn/api/portal/v1/quicklogin/bind/default'
unbindURL = 'http://p.nju.edu.cn/api/portal/v1/quicklogin/unbind/id/%d'
logoutURL = 'http://p.nju.edu.cn/api/portal/v1/logout'
testURL = 'https://www.baidu.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
}

import urllib3
urllib3.disable_warnings()
getkwargs = {'timeout': getTimeout, 'verify': False}