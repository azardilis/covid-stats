import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt


def dict_to_val(d):
    return list(d.values())[0]


def intOrNan(n):
    try:
        return int(n)
    except:
        return np.NAN


def clean(td):
    td = { dt: data for dt, data in td.items()
           if (dt.startswith("2020") or
               dt.startswith("2021") or
               dt.startswith("2022"))
          }

    return {dt.strip(): intOrNan(dict_to_val(data).strip("p "))
            for dt, data in td.items() if not dt.endswith("53 ")}


def rm_nans_dict(d):
    return {k: v for k, v in d.items() if not np.isnan(v)}


def sum_dict(d1, d2):
    d = dict()
    for k in d1.keys():
        d[k] = d1[k] + d2[k]

    return d


def yw_to_date(yw):
    yr, w = yw.split("W")

    return datetime.date.fromisocalendar(int(yr), int(w), 1)
    
    
def get_all_deaths():
    deaths = pd.read_table("demo_r_mwk_ts.tsv", sep="\t")
    deaths_cy_m = deaths[deaths["sex,unit,geo\\time"] == "M,NR,CY"].to_dict()
    deaths_cy_f = deaths[deaths["sex,unit,geo\\time"] == "F,NR,CY"].to_dict()

    deaths_cy = sum_dict(rm_nans_dict(clean(deaths_cy_m)),
                         rm_nans_dict(clean(deaths_cy_f)))

    deaths_cy = {yw_to_date(k): v for k, v in deaths_cy.items()}
    deaths_cy = pd.Series(deaths_cy)
    deaths_cy.index = pd.to_datetime(deaths_cy.index)

    return deaths_cy


def get_covid_data(country_name="Cyprus"):    
    #covid data from owid
    d = pd.read_csv("owid-covid-data.csv")
    dd = d[d.location == country_name].copy()
    dd.date = pd.to_datetime(dd.date)
    casess = dd.groupby([pd.Grouper(key="date", freq='W-MON')]).sum().new_cases
    deathss = dd.groupby([pd.Grouper(key="date", freq='W-MON')]).sum().new_deaths
    vacss = dd.groupby([pd.Grouper(key="date", freq="W-MON")]).sum().new_vaccinations

    return casess, deathss, vacss


def plot_deaths_cases(all_ds, covid_data):
    casess, deathss, vacss = covid_data
    all_ds = pd.DataFrame(all_ds.rename("all_deaths"))
    deathss = pd.DataFrame(deathss)

    dd = deathss.join(all_ds)
    non_covid_deaths = dd["all_deaths"] - dd["new_deaths"]

    
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('date')
    ax1.set_ylabel('non-covid deaths', color=color)
    ax1.plot(non_covid_deaths, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('covid cases', color=color)
    ax2.plot(casess, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.show()




