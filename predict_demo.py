# arg1: model_filename .sav
# arg2: AP_MACaddress bc:c3:42:a2:2c:40
# arg3: STA_MACaddress d8:c4:6a:87:2c:5f

import subprocess
import datetime
import json
import sys
import numpy as np
from sklearn import cluster
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pickle
import os
from analysis import capture_length, get_matrix_data, get_snr, get_csi, get_csi_eval, rm_json, wait_time
from machine_learning import svm_check, error
tdatetime = datetime.datetime.now()
cmd = "tshark -i mon0 -x --disable-protocol wlan_mgt -Y 'wlan.fc.type_subtype == 0x000e' -T json -e wlan.ta -e wlan.da -e data.data -a duration:" + sys.argv[4] + " > $(date +%Y%m%d%H)_cktdata.json"
src_list = []
feedback_data1 = []
feedback_csi1 = []
feature1 = [[], []]
now = tdatetime.strftime("%Y%m%d%H")
#wait_time(10)
print('計測を開始します')
subprocess.run(cmd, shell=True)
now = int(now)
length = capture_length(now)
for i in range(length):
    get_matrix_data(i, now, src_list, feedback_data1, sys.argv[2], sys.argv[3])
#get_matrix_data(i, now, src_list, feedback_data1, 'bc:c3:42:a2:2c:40', 'd8:c4:6a:87:2c:5f')

if len(feedback_data1) == 0:
    error()
    print('計測に失敗しました')
    print('実行or終了を押してください')
    exit()

if os.path.exists("./results/snr_results.txt"):
    os.remove("./results/snr_results.txt")
if os.path.exists("./results/phase_results.txt"):
    os.remove("./results/phase_results.txt")

for i in range(len(feedback_data1)):
    get_csi(feedback_data1,feedback_csi1, i)
    get_snr(feedback_data1, i)
#print(feedback_csi1)

if len(feedback_csi1) != 0:
    get_csi_eval(feedback_csi1, feature1, int(len(feedback_csi1)/624))
else:
    print('cannot capture in node1')

#svm_score = svm_check(feature1, input_label)
svm_check(feature1,sys.argv[1])

rm_json(now)
print('計測に成功しました。結果をUI上に表示します')
print('実行or終了を押してください')
