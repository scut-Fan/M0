import time
import json
from collections import deque
import random
import signal

def timeout_handler(second):
    """
    该函数用于给整个程序定时，超时则终止程序
    """
    signal.signal(signal.SIGALRM, lambda s,f: exit("TIMEOUT"))
    signal.alarm(second)

start = time.time()      # 开始计时

dictionary = {}
READ_FILE = "tasks_demo.json"
status_str = ["SUCCESS","FAILED","RETRY","SKIPPED"]  # 定义任务的四种状态
final_state = ["SUCCESS","SKIPPED"]
current_state ["SUCCESS","FAILED","RETRY","SKIPPED"] # 定义任务的当前状态以及最终状态

def color_print(text):
    """
         这个函数用于控制台某些字符串的彩色输出
    """
    if text == "SUCCESS":
        print("\033[32mSUCCESS\033[0m")
    elif text == "FAILED":
        print("\033[31mFAILED\033[0m")
    elif text == "RETRY":
        print("\033[33mRETRY\033[0m")
    elif text == "SKIPPED":
        print("\033[34mSKIPPED\033[0m")
    else:
        print(text)
    return text    
    

with open(READ_FILE, "r") as f:
    dictionary = json.load(f)

"""    
for k in dictionary.keys():
    print(k,dictionary[k])
"""
    
# 有向无环图
task_graph = {
             "Init" : ("Navigate"),
             "Navigate" : ("DetectQR", "AvoidObstacle"),
             "DetectQR" : ("Grasp"),
             "Grasp" : ("Place"),
             "AvoidObstacle" : ("Place"),
             "Place" : ("ReturnHome")
             }
             
# 计算有向无环图的入度
nodes = set()
value = tuple()
for k in task_graph.keys():
    nodes.add(k)
    value = task_graph[k]
    if not isinstance(value,tuple):
        value = (value,)
    for v in value:
        nodes.add(v)

print("nodes里面的全部节点：",nodes)

indegree = {}
for n in nodes:
    indegree[n] = 0            # 初始化入度为0,入度这里没问题

for k in task_graph.keys():
    v = task_graph[k]
    if not isinstance(v,tuple):
        v = (v,)
    for vt in v:
        indegree[vt] += 1

print("各节点入度：")
print(indegree)

# ---拓扑排序---
def task_sort():
    """
    该函数用于实现对文件任务的拓扑排序并按依赖顺序执行，
    生成一份依赖清单
    """
    global task_graph
    global indegree
    q = deque()
    result = []
    for node in indegree:
        if indegree[node] == 0:
            q.append(node)
            time.sleep(0.5)
    while q:
        e = q.popleft()
        result.append(e)
        i = 1
        while i <= 3:
            time.sleep(0.5)
            test = random.choices(["SUCCESS","FAILED"], weights = [0.8 , 0.2])[0]
            # choice返回一个列表，因此要加下标返回单次结果
            print(f"任务{e}第{i}次尝试结果：",end = "")
            color_print(test)
            if test == "SUCCESS":
                break;
            else:
                if i == 3:
                    print(f"三次都失败！",end = "")
                    color_print(status_str[3])
                i += 1
                

        if e in task_graph:
            value = task_graph[e]       # 找到哪些任务依赖这一个节点
            if not isinstance(value,tuple):
                value = (value,)
            for v in value:
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)
    if len(result) == len(indegree):         
        print(result)
    else:
        print("图有环，无法拓扑排序")
        
        
task_sort()
end = time.time()
print(f"共耗时 {end-start:.4f}秒")
