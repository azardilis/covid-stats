import read_tseries as r
import numpy as np
import matplotlib.pyplot as plt
from numpy import inf
from itertools import dropwhile

def plot_country(res, country, smooth_factor=7, days_trend=5, ncases_start=10):
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

    best_fit_line = np.polyfit(xs[:-(days_trend)], ys[:-(days_trend)], deg=1)

    plt.plot(xs, ys)
    plt.plot(xs, [r.calc_ln(best_fit_line, x) for x in xs], '--')
    plt.title(country)
    plt.show()

    return

def go():
    countries_to_plot = ['United Kingdom']
    res = r.read_csv_header("time_series_covid19_confirmed_global.csv")

    for country in countries_to_plot:
        plot_country(res, country)

    return


if __name__ == "__main__":
    go()
