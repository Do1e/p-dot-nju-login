getTimeout = 2

QRidURL = 'https://authserver.nju.edu.cn/authserver/qrCode/get?ts=%d'
QRURL = 'https://authserver.nju.edu.cn/authserver/qrCode/code?uuid=%s'
statusURL = 'https://authserver.nju.edu.cn/authserver/qrCode/status?ts=%d&uuid=%s'
loginPURL = 'https://authserver.nju.edu.cn/authserver/login?service=http://p.nju.edu.cn/cas/&renew=true'
pnjuURL = 'http://p.nju.edu.cn/portal/'
userInfoURL = 'http://p.nju.edu.cn/api/portal/v1/getinfo?_=%d'
onListURL = 'http://p.nju.edu.cn/api/selfservice/v1/online?page=1&limit=100&_=%d'
quickLoginInfoURL = 'http://p.nju.edu.cn/api/portal/v1/quicklogin/domain/default?_=%d'
logoutURL = 'http://p.nju.edu.cn/api/portal/v1/logout'
testURL = 'https://www.baidu.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
}