import time
import json
import sys
from argparse import ArgumentParser
from datetime import datetime
from statistics import mean

import requests
from yarl import URL


def set_args():
    p = ArgumentParser()
    p.add_argument('-n', '--num', default=10, type=int, nargs='?',
                   help='number of trials')
    p.add_argument('-o', '--output', type=str, nargs='?',
                   default=datetime.now().isoformat() + '.json',
                   help='output file')
    g = p.add_mutually_exclusive_group()
    g.add_argument('-k', '--kilo', action='store_const', const=10**3,
                   help='prefix: kilo')
    g.add_argument('-m', '--mega', action='store_const', const=10**6,
                   help='prefix: mega (default)')
    g.add_argument('-g', '--giga', action='store_const', const=10**9,
                   help='prefix: giga')

    return p.parse_args()


def main():

    args = set_args()

    urls = [
        'http://ftp.jaist.ac.jp/pub/Linux/ubuntu-releases/artful/ubuntu-17.10.1-server-',
        'http://ubuntutym2.u-toyama.ac.jp/ubuntu/artful/ubuntu-17.10.1-server-',
        'http://releases.ubuntu.com/17.10.1/ubuntu-17.10.1-server-',
        'http://mirrorservice.org/sites/releases.ubuntu.com/17.10.1/ubuntu-17.10.1-server-',
        'http://ubuntu.ipacct.com/releases/artful/ubuntu-17.10.1-server-',
        # 'http://mirror.enzu.com/ubuntu-releases/17.10.1/ubuntu-17.10.1-server-',
        'http://mirror.pop-sc.rnp.br/mirror/ubuntu-releases/artful/ubuntu-17.10.1-server-',
        'http://ftp.belnet.be/ubuntu.com/ubuntu/releases/17.10.1/ubuntu-17.10.1-server-',
        'http://mirrors.mit.edu/ubuntu-releases/17.10.1/ubuntu-17.10.1-server-',
        # 'http://mirror.yandex.ru/ubuntu-releases/17.10.1/ubuntu-17.10.1-server-',
    ]

    urls = [url + 'amd64.iso.zsync' for url in urls]
    tmp = {URL(url).host: [] for url in urls}

    for p in (args.kilo, args.mega, args.giga):
            pre = p
            if pre is not None:
                break
    else:
        pre = 10 ** 6

    for i in range(args.num):
        for url in urls:
            begin = time.monotonic()
            resp = requests.get(url)
            end = time.monotonic()
            t = int(resp.headers['Content-Length']) * 8 / (end - begin) / pre
            print(URL(url).host, resp.status_code, resp.reason,
                  'bandwidth={}'.format(t), file=sys.stderr)
            tmp[URL(url).host].append(t)

    thp = {URL(url).host: mean(tmp[URL(url).host]) for url in urls}

    with open(args.output, 'wt') as f:
        json.dump(thp, f)


if __name__ == '__main__':
    main()
