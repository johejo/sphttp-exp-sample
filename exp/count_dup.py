from glob import glob
from statistics import mean, stdev

from sphttp.analyze import open_pickled

YEAR = 2018


def open_logs(delay, init, dup):
    return [open_pickled(filename)
            for filename in sorted(glob('{}*delay={}*init={}*dup={}*'
                                        .format(YEAR, delay, init, dup)))]


def main():
    delays = (
        ('NORMAL', False),
        ('DIFF', False),
        ('DIFF', True),
    )

    dups = (
        'None',
        'IBRC_.',
        'NIBIB',
    )

    for delay, init in delays:
        for dup in dups:
            d = [len(s) - len(r) for s, r, _ in open_logs(delay, init, dup)]
            print(delay, init, dup, mean(d), stdev(d))


if __name__ == '__main__':
    main()
