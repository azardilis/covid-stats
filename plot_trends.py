import read_tseries as r
import numpy as np
import matplotlib.pyplot as plt
from numpy import inf
from itertools import dropwhile
import matplotlib as mpl


def shorter_name(country):
    if country == 'United Kingdom': return 'UK'
    else: return country


def population(country):
    if country == 'United Kingdom': return 66650000
    elif country == 'Cyprus': return 875899
    elif country == 'Greece': return 10720000
    elif country == 'Israel': return 9053000
    elif country == 'Sweden': return 10230000
    elif country == 'US': return 328200000
    elif country == 'Turkey': return 82000000
    elif country == 'Germany': return 83000000
    elif country == 'France': return 67060000
    elif country == 'Spain': return 46940000
    elif country == 'Italy': return 60360000
    else: return None

def plot_country(res, country, lim=13, smooth_factor=7, days_trend=7, ncases_start=50, ax=None):
    res_uk = np.array(list(dropwhile(lambda n: n < ncases_start,
                                     r.get_max(r.get_a(res, country),
                                               lambda x: sum(x)))))

    res_uk_log = np.log(r.running_mean(res_uk, smooth_factor))
    res_uk_log[res_uk_log == -inf] = 0

    ds = r.running_mean(np.array(r.get_ds(res_uk)), smooth_factor)
    ds_log = np.log(ds)
    ds_log[ds_log == -inf] = 0

    xs = res_uk_log[1:]
    ys = ds_log

    if population(country):
        rate = (np.sum(ds[-days_trend:]) / population(country) * 100000)
    else:
        rate = 0.0

    best_fit_line = np.polyfit(xs[-(4*days_trend):], ys[-(4*days_trend):], deg=1)

    sign = ""
    if r.calc_ln(best_fit_line, xs[-1]) < ys[-1]: sign = "up"
    else: sign = "down"

    dy = np.gradient(ys)

    trend_xs = xs[-(24 * days_trend):]

    ax.plot(xs, ys)
    ax.plot(trend_xs, [r.calc_ln(best_fit_line, x) for x in trend_xs],
            '--')
    ax.set_title("{nm} ({coeff:.2f}, {dy:.2f}, r={rate:.2f})".format(nm=shorter_name(country),
                                                                     coeff=best_fit_line[0],
                                                                     rate=rate,
                                                                     dy=np.mean(dy[-days_trend:])),
                 fontsize=9)
    ax.text(2.5, lim-(lim/10), sign, fontsize=10)
    ax.set_xlabel("log(total)", fontsize=9)
    ax.set_ylabel("log(new)", fontsize=9)
    ax.set_xlim(0, 17)
    ax.set_ylim(0, lim)
    

    return

def go(countries_to_plot, tag="", lim=15, smooth_factor=7):
    res = r.read_csv_header("time_series_covid19_confirmed_global.csv")

    ncountries = len(countries_to_plot)

    ncols = 3
    nrows = (ncountries // 3) + 1

    if ncountries < 3:
        ncols = ncountries
        nrows = 1

    fig = plt.figure()

    mpl.rcParams['xtick.labelsize'] = 8
    mpl.rcParams['ytick.labelsize'] = 8

    for i, country in enumerate(countries_to_plot):
        ax = plt.subplot(nrows, ncols, i+1)
        plot_country(res, country, ax=ax, lim=lim, smooth_factor=smooth_factor)

    plt.tight_layout()
    plt.savefig("current_trends_{tag}.png".format(tag=tag), dpi=300)
    plt.show()
    
    return


if __name__ == "__main__":
    countries_to_plot = ['United Kingdom',
                         'Italy',
                         'Spain',
                         'France',
                         'Germany',
                         'Sweden',
                         'US',
                         'Turkey',
                         'Israel']
    go(countries_to_plot)
    go(["Cyprus", "Greece"], tag="CypGre", lim=10, smooth_factor=7)
