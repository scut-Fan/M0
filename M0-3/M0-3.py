#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sensor_analyzer.py  —— 上一届学长留下的"能用"的脚本

注释（学长原话）：
    "处理一下传感器数据就能用"

原本意图：
    1. 读取 sensor_data.csv（列：time, value）
    2. 计算 value 的平均值、标准差
    3. 剔除离群值（|value - mean| > 2 * std）
    4. 把清洗后的数据保存为 cleaned_data.csv
    5. 打印一份统计摘要

现状：跑不通 / 跑出来数不对。就交给你了。
"""

import csv
import os

INPUT_FILE = "sensor_data.csv"
OUTPUT_FILE = "cleaned_data.csv"
OUTPUT_DIR = "out"  # 输出目录

data = []
times = []
cleaned = []

print("=== 传感器数据分析 ===")

# --- 读取数据 ---
with open(INPUT_FILE,"r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        t = float(row["time"])
        v = float(row["value"])                     #这里是不是有问题？
        times.append(t)
        data.append(v)

print("共读取 %d 条数据" % len(data))

# --- 计算平均值 ---
total = 0
for v in data:
    total += v
mean = total / len(data)

# --- 计算标准差 ---
acc = 0
for v in data:
    acc += (v - mean) ** 2                            # 标准差的公式(已修正)
std = (acc / len(data)) ** 0.5

# --- 剔除离群值 ---
for v in data:
    if v > mean + 2 * std:                       # 要用绝对值来判断，这里不对
        data.remove(v)
    elif v < mean + (-2) * std:
        data.remove(v)                           # 负数时绝对值判断
    else:
        cleaned.append(v)                        # 两次判断都没问题就写入cleaned列表中

        
# --- 输出清洗后的数据 ---                         记得运行的时候这里报错了没法输出清洗的数据
output_path = os.path.join("/", OUTPUT_DIR, OUTPUT_FILE)
try:
    f = open(output_path, "w")
    writer = csv.writer(f)
    writer.writerow(["time", "value"])
    for v in cleaned:
        writer.writerow([v])
except Exception as e:
    print(f"出现了异常，异常名称为{e}")

print("均值 mean = %.4f" % mean)
print("标准差 std = %.4f" % std)
print("清洗后剩余 %d 条" % len(cleaned))
print("已保存到 %s" % output_path)
