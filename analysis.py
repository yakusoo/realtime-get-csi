import json
import sys
import numpy as np
import subprocess
import os
import cmath
import math
import csv
import pickle

def capture_length(tdatetime):
    with open("%d_cktdata.json" % (tdatetime), "r") as f:
        json_dict = json.load(f)
        length = len(json_dict)
    return length

def get_matrix_data(i, tdatetime, list_src, list1, ap_address, sta_address):
    with open("%d_cktdata.json" % (tdatetime), "r") as f:
        json_dict = json.load(f)

    dst_data = json_dict[i]["_source"]["layers"]["wlan.da"]
    if dst_data[0] != ap_address: #'bc:c3:42:a2:2c:40':
        print('AP is wrong')
        return 0
    raw_data = json_dict[i]["_source"]["layers"]["data.data"]
    src_data = json_dict[i]["_source"]["layers"]["wlan.ta"]
    if src_data[0] not in list_src:
        list_src.append(src_data[0])
    data1 = raw_data[0].split(":")

    length = len(data1)
    data1 = [int(data1[p], 16) for p in range(length)]
#    for p in range(length):
#       data1[p] = int(data1[p], 16)
    label = json_dict[i]["_source"]["layers"]["wlan.ta"]
    if label[0] == sta_address:#'d8:c4:6a:87:2c:5f':
        list1.append(data1)

def get_snr(input_list, number):
    if len(input_list) != 0:
        snr = input_list[number][5]
        if snr >= pow(2, 7):
            snr = snr - pow(2, 8)
        snr_result = 22 + 0.25 * snr
        f = open('results/snr_results.txt', 'a')
        f.write('%f\n' % (snr_result))
        f.close()
        return snr

def get_csi(input_list, output_list, number):
    csi = []
    sample = []
    if len(input_list) != 0:
        csi = [format(input_list[number][i], 'b').zfill(8)[::-1] for i in range(7, len(input_list[0]))]
#        for i in range(6, len(input_list[0])):
#            csi_2byte = format(input_list[number][i], 'b').zfill(8)[::-1]
#            csi.append(csi_2byte)   

        csi = ''.join(csi)
#        p = cmath.pi
        for i in range(52):
            sample.append(int(csi[50*i:50*i+6][::-1], 2)/32 + 1/64)
            sample.append(int(csi[50*i+6:50*i+12][::-1], 2)/32 + 1/64)
            sample.append(int(csi[50*i+12:50*i+18][::-1], 2)/32 + 1/64)
            sample.append(int(csi[50*i+18:50*i+22][::-1], 2)/32 + 1/64)
            sample.append(int(csi[50*i+22:50*i+26][::-1], 2)/32 + 1/64)
            sample.append(int(csi[50*i+26:50*i+30][::-1], 2)/32 + 1/64)
        for i in range(312):
#            with open('results/phase_results.txt', 'a') as f:
#                f.write('%f\n' % (sample[i]))
            sample[i] *= cmath.pi
            output_list.append(math.cos(sample[i]))
            output_list.append(math.sin(sample[i]))
#        print('/n'.join(sample))
        with open('results/phase_results.txt', 'a') as f:
            for i in range(312):
                f.write('%f\n' % (sample[i]))
#             pickle.dump(str(sample),f)
#            f.writelines('/n'.join(str(sample)))

def get_csi_list(input_list ,output_list, number, label, input_filename):
    for i in range(number):
        sample = [] 
        for rank in range(52):
           for row in range(12):
               sample.append(input_list[row + rank * 12 + i * 624])

        output_list[0].append(sample)
    for i in range(number):
        output_list[1].append(label)
    filename = input_filename
    if os.path.exists(filename):
        train = np.load(filename)
        train = train.tolist()
    else:
        train = [[], []]
    for i in range(number):
        train[0].append(output_list[0][i])
        train[1].append(output_list[1][i])
    np.save(filename, train)

def rm_json(date):
    cmd = "shred --remove %d_cktdata.json" % (date)
    subprocess.run(cmd, shell=True)

def wait_time(time):
    cmd = "sleep %d" % (time)
    subprocess.run(cmd, shell=True)

def get_csi_eval(input_list ,output_list, number):
    for i in range(number):
        sample = [] 
        for rank in range(52):
           for row in range(12):
               sample.append(input_list[row + rank * 12 + i * 624])

        output_list[0].append(sample)
    label_list = []
    #for i in range(number):
    #    output_list[1].append(label)

def get_csi_result(input_list ,output_list, number, label):
    for i in range(number):
        sample = [] 
        for rank in range(52):
           for row in range(12):
               sample.append(input_list[row + rank * 12 + i * 624])

        output_list[0].append(sample)
    label_list = []
    for i in range(number):
        output_list[1].append(label)

 



  

