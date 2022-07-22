# Convert JSON to CSI from Compressed beamforming report packet flame
import os
import sys
import cmath
import csv
import math
from json import JSONDecoder
from glob import glob
from tqdm import tqdm

# コマンドライン引数を変数に代入
argvs = sys.argv

# 使用帯域によりMACアドレスの末尾が変わる
# ch1  : 70
if len(argvs) == 1:
    raise("NO CHANNEL NUMBER")
if argvs[1] == "1":
    ta_addr = "18:ec:e7:f0:25:70"
# ch36 : 78
elif argvs[1] == "36":
    ta_addr = "18:ec:e7:f0:25:78"
else:
    raise("NO VALID CHANNEL NUMBER")

# wlanという重複したキーが存在するのでそれに対処するための関数
def make_unique(key, dct):
    counter = 0
    unique_key = key
    while unique_key in dct:
        counter += 1
        unique_key = '{}_{}'.format(key, counter)
    return unique_key
def parse_object_pairs(pairs):
    dct = {}
    for key, value in pairs:
        if key in dct:
            key = make_unique(key, dct)
        dct[key] = value
    return dct

# JSONファイルフォルダ選択
decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
file_list = sorted(glob("data/*.json"))
record = []

for item in tqdm(file_list):
    csi = []
    csi_sin = []
    csi_cos = []
    csi_all = []
    print("Now processing --> ", item)
    with open(item, "r") as f:
        raw = f.read()
        data_list = decoder.decode(raw)

    for data in data_list:
        wlan_da = data["_source"]["layers"]["wlan"]["wlan.da"]  # dst
        wlan_ta = data["_source"]["layers"]["wlan"]["wlan.ta"]  # src
        captured_at = data["_source"]["layers"]["frame"]["frame.time"]
        try:
            nc_index = data["_source"]["layers"]["wlan.mgt"][
                "Fixed parameters"]["wlan.he.action_tree"]["wlan.he.action.he_mimo_control_tree"][
                    "wlan.he.mimo.nc_index"]
            nr_index = data["_source"]["layers"]["wlan.mgt"][
                "Fixed parameters"]["wlan.he.action_tree"]["wlan.he.action.he_mimo_control_tree"][
                    "wlan.he.mimo.nr_index"]
            codebook_info = data["_source"]["layers"]["wlan.mgt"][
                "Fixed parameters"]["wlan.he.action_tree"]["wlan.he.action.he_mimo_control_tree"][
                    "wlan.he.mimo.codebook_info"]
        except KeyError:
            print("KeyError")
            nc_index = 1
            nr_index = 3
            codebook_info = 1
        # compressed beamforming report raw data
        cbr_raw_data = data["_source"]["layers"][
            "wlan.mgt_raw"]

        cbr_raw_data = cbr_raw_data[0]
        nc_index = int(nc_index) + 1
        nr_index = int(nr_index) + 1
        N_a = 10
        subcarrer_number = 64

        # cbr以外のデータの長さ
        asnr_length = nc_index * 2
        mimo_control_field_length = 14
        other_length = mimo_control_field_length + asnr_length
        # cbr抽出
        cbr_raw_data = cbr_raw_data[other_length:]

        if codebook_info == "0":
            phi_size = 4
            psi_size = 2
        elif codebook_info == "1":
            phi_size = 6
            psi_size = 4
        else:
            continue

        bytes_le = bytes.fromhex(cbr_raw_data)
        bytes_be = bytes_le[::-1]
        hex_be = bytes_be.hex()
        cbr_int = int(hex_be, 16)
        cbr_bnr = bin(cbr_int)
        cbr_bnr = cbr_bnr[2:]
        scdix_length = int(((phi_size+psi_size)/2)*N_a)
        scdix = []
        for i in range(subcarrer_number):
            scdix.append(cbr_bnr[i*scdix_length:(i+1)*scdix_length])
        scdix.reverse()
        max_length = len(scdix)
        if wlan_da == ta_addr:
            csis = []
            csis_sin = []
            csis_cos = []
            csis_all = []
            for i in range(0, max_length):
                d = scdix[i]
                csis.append(int(d[44:], 2)/32 + 1/64)
                csis.append(int(d[38:44], 2)/32 + 1/64)
                csis.append(int(d[32:38], 2)/32 + 1/64)
                csis.append(int(d[28:32], 2)/32 + 1/64)
                csis.append(int(d[24:28], 2)/32 + 1/64)
                csis.append(int(d[20:24], 2)/32 + 1/64)
                csis.append(int(d[14:20], 2)/32 + 1/64)
                csis.append(int(d[8:14], 2)/32 + 1/64)
                csis.append(int(d[4:8], 2)/32 + 1/64)
                csis.append(int(d[:4], 2)/32 + 1/64)
            for i in range(len(csis)):
                csis[i] *= cmath.pi
            for i in range(len(csis)):
                csis_sin.append(math.sin(csis[i]))
                csis_cos.append(math.cos(csis[i]))

            csis_all.extend(csis)
            csis_all.extend(csis_sin)
            csis_all.extend(csis_cos)
            csi_all.append(csis_all)

            csi.append(csis)
            csi_sin.append(csis_sin)
            csi_cos.append(csis_cos)

    if len(csi) != 0:
        item = item.replace(".pcapng.json", "")
        item = item.replace(".json", "")
        item = item.replace("sw501_", "")
        item = item.replace("sw5036_", "")
        item = item.replace("20pear202107270", "")
        item = item.replace("20pear20210727", "")
        item = item.replace("20pear202108300", "")
        item = item.replace("20pear20210830", "")
        item = item.replace("c501", "")
        item = item.replace("c5036", "")
        item = item.replace("w501", "")
        item = item.replace("w5036", "")

        # packet数を100に揃えます
        csi = csi[:100]
        csi_sin = csi_sin[:100]
        csi_cos = csi_cos[:100]
        csi_all = csi_all[:100]

        filename = item + ".csv"
        writer_path = os.path.join("csicsvfile", filename)

        with open(writer_path, "w") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(csi_all)
        print("パケット数：", len(csi_all), "  /  列数(subcar*10*3(ori,sin,cos))：", len(csi_all[0]))
    else:
        print("パケットなし")

    print("-----------------------------------------------")
