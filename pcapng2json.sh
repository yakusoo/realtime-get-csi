#!/bin/bash
USING="Using: $0 'pcapfile_path'"
if [ $# -eq 0 ]; then
	echo $USING
else
    for FILEPATH in $@
    do
        EXTENSION=${FILEPATH##*.}
        if [ ! -e $FILEPATH ]; then
            echo $FILEPATH not exists
            exit 1
        elif [ $EXTENSION != "pcapng" ]; then
            echo Not pcapng file
            exit 2
        fi
    done
    read -p "チャネル番号指定(1/36)： " NUM
    for FILEPATH in $@
    do
        PCAPNG=${FILEPATH##*/}
        mkdir data > /dev/null 2>&1
        mkdir -p csicsvfile/data > /dev/null 2>&1
        tshark -x -r $FILEPATH -T json > data/$PCAPNG.json
        python3 json2csi.py $NUM
        mv csicsvfile/data/* csicsvfile
        rmdir csicsvfile/data
    done
fi

# currentdir
#    ├── json2csi.py
#    ├── pcap
#    │   ├── sw501_1.pcapng
#    │   ├── sw501_2.pcapng
#    │   └── ....
#    └── pcapng2json.sh
#
# │
# │
# ↓
# sh ./pcapng2json.sh pcap/*
#
# │
# │
# ↓
#
# currentdir
#    ├── csicsvfile
#    │   ├── 1.csv
#    │   ├── 2.csv
#    │   └── ....
#    ├── data
#    │   ├── sw501_1.pcapng.json
#    │   ├── sw501_2.pcapng.json
#    │   └── ....
#    ├── json2csi.py
#    ├── pcap
#    │   ├── sw501_1.pcapng
#    │   ├── sw501_2.pcapng
#    │   └── ....
#    └── pcapng2json.sh