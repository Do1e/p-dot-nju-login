import requests
import json
import re
import os
import platform
import subprocess
from time import sleep

from . import config
from .login import login
from .logout import logout

def bind(session: requests.session, name: str) -> None:
    data = ('{"device":"%s"}' % name).encode('utf-8')
    try:
        res = session.post(config.bindURL, data=data, **config.getkwargs)
        data = json.loads(res.text)
        assert data['reply_code'] == 0
        print('已启用设备 %s 的无感认证' % name)
    except Exception:
        print('启用设备 %s 的无感认证失败，检查是否已登录' % name)

def unbind(session: requests.session, deviceID: int) -> None:
    data = '{"id":"%d"}' % deviceID
    try:
        res = session.post(config.unbindURL % deviceID, data='', **config.getkwargs)
        data = json.loads(res.text)
        assert data['reply_code'] == 0
        print('已删除设备 %d 的无感认证' % deviceID)
    except Exception:
        print('删除设备 %d 的无感认证失败，检查是否已登录' % deviceID)

def bindother(mac: str, adapterName: str, name: str) -> None:
    assert adapterName != 'lo' or adapterName != '', "无效的设备名称"
    if platform.system() != 'Linux' or os.geteuid() != 0:
        print('需要在Linux下以超级用户身份运行本程序以启用其他设备的无感认证')
        exit(-1)
    is_mac = re.compile(r'([0-9A-Fa-f]{2})[:-]?([0-9A-Fa-f]{2})[:-]?([0-9A-Fa-f]{2})[:-]?([0-9A-Fa-f]{2})[:-]?([0-9A-Fa-f]{2})[:-]?([0-9A-Fa-f]{2})')
    mac = is_mac.match(mac)
    if not mac:
        print('Mac地址无效')
        return
    mac = ':'.join(mac.groups()).lower()

    # 记录当前mac地址，以便恢复
    try:
        orMAC = subprocess.check_output(['cat', '/sys/class/net/%s/address' % adapterName], stderr=subprocess.STDOUT).decode()[:-1]
    except subprocess.CalledProcessError:
        print('网卡 %s 不存在' % adapterName)
        return
        
    print('修改网卡%s的Mac地址：%s -> %s' % (adapterName, orMAC, mac))
    os.system('ifconfig %s down && ifconfig %s hw ether %s && ifconfig %s up' % (adapterName, adapterName, mac, adapterName))

    sleep(2)
    l = login()
    if l.login() != 0:
        exit(-1)
    sleep(2)
    bind(l.session, name)
    sleep(2)
    logout(l.session)

    print('还原本机Mac地址')
    os.system('ifconfig %s down && ifconfig %s hw ether %s && ifconfig %s up' % (adapterName, adapterName, orMAC, adapterName))


if __name__ == '__main__':
    session = requests.session()
    session.headers = config.headers
    unbind(session, 16653847324416)
    bind(session, 'Lenovo')