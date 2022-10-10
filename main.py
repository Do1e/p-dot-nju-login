import argparse

import utils

def get_args():
    parser = argparse.ArgumentParser()
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
    return True

if __name__ == '__main__':
    args = get_args()
    if not judge_args(args):
        exit(-1)
    l = utils.login()

    if args.login:
        if l.login() != 0:
            exit(-1)
        session = l.session

    if args.printinfo:
        isLogin = l.isLogin()
        if not isLogin:
            if l.login() != 0:
                exit(-1)
        session = l.session
        utils.printInfo(session)
        if not isLogin:
            utils.logout(session)
    
    if args.add:
        if args.mac and args.network:
            utils.bindother(args.mac, args.network, args.add)
        else:
            isLogin = l.isLogin()
            if not isLogin:
                if l.login() != 0:
                    exit(-1)
            session = l.session
            utils.bind(session, args.add)
            if not isLogin:
                utils.logout(session)

    if args.delete:
        isLogin = l.isLogin()
        if not isLogin:
            if l.login() != 0:
                exit(-1)
        session = l.session
        utils.unbind(session, args.delete)
        if not isLogin:
            utils.logout(session)
    
    if args.logout:
        utils.logout(l.session)