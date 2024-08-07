import argparse
import requests
import NJUlogin

import utils

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loginlib', type=str, metavar='loginlib', default='QRlogin', help='login library, QRlogin or pwdLogin, default is QRlogin')
    parser.add_argument('-u', '--username', type=str, metavar='username', help='username, only used when loginlib is pwdLogin')
    parser.add_argument('-w', '--password', type=str, metavar='password', help='password, only used when loginlib is pwdLogin')
    parser.add_argument('-i', '--login', action='store_true', default=False, help='login')
    parser.add_argument('-o', '--logout', action='store_true', default=False, help='logout')
    parser.add_argument('-p', '--printinfo', action='store_true', default=False, help='print info')
    parser.add_argument('-a', '--add', type=str, metavar='name', help='add device as quick login device, please specify device name')
    parser.add_argument('-m', '--mac', type=str, metavar='mac_addr', help='set if you want to add other device as quick login device, please specify device mac address')
    parser.add_argument('-n', '--network', type=str, metavar='network_adapter_name', help="set if you want to add other device as quick login device, please specify this computer's network adapter name, use ifconfig to get the name")
    parser.add_argument('-d', '--delete', type=int, metavar='id', help='delete quick login device by id, use -p to get id first')
    return parser.parse_args()

def judge_args(args: argparse.Namespace) -> bool:
    if not (args.login or args.logout or args.printinfo or args.add or args.delete):
        print('No argument specified, use -h to get help')
        return False
    if args.login and args.logout:
        print('Error: cannot login and logout at the same time')
        return False
    if args.loginlib == 'pwdLogin' and (args.username is None or args.password is None):
        print('Error: username and password must be specified when loginlib is pwdLogin')
        return False
    return True

if __name__ == '__main__':
    dest = utils.config.destURL
    args = get_args()
    if not judge_args(args):
        exit(-1)
    if args.loginlib == 'QRlogin':
        loginlib = NJUlogin.QRlogin(headers=utils.config.headers)
    elif args.loginlib == 'pwdLogin':
        loginlib = NJUlogin.pwdLogin(args.username, args.password, headers=utils.config.headers)
    else:
        print('Error: loginlib must be QRlogin or pwdLogin')
        exit(-1)

    if args.login:
        session = loginlib.login(dest)
        if session is None:
            raise Exception('Login failed')

    if args.printinfo:
        isLogin = utils.isLogin()
        if not isLogin:
            session = loginlib.login(dest)
            if session is None:
                raise Exception('Login failed')
        else:
            session = requests.Session()
            session.headers.update(utils.config.headers)
        utils.printInfo(session)
        if not isLogin:
            utils.logout()

    if args.add:
        if args.mac and args.network:
            utils.bindother(args.mac, args.network, args.add)
        else:
            isLogin = utils.isLogin()
            if not isLogin:
                session = loginlib.login(dest)
                if session is None:
                    raise Exception('Login failed')
            else:
                session = requests.Session()
                session.headers.update(utils.config.headers)
            utils.bind(session, args.add)
            if not isLogin:
                utils.logout()

    if args.delete:
        isLogin = utils.isLogin()
        if not isLogin:
            session = loginlib.login(dest)
            if session is None:
                raise Exception('Login failed')
        else:
            session = requests.Session()
            session.headers.update(utils.config.headers)
        utils.unbind(session, args.delete)
        if not isLogin:
            utils.logout()

    if args.logout:
        utils.logout()

    loginlib.logout()
