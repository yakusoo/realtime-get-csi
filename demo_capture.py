# arg1: filename
# arg2: measurement duration [s]
# arg3: input_label 0~10
# arg4: AP_MACaddress bc:c3:42:a2:2c:40
# arg5: STA_MACaddress d8:c4:6a:87:2c:5f
import subprocess
import datetime
import json
import sys
import numpy as np
import pickle
import os
import time
from analysis import capture_length, get_matrix_data, get_snr, get_csi, get_csi_list, rm_json, wait_time
#from test import get_snr, get_csi, get_csi_matrix

#filename1 = '20181026_test_model1.npy' 
filename1 = sys.argv[1]
tdatetime = datetime.datetime.now()
cmd = "tshark -i mon0 -x --disable-protocol wlan_mgt -Y 'wlan.fc.type_subtype == 0x000e' -T json -e wlan.ta -e wlan.da -e data.data -a duration:" + sys.argv[2] + " > $(date +%Y%m%d%H)_cktdata.json"
src_list = []
feedback_data1 = []
feedback_csi1 = []
feature1 = [[], []]
#input_label = int(input('input label: '))
input_label = int(sys.argv[3])

now = tdatetime.strftime("%Y%m%d%H")
#wait_time(10)
subprocess.run(cmd, shell=True)
now = int(now)
print(now)
length = capture_length(now)

for i in range(length):
    get_matrix_data(i, now, src_list, feedback_data1, sys.argv[4], sys.argv[5])
#get_matrix_data(i, now, src_list, feedback_data1, 'bc:c3:42:a2:2c:40', 'd8:c4:6a:87:2c:5f')

for i in range(length):
    get_snr(feedback_data1,i)
for i in range(len(feedback_data1)):
    get_csi(feedback_data1,feedback_csi1, i)
get_csi_list(feedback_csi1, feature1, int(len(feedback_csi1)/624), input_label, filename1)

#rm_json(now)

print(src_list)
