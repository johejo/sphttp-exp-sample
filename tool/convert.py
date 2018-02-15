#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Convert pickle style log to text style.
# python3 is required.
# Please see the script's help for detailed usage.
# $ python convert.py -h

import pickle
import argparse
import sys
from urllib.parse import urlparse


def set_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', nargs=None,
                        help='log file path (python pickle)')
    parser.add_argument('-s', '--send', action='store_true',
                        help='print send log')
    parser.add_argument('-r', '--recv', action='store_true',
                        help='print recv log')
    parser.add_argument('-d', '--delay', action='store_true',
                        help='print delay sec of init HEAD request')
    parser.add_argument('-o', '--out',
                        help='output file (The default output is stdout.)')

    return parser.parse_args()


def log_write(file, log, out):
    for t, block_id, host in log:
        line = '{} {} {}'.format(t, block_id, host)
        if out:
            file.write(line + '\n')
        else:
            print(line)


def delay_write(file, delay, out):
    for url, delay in delay.items():
        line = '{} {}'.format(urlparse(url).hostname, delay)
        if out:
            file.write(line + '\n')
        else:
            print(line)


def main():
    args = set_args()

    with open(args.file, 'rb') as f:
        send_log, recv_log, init_delay = pickle.load(f)

    if args.out:
        f = open(args.out, 'wt')

    if args.send:
        log_write(f, send_log, args.out)

    elif args.recv:
        log_write(f, recv_log, args.out)

    elif args.delay:
        delay_write(f, init_delay, args.out)

    else:
        sys.stderr.write('Nothing to print.\n')

    if args.out:
        f.close()


if __name__ == '__main__':
    main()
