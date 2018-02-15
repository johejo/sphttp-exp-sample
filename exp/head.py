import glob

from matplotlib import pyplot as plt
from yarl import URL

from sphttp.analyze import open_pickled, get_mean_block_arr_interval


def open_logs(delay, init, dup):
    return [open_pickled(filename)
            for filename in sorted(glob.glob('2018*delay={}*init={}*dup={}*'
                                             .format(delay, init, dup)))]


def get_ave_interval(delay, init, dup):

    x = []
    y = []

    for s, r, d in open_logs(delay, init, dup):
        c = get_mean_block_arr_interval(s, r)
        for dk, dv in d.items():
            x.append(dv)
            y.append(c[URL(dk).host])

    return x, y


def plot(delay, init, dup):
    rd, itv = get_ave_interval(delay, init, dup)
    plt.plot(rd, itv, '.')


def main():
    delays = [
        ('NORMAL', False),
        ('DIFF', False),
        ('DIFF', True),
    ]

    dups = [
        'NIBIB',
    ]

    plt.figure()

    for delay, init in delays:
        for dup in dups:
            plot(delay, init, dup)
    plt.plot([0, 0.6], [0, 6])
    plt.grid(which='major')

    plt.xlabel('Response Time of HEAD-Request [s]')
    plt.ylabel('Average Block Arrival Interval [s]')
    plt.savefig('head_itv.pdf')


if __name__ == '__main__':
    main()
