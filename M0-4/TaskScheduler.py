import time
import json
from collections import deque
import random
import signal

# ---读取文件---
dictionary = {}       # dictionary字典用于存储文件内容
tasks = {}            # tasks字典用于存储文件里的任务信息
READ_FILE = "tasks_demo.json"
with open(READ_FILE, "r") as f:
    dictionary = json.load(f)
   
MAX_TIME = dictionary["timeout"]    

# ---定时与计时---
def timeout_handler(second):
    """
         该函数用于给整个程序定时,超时则终止程序
    """
    signal.signal(signal.SIGALRM, lambda s,f: exit("TIMEOUT"))
    signal.alarm(second)

start = time.time()      # 开始计时
timeout_handler(MAX_TIME)

# ---控制台输出---
status_str = ["SUCCESS","FAILED","RETRY","SKIPPED"]  # 定义任务的四种状态
final_state = {"Init":None,"Navigate":None,"DetectQR":None,"Grasp":None,"AvoidObstacle":None, "Place":None,"ReturnHome":None}
current_state = {"Init":None,"Navigate":None,"DetectQR":None,"Grasp":None,"AvoidObstacle":None, "Place":None,"ReturnHome":None}
# 定义任务的当前状态以及最终状态

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
    

task_graph = []
for t in dictionary["tasks"]:
    task_graph.append(t)

task_info_d = {}
for t in dictionary["tasks"]:
    task_info_d[t["name"]] = t["duration"]
    
task_info_s = {}
for t in dictionary["tasks"]:
    task_info_s[t["name"]] = t["success_rate"]
    
adj_graph = {}
for t in task_graph:
    task_name = t["name"]  
    adj_graph[task_name] = []
    dep_list = t["dependencies"]
    for d in dep_list:
        adj_graph[d].append(task_name)
print(adj_graph)

             
# 计算有向无环图的入度
nodes = set()
value = tuple()
for k in task_graph:
    nodes.add(k["name"])
    value = k["dependencies"]
    if not isinstance(value,list):
        value = [value]
    for v in value:
        nodes.add(v)

print("nodes里面的全部节点：",nodes)


indegree = {}
for n in nodes:
    indegree[n] = 0            
for k in task_graph:
    indegree[k["name"]] += len(k["dependencies"])

print("各节点入度：")
print(indegree)

report_data_list = []

# ---拓扑排序---
def task_sort():
    """
         该函数用于实现对文件任务的拓扑排序并按依赖顺序执行，生成一份依赖清单
    """
    global task_graph, task_info_d, task_info_s
    global indegree
    global report_data
    q = deque()
    result = []
    for node in indegree:
        if indegree[node] == 0:
            q.append(node)
    while q:
        e = q.popleft()
        report_data = {"name": None,
               "status": None,
               "attempts": None,
               "duration": None,
               "started_at": None,
               "ended_at": None}
        report_data["started_at"] = time.perf_counter()
        report_data["name"] = e
        result.append(e)
        if final_state[e] != "SKIPPED":
            attempt = 1
            while attempt <= 3:
                duration = task_info_d[e]
                time.sleep(duration)
                success_rate = task_info_s[e]
                test = random.choices(["SUCCESS","FAILED"], weights = [success_rate, 1-success_rate])[0]  
                # choice返回一个列表，因此要加下标返回单次结果
                print(f"任务{e}第{attempt}次尝试结果：",end = "")
                color_print(test)
                if test == "SUCCESS":
                    final_state[e] = "SUCCESS"
                    report_data["status"] = "SUCCESS"
                    report_data["attempts"] = attempt
                    report_data["ended_at"] = time.perf_counter()
                    report_data["duration"] = report_data["ended_at"] - report_data["started_at"]
                    break;
                else:
                    if attempt == 3:
                        print(f"三次都失败！",end = "")
                        color_print("SKIPPED")
                        final_state[e] = "SKIPPED"
                        report_data["status"] = "SKIPPED"
                        report_data["attempts"] = attempt
                        report_data["ended_at"] = time.perf_counter()
                        report_data["duration"] = report_data["ended_at"] - report_data["started_at"]
                        break
                attempt += 1
                current_state[e] = "RETRY"
                print(f"任务{e}:",end = "")
                color_print(current_state[e])
		        
                if final_state[e] == "SKIPPED":
                    for v in adj_graph[e]:
                        final_state[v] = "SKIPPED"
        else:
            report_data["status"] = "SKIPPED"
            report_data["attempts"] = 0
            report_data["ended_at"] = time.perf_counter()
            report_data["duration"] = report_data["ended_at"] - report_data["started_at"]
            
        for v in adj_graph[e]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
        
        report_data_list.append(report_data)
       
    if len(result) == len(indegree):         
        print(result)
    else:
        print("图有环，无法拓扑排序")

def create_file():
    """
         本函数的作用是生成报告文件
    """
    global total_time, report_data_list
    json_dict = {"timeout":None, "total_duration":None, "tasks":[]}
    if total_time < MAX_TIME:
        json_dict["timeout"] = "false"
    else:
        json_dict["timeout"] = "true"
    json_dict["total_duration"] = total_time
    json_dict["tasks"] = report_data_list
    json_str = json.dumps(json_dict, indent = 2, ensure_ascii = False)

    with open("report.json","w") as f:
        f.write(json_str)
    print(f"运行结果已保存到{f}中")
    

# ---函数执行---      
task_sort()
end = time.time()
total_time = end - start
print(f"共耗时 {total_time:.4f}秒")
try:
    create_file()
except Exception as e:
    print(f"创建文件发生异常，{e}")
