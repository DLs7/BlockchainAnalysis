#!/bin/bash

NAME=$1             # lower-case name on blockchair.com/dumps
CAPITALIZED_NAME=$2 # capitalized name
START_DATE=$3       # start date in YYYYMMDD
END_DATE=$4         # end date in YYYYMMDD
DIR=$5              # download directory

mkdir -p ${DIR}/${CAPITALIZED_NAME}

CURRENT_DATE=$START_DATE
i=0
while [ $CURRENT_DATE != $END_DATE ]
do
    echo $CURRENT_DATE
    wget https://gz.blockchair.com/${NAME}/blocks/blockchair_${NAME}_blocks_${CURRENT_DATE}.tsv.gz -P ${DIR}/${CAPITALIZED_NAME}
    CURRENT_DATE=$(date +%Y%m%d -d "$DATE + $i day")
    i=$((i + 1))
done