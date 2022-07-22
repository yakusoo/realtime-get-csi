#!/bin/bash

tshark -D
read -p "select interface: " INTERFACE
DATE=`date "+%F"`
tshark -i $INTERFACE -f 'wlan.fc.type_subtype == 14' -c 1000 -w $DATE
