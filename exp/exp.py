#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import pickle
import gc

from tqdm import tqdm

from sphttp import Downloader, DelayRequestAlgorithm, DuplicateRequestAlgorithm

tqdm.monitor_interval = 0


def main():
    urls = [
        'http://ftp.jaist.ac.jp/pub/Linux/ubuntu-releases/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://ubuntutym2.u-toyama.ac.jp/ubuntu/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://releases.ubuntu.com/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://mirrorservice.org/sites/releases.ubuntu.com/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://ubuntu.ipacct.com/releases/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://mirror.pop-sc.rnp.br/mirror/ubuntu-releases/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://ftp.belnet.be/ubuntu.com/ubuntu/releases/artful/ubuntu-17.10.1-server-amd64.iso',
        'http://mirrors.mit.edu/ubuntu-releases/artful/ubuntu-17.10.1-server-amd64.iso',
    ]

    dup = [
        (False, None),
        (True, DuplicateRequestAlgorithm.IBRC),
        (True, DuplicateRequestAlgorithm.NIBIB),
    ]

    delay_algo = [
        (DelayRequestAlgorithm.NORMAL, False),
        (DelayRequestAlgorithm.DIFF, False),
        (DelayRequestAlgorithm.DIFF, True),
    ]

    n = 10
    threshold = 20

    bar = tqdm(total=n * len(delay_algo) * len(dup), desc='Total')
    for i in range(n):
        for dr, du in dup:
            for delay, init in delay_algo:
                dl = Downloader(urls, enable_trace_log=True,
                                enable_dup_req=dr, dup_req_algo=du,
                                invalid_block_threshold=threshold,
                                delay_req_algo=delay, enable_init_delay=init)

                dlbar = tqdm(total=dl.length, leave=False, desc='Download')

                for p in dl:
                    dlbar.update(len(p))

                dlbar.close()

                if du is None:
                    dupname = None
                else:
                    dupname = du.name

                end = '_delay={}_init={}_dup={}_'.format(delay.name, init,
                                                         dupname) + '.pickle'
                filename = datetime.now().isoformat() + end

                with open(filename, 'wb') as f:
                    pickle.dump(dl.get_trace_log(), f)

                bar.update()
                gc.collect()


if __name__ == '__main__':
    main()
