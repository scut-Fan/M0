import yaml
import csv
import math

CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

csv_path = cfg["input_csv"]
col_x = cfg["columns"]["x"]
col_y = cfg["columns"]["y"]

xs = []
ys = []

with open(csv_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        xs.append(float(row[col_x]))
        ys.append(float(row[col_y]))     #从文件里读取元素并且尾插到列表中

n = len(xs)

sum_x = 0.0
sum_y = 0.0
for i in range(n):
    sum_x = sum_x + xs[i]
    sum_y = sum_y + ys[i]

mean_x = sum_x / n
mean_y = sum_y / n                # 求平均数的操作

dx = 0.0
dy = 0.0
prod = 0.0
for i in range(n):
    a = xs[i] - mean_x
    b = ys[i] - mean_y
    dx = dx + a * a   
    dy = dy + b * b              # 求方差
    prod = prod + a * b

denom = dx * dy
r = prod / denom                 # 求相关系数的公式真的是这个吗？

print("n =", n)
print("mean_x =", mean_x)
print("mean_y =", mean_y)
print("r =", r)

def correlation(x,y):
    """
    这是一个求相关系数的函数，传入x和y后，会自动计算x和y的均值和方差，
    然后根据相关系数公式计算出相关系数
    """
    sum_x = 0.0
    sum_y = 0.0
    n = len(xs)
    for i in range(n)
        sum_x += xs[i]
        sum_y += ys[i]
        
    meant_x = sum_x / n
    meant_y = sum_y / n
    
    dx = 0.0
    dy = 0.0
    prod = 0.0
    for i in range(n)
        a = xs[i] - meant_x
        b = ys[i] - meant_y
        dx += a*a
        dy += b*b
        prod += a*b
        
    demon = dx * dy
    r = prod / demon
    
    print("n =", n)
    print("mean_x =", mean_x)
    print("mean_y =", mean_y)
    print("r =", r)   
