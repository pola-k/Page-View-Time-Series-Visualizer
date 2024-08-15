import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import random

register_matplotlib_converters()

df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

condition1 = df['value'] >= df['value'].quantile(0.025)
condition2 = df['value'] <= df['value'].quantile(0.975)
df = df.loc[condition1 & condition2]

fig, axis = plt.subplots()
axis.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
axis.set_xlabel("Date")
axis.set_ylabel("Page Views")
axis.plot(df.index, df['value'], color='red')
fig.savefig("line_plot.png")

df_bar = df.copy()
df_bar["Years"] = df_bar.index.year
df_bar["Months"] = df_bar.index.month_name()
df_bar = pd.DataFrame(df_bar.groupby(["Years", "Months"], sort=False)["value"].mean().round().astype(int))
df_bar = df_bar.rename(columns={"value": "Average Page Views"})
df_bar = df_bar.reset_index()
missing_data = {
        "Years": [2016, 2016, 2016, 2016],
        "Months": ['January', 'February', 'March', 'April'],
        "Average Page Views": [0, 0, 0, 0]
}

df_bar = pd.concat([pd.DataFrame(missing_data), df_bar])

# Draw bar plot
fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
ax.set_title("Daily freeCodeCamp Forum Average Page Views per Month")

chart = sns.barplot(data=df_bar, x="Years", y="Average Page Views", hue="Months", palette="tab10")
chart.set_xticklabels(chart.get_xticklabels(), rotation=90, horizontalalignment='center')

fig.savefig("bar_plot.png")

df_box = df.copy()
df_box.reset_index(inplace=True)
df_box['year'] = [d.year for d in df_box.date]
df_box['month'] = [d.strftime('%b') for d in df_box.date]

fig, ax = plt.subplots(1, 2, figsize=(10, 7))

data = []
year_list = df_box['year'].unique()
for year in year_list:
    condition3 = df_box['year'] == year
    box_df = df_box.loc[condition3, 'value']
    data.append(box_df)

bp = ax[0].boxplot(data, patch_artist=True)

def random_color():
    return (random.random(), random.random(), random.random())

# Apply random colors to each box
for patch in bp['boxes']:
    patch.set_facecolor(random_color())

ax[0].set_xticklabels(year_list)
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Page Views')
ax[0].set_title('Year-wise Box Plot(Trend)')

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

data2 = []
for month in month_list:
    condition3 = df_box['month'] == month
    box_df = df_box.loc[condition3, 'value']
    data2.append(box_df)

bp = ax[1].boxplot(data2, patch_artist=True)

for patch in bp['boxes']:
    patch.set_facecolor(random_color())

ax[1].set_xticklabels(month_list)
ax[1].set_xlabel('Month')
ax[1].set_ylabel('Page Views')
ax[1].set_title('Month-wise Box Plot(Trend)')
plt.subplots_adjust(wspace=0.4)
fig.savefig('boxplot.png')
