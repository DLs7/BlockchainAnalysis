import datetime
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.dates import YearLocator, DateFormatter
import numpy as np
from pathlib import Path

def read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown):
    start_date_strp = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date_strp = datetime.datetime.strptime(end_date, '%Y%m%d')
    current_date = start_date_strp
    files = []
    #
    i = 0
    while current_date != end_date_strp:
        file = '/home/agasta/hdd/TCC/' + capitalized_name + '/blockchair_' + name + '_blocks_' + datetime.datetime.strftime(current_date, '%Y%m%d') + '.tsv.gz'
        files.append(file)
        i += 1
        current_date = start_date_strp + datetime.timedelta(days=i)
    #
    result = []
    for file in files:
        df = pd.read_csv(file, sep='\t', header=0)
        #
        df['date'] = pd.to_datetime(df['time'])
        df = df.set_index('date')
        #
        big_df2 = df.resample('D')[miner_field].value_counts()
        big_df2.name = 'blocks'
        big_df2 = big_df2.reset_index(miner_field)
        #
        big_df3 = big_df2.resample('D')['blocks'].sum()
        big_df2['percent'] = big_df2['blocks'].div(big_df3)
        result.append(big_df2)
        i += 1
    
        # print(result)
    big_df2 = pd.concat(result)
    big_df2_count = big_df2.groupby(miner_field)['blocks'].sum().sort_values(ascending=False)
    if(change_unknown):
        valuable_info = big_df2_count.axes[0][:13]
    elif(): valuable_info = big_df2_count.axes[0][:14]
    big_df2.loc[big_df2[miner_field].isin(valuable_info) == False, miner_field] = '*Outros'
    if(change_unknown): big_df2.loc[big_df2[miner_field] == "Unknown", miner_field] = '*Desconhecido'
    big_df2 = big_df2.groupby(['date', miner_field])['blocks', 'percent'].sum()

    big_df2.to_csv('dataframes/'+ name + '_' + start_date + '_' + end_date + '.csv')


def plot_coin(name, capitalized_name, start_date, end_date, miner_field, change_unknown):
    print("Started " + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')
    file_csv = Path('dataframes/' + name + '_' + start_date + '_' + end_date + '.csv')
    if file_csv.exists() == False:
        read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown)

    df = pd.read_csv('dataframes/'+ name + '_' + start_date + '_' + end_date + '.csv')
    print(df.groupby(miner_field)['blocks'].sum().sort_values(ascending=False))
    df['date'] = pd.to_datetime(df['date'])

    plot = df.pivot_table(index="date", columns=miner_field, values='percent').fillna(0).plot.area(colormap="gnuplot2_r")
    plot.set_title("% de blocos minerados por pools em " + capitalized_name, color="black")
    plot.set_ylim([0, 1])
    plot.invert_yaxis()
    plt.legend(bbox_to_anchor=(1.04,0), loc="lower left")
    plt.savefig('figs/'+ name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")
    # plt.show()
    print("Finished " + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')

def plot_gini(name, capitalized_name, start_date, end_date):
    df = pd.read_csv('dataframes/'+ name + '_' + start_date + '_' + end_date + '.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby(['date', 'guessed_miner'])['blocks'].sum()
    print(df)

def plot_upc(name, capitalized_name, start_date, end_date):
    df = pd.read_csv('dataframes/'+ name + '_' + start_date + '_' + end_date + '.csv')
    df = df.groupby(['date'])['blocks'].agg(['mean', 'std']).fillna(0)
    df['upc'] = df['std']/df['mean']
    df = df.drop(['std', 'mean'], axis=1)
    plot = df.plot()
    plot.set_title('Coeficiente de Proporção de Uniformidade do ' + capitalized_name)
    plot.set_ylim([0, None])
    plot.margins(x=0)
    # plot.xaxis.set_major_locator(YearLocator())
    # plot.xaxis.set_major_formatter(DateFormatter('%Y-%m-d'))
    plt.savefig('figs/upc/'+ name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")
    # print(df)

def main():
    plot_gini('bitcoin', 'Bitcoin', '20090109', '20220113')

    # plot_upc('bitcoin', 'Bitcoin', '20090109', '20220113')
    # plot_upc('bitcoin', 'Bitcoin', '20200101', '20220113')
    # plot_upc('bitcoin-cash', 'BitcoinCash', '20090109', '20220113')
    # plot_upc('bitcoin-cash', 'BitcoinCash', '20200101', '20220113')
    # plot_upc('dash', 'Dash', '20140119', '20220113')
    # plot_upc('dash', 'Dash', '20200101', '20220113')
    # plot_upc('ethereum', 'Ethereum', '20150730', '20220113')
    # plot_upc('ethereum', 'Ethereum', '20200101', '20220113')
    # plot_upc('litecoin', 'Litecoin', '20111012', '20220113')
    # plot_upc('litecoin', 'Litecoin', '20200101', '20220113')
    
    # plot_coin('bitcoin', 'Bitcoin', '20090109', '20220113', 'guessed_miner', True)
    # plot_coin('bitcoin', 'Bitcoin', '20200101', '20220113', 'guessed_miner', True)
    # plot_coin('bitcoin-cash', 'BitcoinCash', '20090109', '20220113', 'guessed_miner', True)
    # plot_coin('bitcoin-cash', 'BitcoinCash', '20200101', '20220113', 'guessed_miner', True)
    # plot_coin('dash', 'Dash', '20140119', '20220113', 'guessed_miner', True)
    # plot_coin('dash', 'Dash', '20200101', '20220113', 'guessed_miner', True)
    # plot_coin('ethereum', 'Ethereum', '20150730', '20220113', 'miner', False)
    # plot_coin('ethereum', 'Ethereum', '20200101', '20220113', 'miner', False)
    # plot_coin('litecoin', 'Litecoin', '20111012', '20220113', 'guessed_miner', True)
    # plot_coin('litecoin', 'Litecoin', '20200101', '20220113', 'guessed_miner', True)

if __name__ == "__main__":
    main()