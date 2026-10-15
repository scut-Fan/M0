import time
import json

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
             
# 拓扑排序
# def tasks_sort(None):
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

