import time
import json
from collections import deque

READ_FILE = "tasks_demo.json"
dictionary = {}

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
    while q:
        e = q.popleft()
        result.append(e)
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

