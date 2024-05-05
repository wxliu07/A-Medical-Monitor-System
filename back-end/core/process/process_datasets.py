import json
import csv
from datetime import datetime
import os
import numpy as np

# 文件夹路径
json_folder = '../video/JSON'
csv_folder = '../video/DATA'

# 处理10个JSON文件
for i in range(1, 11):
    json_filename = os.path.join(json_folder, f'A{i:02d}-01.json')
    csv_filename = os.path.join(csv_folder, f'A{i:02d}-01.csv')

    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'SpO2', 'HR', 'RR'])

    processed_timestamps = set()    # 记录已经处理过的秒级时间戳

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 一次性加载整个JSON文件
        with open(json_filename, 'r') as jsonfile:
            data = json.load(jsonfile)
            # 处理每个JSON对象
            for item in data['/FullPackage']:
                timestamp_seconds = int(item['Timestamp'] // 1e9)   # 提取Timestamp字段并转换为秒级别
                # 如果已经处理过该秒级时间戳，则跳过当前数据
                if timestamp_seconds in processed_timestamps:
                    continue

                # 记录已处理的秒级时间戳
                processed_timestamps.add(timestamp_seconds)
                # 格式化时间字符串
                time_str = datetime.fromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
                # 提取血氧饱和度和心率字段
                spo2 = item['Value']['o2saturation']
                hr = item['Value']['pulseRate']

                # 生成呼吸率（RR），假设与心率（HR）存在一定的相关性, 使用正态分布来生成RR
                mean_rr = hr * 0.2
                std_dev_rr = hr * 0.1
                rr = max(13, min(18, np.random.normal(mean_rr, std_dev_rr)))  # 限制呼吸率在14到18之间
                rr = int(rr)
                writer.writerow([time_str, spo2, hr, rr])
