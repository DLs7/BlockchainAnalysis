#!/bin/bash

TODAY=$(date +%Y%m%d)
DATE=20101102
NEW_DATE=DATE
i=0

while [ $NEW_DATE != $TODAY ]
do
    echo $NEW_DATE
    wget https://gz.blockchair.com/bitcoin/blocks/blockchair_bitcoin_blocks_${NEW_DATE}.tsv.gz -P /home/agasta/hdd/TCC/Bitcoin
    NEW_DATE=$(date +%Y%m%d -d "$DATE + $i day")
    i=$((i + 1))
done

DATE=20090103
NEW_DATE=DATE
i=0

while [ $NEW_DATE != $TODAY ]
do
    echo $NEW_DATE
    wget https://gz.blockchair.com/bitcoin-cash/blocks/blockchair_bitcoin-cash_blocks_${NEW_DATE}.tsv.gz -P /home/agasta/hdd/TCC/BitcoinCash
    NEW_DATE=$(date +%Y%m%d -d "$DATE + $i day")
    i=$((i + 1))
done

DATE=20131206
NEW_DATE=DATE
i=0

while [ $NEW_DATE != $TODAY ]
do
    echo $NEW_DATE
    wget https://gz.blockchair.com/dogecoin/blocks/blockchair_dogecoin_blocks_${NEW_DATE}.tsv.gz -P /home/agasta/hdd/TCC/Dogecoin
    NEW_DATE=$(date +%Y%m%d -d "$DATE + $i day")
    i=$((i + 1))
done

DATE=20150730
NEW_DATE=DATE
i=0

while [ $NEW_DATE != $TODAY ]
do
    echo $NEW_DATE
    wget https://gz.blockchair.com/ethereum/blocks/blockchair_ethereum_blocks_${NEW_DATE}.tsv.gz -P /home/agasta/hdd/TCC/Ethereum
    NEW_DATE=$(date +%Y%m%d -d "$DATE + $i day")
    i=$((i + 1))
done

DATE=20111007
NEW_DATE=DATE
i=0

while [ $NEW_DATE != $TODAY ]
do
    echo $NEW_DATE
    wget https://gz.blockchair.com/litecoin/blocks/blockchair_litecoin_blocks_${NEW_DATE}.tsv.gz -P /home/agasta/hdd/TCC/Litecoin
    NEW_DATE=$(date +%Y%m%d -d "$DATE + $i day")
    i=$((i + 1))
done