import pandas as pd
import matplotlib.pyplot as plt


def plot_cases_hosps(d, country_name, vacc_perc=50):
    dd = d[d.location == country_name].copy()
    dd.date = pd.to_datetime(dd.date)

    hospss = (dd.groupby([pd.Grouper(key='date', freq='W')])
              .mean()
              .weekly_hosp_admissions_per_million)
    casess = (dd.groupby([pd.Grouper(key='date', freq='W')])
              .sum()
              .new_cases_per_million)

    fig, ax1 = plt.subplots(figsize=(9, 5))
    color = 'tab:blue'
    ax1.set_xlabel('date')
    ax1.set_ylabel('cases', color=color)
    ax1.plot(casess, color=color)

    ax2 = ax1.twinx()

    color = 'tab:red'
    ax2.set_ylabel('hosps', color=color)
    ax2.plot(hospss, color=color)

    vacc50 = (dd.groupby([pd.Grouper(key='date', freq='W')])
              .mean()
              .people_vaccinated_per_hundred > vacc_perc)

    xv50 = vacc50.where(vacc50 == True).first_valid_index()

    plt.axvline(x=xv50, color="grey", linestyle="--",
                label="Vacc > {perc}%".format(perc=vacc_perc))
    plt.legend()
    fig.tight_layout()

    plt.show()

def plot_hosp_rate(d, country_name, vacc_perc=50):
    dd = d[d.location == country_name].copy()
    dd.date = pd.to_datetime(dd.date)
    dd = dd[dd.date > '2021-01-01']

    hospss = (dd.groupby([pd.Grouper(key='date', freq='W')])
              .mean()
              .weekly_hosp_admissions_per_million)
    casess = (dd.groupby([pd.Grouper(key='date', freq='W')])
              .sum()
              .new_cases_per_million)

    fig, ax = plt.subplots(figsize=(9, 5))
    color = 'tab:blue'
    ax.set_xlabel('date')
    ax.set_ylabel('hosp rate', color=color)
    ax.plot(hospss/casess, color=color)

    plt.show()

    
def go(country_name):
    d = pd.read_csv("owid-covid-data.csv")
    plot_hosp_rate(d, country_name)


if __name__ == "__main__":
    go("United Kingdom")
    go("Cyprus")
