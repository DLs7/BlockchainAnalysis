import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import inequality
from pathlib import Path

def read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown, full, add_missing):
    eth_dict = {
        '0xea674fdde714fd979de3edf0f56aa9716b898ec8': 'Ethermine',
        '0x829bd824b016326a401d083b33d092293333a830': 'F2Pool',
        '0x1ad91ee08f21be3de0ba2ba6918e714da6b45836': 'Hiveon',
        '0x2a20380dca5bc24d052acfbf79ba23e988ad0050': 'Poolin',
        '0x7f101fe45e6649a6fb8f3f8b43ed03d353f2b90c': 'Flexpool',
        '0x00192fb10df37c9fb26829eb2cc623cd1bf599e8': '2MinersPool',
        '0x45a36a8e118c37e4c47ef4ab827a7c9e579e11e2': 'Antpool',
        '0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5': 'Nanopool',
        '0x3ecef08d0e2dad803847e052249bb4f8bff2d5bb': 'MiningPoolHub',
        '0xc365c3315cf926351ccaf13fa7d19c8c4058c8e1': 'Binance',
        '0xeea5b82b61424df8020f5fedd81767f2d0d25bfb': 'BTC.com',
        '0xc3348b43d3881151224b490e4aa39e03d2b1cdea': 'Ezilpool',
        '0x03e75d7dd38cce2e20ffee35ec914c57780a8e29': 'GPUMINEPool',
        '0x4069e799da927c06b430e247b2ee16c03e8b837d': '666MiningPool',
        '0xd757fd54b273bb1234d4d9993f27699d28d0edd2': 'KuCoin',
        '0x433022c4066558e7a32d850f02d2da5ca782174d': 'K1POOL.COM',
        '0x002e08000acbbae2155fab7ac01929564949070d': '2MinersSolo',
        '0x1ca43b645886c98d7eb7d27ec16ea59f509cbe1a': 'ViaBTC',
        '0x249bdb4499bd7c683664c149276c1d86108e2137': 'Cruxpool',
        '0x99c85bb64564d9ef9a99621301f22c9993cb89e3': 'BeePool',
        '0x5a0b54d5dc17e0aadc383d2db43b0a0d3e029c4c': 'SparkPool'
    }
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
        if add_missing == True:
            foundry_digital_substring = '466f756e64727920555341'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(foundry_digital_substring), miner_field] = 'FoundryDigital'

            okex_substring = '7777772e6f6b65782e636f6d'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(okex_substring), miner_field] = 'OKEX'

            via_btc_substring = '566961425443'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(via_btc_substring), miner_field] = 'ViaBTC'

            sbi_crypto_substring = '53424943727970746f2e636f6d'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(sbi_crypto_substring), miner_field] = 'SBIcrypto'

            poolin_substring = '706f6f6c696e2e636f6d'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(poolin_substring), miner_field] = 'Poolin'

            pro_hashing_substring = '70726f68617368696e672e636f6d'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(pro_hashing_substring), miner_field] = 'ProHashing'

            hash_city_substring = '68617368636974792e6f7267'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(hash_city_substring), miner_field] = 'HashCity'

            luxor_substring = '4c55584f52'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(luxor_substring), miner_field] = 'Luxor'

            xn_pool_substring = '4d696e696e67436f7265'
            df['coinbase_data_hex'] = df['coinbase_data_hex'].astype(str)
            df.loc[df['coinbase_data_hex'].str.contains(luxor_substring), miner_field] = 'xnpool'

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
    if(name == 'ethereum'):
            big_df2 = big_df2.replace({miner_field: eth_dict})
    print(big_df2)
    big_df2_count = big_df2.groupby(miner_field)['blocks'].sum().sort_values(ascending=False)
    if full == False:
        valuable_info = big_df2_count.axes[0][:14]
        if(change_unknown):
            valuable_info = big_df2_count.axes[0][:13]
        big_df2.loc[big_df2[miner_field].isin(valuable_info) == False, miner_field] = '*Outros'
    if(change_unknown): big_df2.loc[big_df2[miner_field] == 'Unknown', miner_field] = '*Desconhecido'
    big_df2 = big_df2.groupby(['date', miner_field])[['blocks', 'percent']].sum()

    if full: big_df2.to_csv('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    elif(full == False): big_df2.to_csv('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')


def plot_coin(name, capitalized_name, start_date, end_date, miner_field, change_unknown, add_missing):
    print('Started ' + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')
    file_csv_parsed = Path('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')
    if file_csv_parsed.exists() == False:
        read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown, False, add_missing)

    file_csv_full = Path('dataframes/full/' + name + '_' + start_date + '_' + end_date + '.csv')
    if file_csv_full.exists() == False:
        read_data(name, capitalized_name, start_date, end_date, miner_field, change_unknown, True, add_missing)

    df = pd.read_csv('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')
    # print(df.groupby(miner_field)['blocks'].sum().sort_values(ascending=False))
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m')
    df[miner_field] = df[miner_field].apply(lambda x: truncate(x))

    plot = df.pivot_table(index='date', columns=miner_field, values='percent').fillna(0).plot.area(colormap='turbo')
    plot.set_title('% de blocos minerados por pools em ' + capitalized_name, color='black')
    plot.set_ylim([0, 1])
    plot.invert_yaxis()
    plt.margins(x=0)
    plt.legend(bbox_to_anchor=(1.04,0), loc='lower left')
    plt.savefig('figs/distribution/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches='tight')
    # plt.show()
    print('Finished ' + capitalized_name + ' (' + start_date + ' -> ' + end_date + ')')

def truncate(index):
    if len(index) >= 20:
        index = index[:17] + '...'
    return index

def plot_pie(name, capitalized_name, start_date, end_date, miner_field):
    df = pd.read_csv('dataframes/parsed/' + name + '_' + start_date + '_' + end_date + '.csv')
    df = df.groupby(miner_field)['blocks'].sum().sort_values(ascending=False)

    plot = df.plot.pie(y='blocks', colormap='turbo', labels=None)
    plot.set_title('Total de blocos minerados por pools em ' + capitalized_name, color='black')
    index = df.index.map(truncate)
    plt.legend(bbox_to_anchor=(1.04,0), loc='lower left', labels=index)
    plt.savefig('figs/pie/' + name + '_' + start_date + '_' + end_date + '.png', bbox_inches='tight')
    plt.close()
    plt.figure().clear()

def gini_by_column(column):
    return inequality.gini.Gini(column.values).g

def plot_gini(names, capitalized_names, start_date, end_date, miner_fields):
    eth_array = [ 'Ethermine','F2Pool', 'Hiveon', 'Poolin', 'Flexpool', '2MinersPool',
     'Antpool', 'Nanopool', 'Binance', 'BTC.com', 'Ezilpool', 'GPUMINEPool', '666MiningPool',
      'KuCoin', 'K1POOL.COM', '2MinersSolo', 'ViaBTC', 'Cruxpool', 'BeePool', 'SparkPool']
    
    i = 0
    result = []
    while i < len(names):
        df = pd.read_csv('dataframes/full/' + names[i] + '_' + start_date + '_' + end_date + '.csv')
        df = df[df[miner_fields[i]] != '*Desconhecido']
        if names[i] == 'ethereum':
            df = df[df[miner_fields[i]].isin(eth_array) == True]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m')
        df = df.reset_index().pivot_table(index=miner_fields[i], columns='date', values='blocks', aggfunc='sum').fillna(0)

        result.append(df[list(df.columns.values)].apply(gini_by_column, axis=0).to_frame(capitalized_names[i]))
        i += 1
    result2 = pd.concat(result, axis=1)
    plot = result2.plot();
    plot.set_title('Coeficiente de Gini')
    plot.margins(x=0)
    plt.legend(bbox_to_anchor=(1.04,0), loc='lower left')
    plt.savefig('figs/gini/' + start_date + '_' + end_date + '.png', bbox_inches='tight')

def theil_by_column(column):
    return inequality.theil.Theil(column.values).T

def plot_theil(names, capitalized_names, start_date, end_date, miner_fields):
    eth_array = [ 'Ethermine','F2Pool', 'Hiveon', 'Poolin', 'Flexpool', '2MinersPool',
     'Antpool', 'Nanopool', 'Binance', 'BTC.com', 'Ezilpool', 'GPUMINEPool', '666MiningPool',
      'KuCoin', 'K1POOL.COM', '2MinersSolo', 'ViaBTC', 'Cruxpool', 'BeePool', 'SparkPool']

    i = 0
    result = []
    while i < len(names):
        df = pd.read_csv('dataframes/full/' + names[i] + '_' + start_date + '_' + end_date + '.csv')
        df = df[df[miner_fields[i]] != '*Desconhecido']
        if names[i] == 'ethereum':
            df = df[df[miner_fields[i]].isin(eth_array) == True]
            # with pd.option_context('display.max_columns', None):  # more options can be specified also
            #     print(df)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m')
        df = df.reset_index().pivot_table(index=miner_fields[i], columns='date', values='blocks', aggfunc='sum').fillna(0)
        result.append(df[list(df.columns.values)].apply(theil_by_column, axis=0).to_frame(capitalized_names[i]))
        i += 1
    result2 = pd.concat(result, axis=1)
    plot = result2.plot()
    plot.set_title('Coeficiente de Theil')
    plot.margins(x=0)
    plt.legend(bbox_to_anchor=(1.04,0), loc='lower left')
    plt.savefig('figs/theil/' + start_date + '_' + end_date + '.png', bbox_inches='tight')

def nakamoto_by_column(column):
    blocks_array = column.sort_values(ascending=False).to_numpy()
    blocks = blocks_array.sum()/2
    print(column.sort_values(ascending=False))
    print(blocks)
    # print(blocks_array)
    # print(blocks)
    sum = 0
    result = 0
    for block in blocks_array:
        result += 1
        sum = sum + block
        print('> ' + str(block))
        print('- ' + str(result))
        if(sum >= blocks):
            print('>> ' + str(sum))
            print('-- ' + str(result))
            return result

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
    plt.savefig('figs/nakamoto/' + start_date + '_' + end_date + '.png', bbox_inches="tight")

def std(x): return np.std(x)
def mean(x): return np.mean(x)

def plot_upc(names, capitalized_names, start_date, end_date, miner_fields):
    eth_array = [ 'Ethermine','F2Pool', 'Hiveon', 'Poolin', 'Flexpool', '2MinersPool',
     'Antpool', 'Nanopool', 'Binance', 'BTC.com', 'Ezilpool', 'GPUMINEPool', '666MiningPool',
      'KuCoin', 'K1POOL.COM', '2MinersSolo', 'ViaBTC', 'Cruxpool', 'BeePool', 'SparkPool']
    
    i = 0
    result = []
    while(i < len(names)):
        df = pd.read_csv('dataframes/full/' + names[i] + '_' + start_date + '_' + end_date + '.csv')
        df = df[df[miner_fields[i]] != '*Desconhecido']
        if names[i] == 'ethereum':
            df = df[df[miner_fields[i]].isin(eth_array) == True]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m')
        # print(df)
        df = df.groupby(['date'])['blocks'].agg([mean, std])
        df[capitalized_names[i]] = df['std']/df['mean']
        result.append(df.drop(['std', 'mean'], axis=1))
        i += 1
    result2 = pd.concat(result, axis=1)
    # print(result2)
    plot = result2.plot()
    plot.set_title('Coeficiente de Proporção de Uniformidade')
    # plot.set_ylim([0.4, None])
    plot.margins(x=0)
    plt.legend(bbox_to_anchor=(1.04,0), loc='lower left')
    plt.savefig('figs/upc/' + start_date + '_' + end_date + '.png', bbox_inches='tight')
    # print(df)

def main():
    names = ['bitcoin', 'bitcoin-cash', 'dash', 'ethereum', 'litecoin']
    capitalized_names = ['Bitcoin', 'BitcoinCash', 'Dash', 'Ethereum', 'Litecoin']
    start_date='20200101'
    end_date='20211231'
    miner_fields = ['guessed_miner', 'guessed_miner', 'guessed_miner', 'miner', 'guessed_miner']

    # plot_coin('dash', 'Dash', '20200101', '20211231', 'guessed_miner', True, True)
    # plot_coin('bitcoin', 'Bitcoin', '20200101', '20211231', 'guessed_miner', True, True)
    # plot_coin('bitcoin-cash', 'BitcoinCash', '20200101', '20211231', 'guessed_miner', True, True)
    # plot_coin('ethereum', 'Ethereum', '20200101', '20211231', 'miner', False, False)
    # plot_coin('litecoin', 'Litecoin', '20200101', '20211231', 'guessed_miner', True, False)

    plot_nakamoto(names, capitalized_names, start_date, end_date, miner_fields)
    plot_gini(names, capitalized_names, start_date, end_date, miner_fields)
    plot_theil(names, capitalized_names, start_date, end_date, miner_fields)
    plot_upc(names, capitalized_names, start_date, end_date, miner_fields)

    # plot_pie('dash', 'Dash', '20200101', '20211231', 'guessed_miner')
    # plot_pie('bitcoin', 'Bitcoin', '20200101', '20211231', 'guessed_miner')
    # plot_pie('bitcoin-cash', 'BitcoinCash', '20200101', '20211231', 'guessed_miner')
    # plot_pie('ethereum', 'Ethereum', '20200101', '20211231', 'miner')
    # plot_pie('litecoin', 'Litecoin', '20200101', '20211231', 'guessed_miner')

if __name__ == '__main__':
    main()