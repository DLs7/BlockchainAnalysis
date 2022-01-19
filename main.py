import gzip

# Bitcoin
with gzip.open('/home/agasta/hdd/TCC/Bitcoin/blockchair_bitcoin_blocks_20220113.tsv.gz', 'rb') as f:
    for i in range(1):
        line = f.readline()
        print(i, line)


# Bitcoin Cash
with gzip.open('/home/agasta/hdd/TCC/BitcoinCash/blockchair_bitcoin-cash_blocks_20220113.tsv.gz', 'rb') as f:
    for i in range(1):
        line = f.readline()
        print(i, line)


# Dogecoin
with gzip.open('/home/agasta/hdd/TCC/Dogecoin/blockchair_dogecoin_blocks_20220113.tsv.gz', 'rb') as f:
    for i in range(1):
        line = f.readline()
        print(i, line)


# Ethereum
with gzip.open('/home/agasta/hdd/TCC/Ethereum/blockchair_ethereum_blocks_20220113.tsv.gz', 'rb') as f:
    for i in range(1):
        line = f.readline()
        print(i, line)


# Litecoin
with gzip.open('/home/agasta/hdd/TCC/Litecoin/blockchair_litecoin_blocks_20220113.tsv.gz', 'rb') as f:
    for i in range(1):
        line = f.readline()
        print(i, line)