import datetime
from math import trunc
from tracemalloc import start
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.dates import YearLocator, DateFormatter
import numpy as np
import random
import inequality
from pathlib import Path

def read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown, full, foundry_digital):
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
        if foundry_digital == True:
            foundry_digital_substring = "466f756e6472792055534120506f6f6c202364726f70676f6c64"
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(foundry_digital_substring), miner_field] = "FoundryDigital"
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
    if full == False:
        valuable_info = big_df2_count.axes[0][:14]
        if(change_unknown):
            valuable_info = big_df2_count.axes[0][:13]
        big_df2.loc[big_df2[miner_field].isin(valuable_info) == False, miner_field] = '*Outros'
    if(change_unknown): big_df2.loc[big_df2[miner_field] == "Unknown", miner_field] = '*Desconhecido'
    big_df2 = big_df2.groupby(['date', miner_field])['blocks', 'percent'].sum()

    if full: big_df2.to_csv('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    elif(full == False): big_df2.to_csv('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')


def plot_coin(name, capitalized_name, start_date, end_date, miner_field, change_unknown, foundry_digital):
    print("Started " + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')
    file_csv = Path('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')
    if file_csv.exists() == False:
        read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown, False, foundry_digital)

    df = pd.read_csv('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')
    print(df.groupby(miner_field)['blocks'].sum().sort_values(ascending=False))
    df['date'] = pd.to_datetime(df['date'])
    df[miner_field] = df[miner_field].apply(lambda x: truncate(x))

    plot = df.pivot_table(index="date", columns=miner_field, values='percent').fillna(0).plot.area(colormap="turbo")
    plot.set_title("% de blocos minerados por pools em " + capitalized_name, color="black")
    plot.set_ylim([0, 1])
    plot.invert_yaxis()
    plt.legend(bbox_to_anchor=(1.04,0), loc="lower left")
    plt.savefig('figs/distribution/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")
    # plt.show()
    print("Finished " + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')

def truncate(index):
    if len(index) >= 20:
        index = index[:17] + '...'
    return index

def plot_pie(name, capitalized_name, start_date, end_date, miner_field):
    df = pd.read_csv('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')
    df = df.groupby(miner_field)['blocks'].sum().sort_values(ascending=False)

    plot = df.plot.pie(y='blocks', colormap="turbo", labels=None)
    plot.set_title("Total de blocos minerados por pools em " + capitalized_name, color="black")
    index = df.index.map(truncate)
    plt.legend(bbox_to_anchor=(1.04,0), loc="lower left", labels=index)
    plt.savefig('figs/pie/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")
    plt.close()
    plt.figure().clear()

def gini_by_col(column):
    return inequality.gini.Gini(column.values).g

def plot_gini(name, capitalized_name, start_date, end_date, miner_field, change_unknown):
    print("Started " + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')
    file_csv = Path('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    if file_csv.exists() == False:
        read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown, True)
    df = pd.read_csv('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    print(df)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m')
    df = df.reset_index().pivot_table(index=miner_field, columns='date', values='blocks').fillna(0)
    # with pd.option_context('display.max_rows', None):  # more options can be specified also
    #     print(df)

    inequalities = df[list(df.columns.values)].apply(gini_by_col, axis=0).to_frame('Gini')
    plot = inequalities.plot(figsize=(10, 3));
    plot.set_title('Coeficiente de Gini de ' + capitalized_name)
    plot.margins(x=0)
    plt.savefig('figs/gini/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")

def theil_by_column(column):
    return inequality.theil.Theil(column.values).T

def plot_theil(name, capitalized_name, start_date, end_date, miner_field, change_unknown):
    df = pd.read_csv('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    print(df)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m')
    df = df.reset_index().pivot_table(index=miner_field, columns='date', values='blocks').fillna(0)
    # with pd.option_context('display.max_rows', None):  # more options can be specified also
    #     print(df)

    inequalities = df[list(df.columns.values)].apply(theil_by_column, axis=0).to_frame('Theil')
    plot = inequalities.plot(figsize=(10, 3));
    plot.set_title('Coeficiente de Theil de ' + capitalized_name)
    plot.margins(x=0)
    plt.savefig('figs/theil/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")

def nakamoto(arr, count_df):
    index = 0
    sum = 0
    for num in arr:
        sum += num
        index += 1
        if sum >= count_df/2:
            return index

def plot_nakamoto(names, capitalized_names, start_date, end_date, miner_fields):
    i = 0
    index = []
    while i < len(names):
        df = pd.read_csv('dataframes/full/' + names[i] + '_' + start_date + '_' + end_date + '.csv')
        df = df.groupby([miner_fields[i]])['blocks'].sum().sort_values(ascending=False)
        count_df = df.sum()
        if(names[i] != 'ethereum'):
            df.drop(['*Desconhecido'], inplace=True)
        index.append(nakamoto(df.to_numpy(), count_df))
        i += 1
    plt.bar(capitalized_names, index)
    plt.show()

def std(x): return np.std(x)
def mean(x): return np.mean(x)

def plot_upc(name, capitalized_name, start_date, end_date):
    df = pd.read_csv('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    df = df.groupby(['date'])['blocks'].agg([mean, std])
    df['upc'] = df['std']/df['mean']
    df = df.drop(['std', 'mean'], axis=1)
    plot = df.plot()
    plot.set_title('Coeficiente de Proporção de Uniformidade do ' + capitalized_name)
    plot.set_ylim([0, None])
    plot.margins(x=0)
    # plot.xaxis.set_major_locator(YearLocator())
    # plot.xaxis.set_major_formatter(DateFormatter('%Y-%m-d'))
    plt.savefig('figs/upc/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches="tight")
    # print(df)

def main():
    # names = ['bitcoin', 'bitcoin-cash', 'dash', 'ethereum', 'litecoin']
    # capitalized_names = ['Bitcoin', 'BitcoinCash', 'Dash', 'Ethereum', 'Litecoin']
    # start_date='20200101'
    # end_date='20211231'
    # miner_fields = ['guessed_miner', 'guessed_miner', 'guessed_miner', 'miner', 'guessed_miner']
    # plot_nakamoto(names, capitalized_names, start_date, end_date, miner_fields)

    # plot_coin('bitcoin', 'Bitcoin', '20090109', '20211231', 'guessed_miner', True, True)
    # plot_coin('bitcoin', 'Bitcoin', '20200101', '20211231', 'guessed_miner', True, True)
    # plot_coin('bitcoin-cash', 'BitcoinCash', '20170801', '20211231', 'guessed_miner', True, True)
    # plot_coin('bitcoin-cash', 'BitcoinCash', '20200101', '20211231', 'guessed_miner', True, True)
    # plot_coin('dash', 'Dash', '20140119', '20211231', 'guessed_miner', True, False)
    # plot_coin('dash', 'Dash', '20200101', '20211231', 'guessed_miner', True, False)
    # plot_coin('ethereum', 'Ethereum', '20150730', '20211231', 'miner', False, False)
    # plot_coin('ethereum', 'Ethereum', '20200101', '20211231', 'miner', False, False)
    # plot_coin('litecoin', 'Litecoin', '20111012', '20211231', 'guessed_miner', True, False)
    # plot_coin('litecoin', 'Litecoin', '20200101', '20211231', 'guessed_miner', True, False)

    # plot_gini('bitcoin', 'Bitcoin', '20090109', '20211231', 'guessed_miner', True)
    # plot_gini('bitcoin', 'Bitcoin', '20200101', '20211231', 'guessed_miner', True)
    # plot_gini('bitcoin-cash', 'BitcoinCash', '20170801', '20211231', 'guessed_miner', True)
    # plot_gini('bitcoin-cash', 'BitcoinCash', '20200101', '20211231', 'guessed_miner', True)
    # plot_gini('dash', 'Dash', '20140119', '20211231', 'guessed_miner', True)
    # plot_gini('dash', 'Dash', '20200101', '20211231', 'guessed_miner', True)
    # plot_gini('ethereum', 'Ethereum', '20150730', '20211231', 'miner', False)
    # plot_gini('ethereum', 'Ethereum', '20200101', '20211231', 'miner', False)
    # plot_gini('litecoin', 'Litecoin', '20111012', '20211231', 'guessed_miner', True)
    # plot_gini('litecoin', 'Litecoin', '20200101', '20211231', 'guessed_miner', True)

    plot_theil('bitcoin', 'Bitcoin', '20090109', '20211231', 'guessed_miner', True)
    plot_theil('bitcoin', 'Bitcoin', '20200101', '20211231', 'guessed_miner', True)
    plot_theil('bitcoin-cash', 'BitcoinCash', '20170801', '20211231', 'guessed_miner', True)
    plot_theil('bitcoin-cash', 'BitcoinCash', '20200101', '20211231', 'guessed_miner', True)
    plot_theil('dash', 'Dash', '20140119', '20211231', 'guessed_miner', True)
    plot_theil('dash', 'Dash', '20200101', '20211231', 'guessed_miner', True)
    plot_theil('ethereum', 'Ethereum', '20150730', '20211231', 'miner', False)
    plot_theil('ethereum', 'Ethereum', '20200101', '20211231', 'miner', False)
    plot_theil('litecoin', 'Litecoin', '20111012', '20211231', 'guessed_miner', True)
    plot_theil('litecoin', 'Litecoin', '20200101', '20211231', 'guessed_miner', True)

    # plot_pie('bitcoin', 'Bitcoin', '20090109', '20211231', 'guessed_miner')
    # plot_pie('bitcoin', 'Bitcoin', '20200101', '20211231', 'guessed_miner')
    # plot_pie('bitcoin-cash', 'BitcoinCash', '20170801', '20211231', 'guessed_miner')
    # plot_pie('bitcoin-cash', 'BitcoinCash', '20200101', '20211231', 'guessed_miner')
    # plot_pie('dash', 'Dash', '20140119', '20211231', 'guessed_miner')
    # plot_pie('dash', 'Dash', '20200101', '20211231', 'guessed_miner')
    # plot_pie('ethereum', 'Ethereum', '20150730', '20211231', 'miner')
    # plot_pie('ethereum', 'Ethereum', '20200101', '20211231', 'miner')
    # plot_pie('litecoin', 'Litecoin', '20111012', '20211231', 'guessed_miner')
    # plot_pie('litecoin', 'Litecoin', '20200101', '20211231', 'guessed_miner')

    # plot_upc('bitcoin', 'Bitcoin', '20090109', '20211231')
    # plot_upc('bitcoin', 'Bitcoin', '20200101', '20211231')
    # plot_upc('bitcoin-cash', 'BitcoinCash', '20170801', '20211231')
    # plot_upc('bitcoin-cash', 'BitcoinCash', '20200101', '20211231')
    # plot_upc('dash', 'Dash', '20140119', '20211231')
    # plot_upc('dash', 'Dash', '20200101', '20211231')
    # plot_upc('ethereum', 'Ethereum', '20150730', '20211231')
    # plot_upc('ethereum', 'Ethereum', '20200101', '20211231')
    # plot_upc('litecoin', 'Litecoin', '20111012', '20211231')
    # plot_upc('litecoin', 'Litecoin', '20200101', '20211231')

if __name__ == "__main__":
    main()