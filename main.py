import gzip
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Bitcoin
bitcoin_start_date = datetime.datetime.strptime("20090109", "%Y%m%d")
current_date = bitcoin_start_date
files = []

i = 0
while current_date != datetime.datetime.strptime("20220113", "%Y%m%d"):
    file = "/home/agasta/hdd/TCC/Bitcoin/blockchair_bitcoin_blocks_" + datetime.datetime.strftime(current_date, "%Y%m%d") + ".tsv.gz"
    files.append(file)
    current_date = bitcoin_start_date + datetime.timedelta(days=i)
    i+=1

df = [pd.read_csv(file, sep="\t", header=0) for file in files]
big_df = pd.concat(df)

foundry_digital_substring = "466f756e6472792055534120506f6f6c202364726f70676f6c64"
big_df['coinbase_data_hex'] = big_df['coinbase_data_hex'].astype(str)
big_df.loc[big_df['coinbase_data_hex'].str.contains(foundry_digital_substring), 'guessed_miner'] = "FoundryDigital"

big_df_count = big_df['guessed_miner'].value_counts().to_frame('blocks')
# valuable_info = bisg_df_count[['pools']].values

print(big_df_count);

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(big_df_count)


# foundry_digital_substring = "466f756e6472792055534120506f6f6c202364726f70676f6c64"
# big_df['coinbase_data_hex'] = big_df['coinbase_data_hex'].astype(str)
# big_df.loc[big_df['coinbase_data_hex'].str.contains(foundry_digital_substring), 'guessed_miner'] = "FoundryDigital"

# big_df['date'] = pd.to_datetime(big_df['time'])
# big_df = big_df.set_index('date')

# big_df2 = big_df.resample('D')['guessed_miner'].value_counts()
# big_df2.name = 'blocks'
# big_df2 = big_df2.reset_index('guessed_miner')

# big_df3 = big_df2.resample('D')['blocks'].sum()
# big_df2['percent'] = big_df2['blocks'].div(big_df3) * 100

# big_df2.pivot(columns='guessed_miner', values="percent").fillna(0).plot.area()
# plt.show()

# Bitcoin Cash
# with gzip.open('/home/agasta/hdd/TCC/BitcoinCash/blockchair_bitcoin-cash_blocks_20220113.tsv.gz', 'rb') as f:
#     for i in range(1):
#         line = f.readline()
#         print(i, line)


# # Dogecoin
# with gzip.open('/home/agasta/hdd/TCC/Dogecoin/blockchair_dogecoin_blocks_20220113.tsv.gz', 'rb') as f:
#     for i in range(1):
#         line = f.readline()
#         print(i, line)


# # Ethereum
# with gzip.open('/home/agasta/hdd/TCC/Ethereum/blockchair_ethereum_blocks_20220113.tsv.gz', 'rb') as f:
#     for i in range(1):
#         line = f.readline()
#         print(i, line)


# # Litecoin
# with gzip.open('/home/agasta/hdd/TCC/Litecoin/blockchair_litecoin_blocks_20220113.tsv.gz', 'rb') as f:
#     for i in range(1):
#         line = f.readline()
#         print(i, line)