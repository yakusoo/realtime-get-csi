#!/usr/bin/env python
# --coding:utf-8--

import os
import json
import random

snr_path = 'results/snr.txt'
image_path = 'results/image.txt'
accuracy_path = 'results/accuracy.txt'
package_path = 'results/package.txt'


def get_snr_avg(snr_path):
    snr_sum = 0
    snr_count = 0
    with open(snr_path, 'r') as f:
        for line in f:
            snr = line.rstrip('\r\n')
            snr_sum += float(snr)
            snr_count += 1
    return round(snr_sum / snr_count, 6)


def get_phase_arr(phase_path):
    phase_arr = [[0 for i in range(52)] for j in range(6)]
    phase_index_arr = 0
    phase_index = 0
    with open(phase_path, 'r') as f:
        for line in f:
            phase = line.rstrip('\r\n')
            phase_arr[phase_index][phase_index_arr] = {'x': phase_index_arr + 1, 'y': float(phase)}
            phase_index += 1
            if phase_index == 6:
                phase_index = 0
                phase_index_arr += 1
            if phase_index_arr == 52:
                break
    return phase_arr


def get_result(result_path):
    result_arr = [0 for i in range (3)]
    index = 0
    with open(result_path, 'r') as f:
        for line in f:
            result = line.rstrip('\r\n')
            result_arr[index] = int(result)
            index += 1
    return result_arr


def list_to_json(list):
    jsontxt = []
    for item in list:
       key, value = item.split(':')
       jsontxt.append({'x':key, 'y':value});
    return jsontxt


def read_file(filename):
    data = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                result = line.rstrip('\r\n')
                data.append(result)
    return data


def write_file(filename, snr_data):
    with open(filename , 'w') as f:
        for snr in snr_data:
            f.write(snr + '\n')


def update_data(index):
    # snrデータ
    snr_avg = get_snr_avg('results/snr_results.txt');
    snr_data = read_file(snr_path)
    if len(snr_data) == 10:
        snr_data.pop(0)
    snr_data.append('{}:{}'.format(index, snr_avg))
    write_file(snr_path, snr_data)
    # 周波数データ
    phase_data = get_phase_arr('results/phase_results.txt')
    # 解析結果データ
    result = get_result('results/result.txt')
    # 画像データ
    image_data = read_file(image_path)
    if len(image_data) == 10:
        image_data.pop(0)
    image_data.append('{}:{}'.format(index, result[0]))
    write_file(image_path, image_data)
    # 精度データ
    accuracy_data = read_file(accuracy_path)
    if len(accuracy_data) == 10:
        accuracy_data.pop(0)
    accuracy_data.append('{}:{}'.format(index, result[1]))
    write_file(accuracy_path, accuracy_data)
    # 取得パケット数データ
    package_data = read_file(package_path)
    if len(package_data) == 10:
        package_data.pop(0)
    package_data.append('{}:{}'.format(index, result[2]))
    write_file(package_path, package_data)
    # レスポンスJSONデータ
    response_json = {
        'snr':list_to_json(snr_data),
        'phase':phase_data,
        'image':list_to_json(image_data),
        'accuracy':list_to_json(accuracy_data),
        'package':list_to_json(package_data),
        }
    #print(json.dumps(response_json))
    return json.dumps(response_json)

