from glob import glob
from statistics import mean

from matplotlib import pyplot as plt

from sphttp.analyze import (
    get_invalid_block_log, open_pickled, get_time_log, get_delay_time_log,
)


def monochrome_style_generator():
    linestyle = ['-', '--', '-.', ':']
    markerstyle = ['h', '2', 'v', '^', 's', '<', '>', '1', '3', '4', '8', 'p',
                   '*', 'H', '+', ',', '.', 'x', 'o', 'D', 'd', '|', '_']
    line_idx = 0
    marker_idx = 0
    while True:
        yield 'k' + linestyle[line_idx] + markerstyle[marker_idx]
        line_idx = (line_idx + 1) % len(linestyle)
        marker_idx = (marker_idx + 1) % len(markerstyle)


def open_pickleds(delay, init, dup):
    return [open_pickled(filename)
            for filename in sorted(glob('2018*delay={}*init={}*dup={}*'
                                        .format(delay, init, dup)))]


def main():
    h = (
        'ADT',
        'NSB',
    )

    delays = (
        ('NORMAL', False),
        ('DIFF', False),
        ('DIFF', True),
    )

    points = ('p', 'o', None)
    color = ('g', 'r', 'b')
    mfc = ('0.3', 'white', None)
    # mfc = ('white', '0.3')

    # gen = monochrome_style_generator()

    dups = (
        'None',
        'IBRC',
        'NIBIB',
    )

    figsize = (18, 9)
    plt.rcParams["font.size"] = 26

    left = -5
    right = 100

    for n in range(10):
        for dup in dups:
            for i in h:
                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(1, 1, 1)
                for (delay, init), p, c, m in zip(delays, points, color, mfc):
                    _, recv_log, _ = open_pickleds(delay, init, dup)[n]
                    if i == 'ADT':
                        log = get_delay_time_log(recv_log)
                        val = mean(log)
                        ax.set_ylabel('Delay Time [sec]')
                    elif i == 'NSB':
                        log = get_invalid_block_log(recv_log)
                        val = mean(log)
                        ax.set_ylabel('Number of Invalid Blocks')
                    else:
                        return

                    t_log = get_time_log(recv_log)
                    ax.plot(t_log, log,
                            label='{}-{}'.format(delay, init), color=c,)
                    ax.plot([0, 100], [val, val],
                            color=c, linestyle='dashed')

                    if init:
                        x = left
                    else:
                        x = right
                    ax.text(x, val, '{}'.format(round(val, 2)), color=c)

                ax.grid()
                ax.legend()
                ax.set_xlabel('Time [s]')
                fig.savefig('{}_{}_{}.pdf'.format(dup, i, n),
                            bbox_inches="tight", pad_inches=0.0)


if __name__ == '__main__':
    main()
