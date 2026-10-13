import yaml
import csv
import math
import numpy

CONFIG_PATH = "config.yaml"

try:
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)
except Exception as e:
    print(f"出现了异常，异常名是 {e}")

csv_path = cfg["input_csv"]
try:
    col_x = cfg["columns"]["x"]
    col_y = cfg["columns"]["y"]
except NameError as e:
    print("出现了异常，列名不匹配")

xs = []      # 空列表
ys = []

try:
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            xs.append(float(row[col_x]))
            ys.append(float(row[col_y]))     #从文件里读取元素并且尾插到列表中
except Exception as e:
    print(f"出现了异常，异常名是 {e}")

n = len(xs)

def correlation(xs,ys):
    """
    这是一个求相关系数的函数，传入x和y后，会自动计算x和y的均值和方差，
    然后根据相关系数公式计算出相关系数
    """
    sum_x = 0.0
    sum_y = 0.0
    global n
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
        dx += a*a                  # 方差（不对，也没除以总量）
        dy += b*b
        prod += a*b                # 协方差（这个公式是对的）
        
    demon = ((dx/n) * (dy/n)) **0.5   # 这一步实现开根号的操作，demon是标准差的乘积
    
    try:
        r = prod / demon               # 相关系数的分母应为标准差
    except ZeroDivisionError as e:
        print("出现了异常！有一列的方差为0！")
    else:
        print("n =", n)
        print("mean_x =", mean_x)
        print("mean_y =", mean_y)
        print("r =", r)

if __name__ = 'main'        
    result1 = correlation([1,2,3],[2,4,6])   # 测试程序
    result2 = numpy.corrcoef([1,2,3],[2,4,6])
    print(f"模块函数计算结果：{result1}")
    print(f"numpy函数计算结果：{result2}")
