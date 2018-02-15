from glob import glob
from statistics import mean, stdev

from matplotlib import pyplot as plt

from sphttp.analyze import (
    open_pickled,
    calc_med_posi_delay_time,
    calc_mean_posi_delay_time, calc_mean_num_invalid_block,
    calc_init_buffering_time, calc_mean_ret_evt_interval,
)

YEAR = 2018


def plot_bar(xdata, ydata, yerr, ylabel, title, hatches, colors):
    # fig = plt.figure(figsize=(20, 10))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bars = ax.bar(xdata, ydata, yerr=yerr, color=colors, edgecolor='black')
    # for bar, hatch in zip(bars, hatches):
    #     bar.set_hatch(hatch)
    ax.set_xlabel('Algorithms')
    ax.set_ylabel(ylabel)
    plt.title(title)
    fig.savefig(title.replace(' ', '') + 'Pub.pdf', bbox_inches="tight",
                pad_inches=0.0)


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
        # 'None',
        'IBRC',
        # 'NIBIB',
    )

    hatches = (
        "/",
        # ".",
        "o",
        "x",
    )

    colors = (
        # '0.5',
        # '1',
        # '0.9',
        # '0.7',
        'cyan',
        'green',
        'yellow',
    )

    adts = []
    ibts = []

    adtdev = []
    ibtdev = []

    nsbs = []
    nsbdev = []

    rei = []
    reidev = []

    for delay, init in delays:
        for dup in dups:
            adts_t = []
            nsbs_t = []
            ibts_t = []
            rei_t = []
            for send_log, recv_log, init_log in open_logs(delay, init, dup):
                adts_t.append(calc_mean_posi_delay_time(recv_log))
                nsbs_t.append(calc_mean_num_invalid_block(recv_log))
                ibts_t.append(calc_init_buffering_time(recv_log))
                rei_t.append(calc_mean_ret_evt_interval(recv_log))

            adts.append(mean(adts_t))
            adtdev.append(stdev(adts_t))
            nsbs.append(mean(nsbs_t))
            nsbdev.append(stdev(nsbs_t))
            ibts.append(mean(ibts_t))
            ibtdev.append(stdev(ibts_t))
            rei.append(mean(rei_t))
            reidev.append(stdev(rei_t))

    padt = (adts, adtdev, 'Average Delay Time [sec]',
            'Average Delay Time')
    pibt = (ibts, ibtdev, 'Initial Buffering Time [sec]',
            'Initial Buffering Time')
    pnsb = (nsbs, nsbdev, 'Number of Blocks Staying in Buffer',
            'Number of Blocks Staying in Buffer')
    prei = (rei, reidev, 'Block Return Interval [sec]',
            'Block Return Interval')

    x = [algo + '-' + str(b) if algo == 'DIFF' else algo
         for algo, b in delays for dup in dups]
    # x = [algo + '-' + str(b) + '-' + dup
    #      for algo, b in delays for dup in dups]

    for p, yerr, ylabel, title in (padt, pibt, pnsb, prei):
        plot_bar(x, p, yerr, ylabel, title, hatches, colors)


if __name__ == '__main__':
    main()
