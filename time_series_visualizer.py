import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df[
    (df.value >= df.value.quantile(0.025)) &
    (df.value <= df.value.quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    df.plot(figsize=(32,10), color='red', legend=False, ax=ax, rot=0);
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_bar = df_bar.groupby(['year', 'month'], sort=False).mean().round().astype(int).reset_index()

    data_missing = {
        "year": [2016, 2016, 2016, 2016],
        "month": ['January', 'February', 'March', 'April'],
        "value": [0, 0, 0, 0]
    }

    df_bar = pd.concat([pd.DataFrame(data_missing), df_bar])

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=df_bar, x='year', legend=False, y='value', hue='month', ax=ax, palette='tab10')
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(months, title='Months')
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,8))
    flierprops = {'marker': 'd', 'markersize': 2, 'markerfacecolor':'black'}
    kwargs = {'data': df_box, 'legend': False, 'palette': 'tab10', 'flierprops': flierprops}
    order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    sns.boxplot(x='year', hue='year', y='value', ax=ax1, **kwargs)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_ylabel('Page Views')
    ax1.set_xlabel('Year')

    sns.boxplot(x='month', hue='month', y='value', order=order, ax=ax2, **kwargs)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_ylabel('Page Views')
    ax2.set_xlabel('Month')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig