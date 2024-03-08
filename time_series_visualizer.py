import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    df.index= df['date']
    df.index = df.index.str[:-3]

    fig, ax = plt.subplots(figsize= (18, 5))

    df.plot(ax=ax, legend=None, title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019', xlabel='Date', ylabel='Page Views', color='#d62728')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()

    df_bar['months'] = df_bar['date'].str[5:7].replace({"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"})
    df_bar['date'] = df_bar['date'].str[0:4]

    # Convertir 'date' en el índice
    df_bar.set_index('date', inplace=True)
    # Pivotear la tabla y sumar los valores
    df_bar = df_bar.pivot_table(index='date', columns='months', values='value', aggfunc='sum')

    df_bar = df_bar[['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']]

    # Draw bar plot
    fig, ax = plt.subplots(figsize= (18, 5))

    df_bar.plot(ax=ax, kind='bar', legend='Months', xlabel='Years', ylabel='Average Page Views')

    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box['date'] = pd.to_datetime(df_box['date']) 
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    ord = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=ord, ordered=True)

    fig, ax = plt.subplots(figsize=(18, 6), nrows=1, ncols=2)
    sns.boxplot(data=df_box, x="year", y="value",ax=ax[0])
    sns.boxplot(data=df_box, x="month", y="value",ax=ax[1])



    for axes in ax:
        axes.set_ylim(0, 200000)  # Especificar el rango de valores en y
        axes.set_yticks(range(0, 200001, 20000))  # Especificar los intervalos en y

    # Ajustes de etiquetas y título
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title('Year-wise Box Plot (Trend)')

    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')

    plt.tight_layout()

    fig.savefig('box_plot.png')
    return fig
