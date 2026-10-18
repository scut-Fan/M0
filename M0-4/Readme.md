                                   # ---参数说明---
#1.文件读取与任务图设计
dictionary: 字典，读取文件里的内容并存储到该字典
READ_FILE: 字符串，代表要读取的文件名
MAX_TIME: 用户设定的执行时长，一般是文件里的"timeout"，超出会退出程序
status_str: 列表，含"success""failed""retry""skipped"四种状态
current_state: 列表，记录任务当前处于哪一状态
final_state: 列表，记录任务的最终状态("success" or "skipped")
task_graph: 列表，只存储了文件里的"tasks"列表
task_info_d: 字典，键为文件"tasks"里的"name"，值为"duration"，用于定向查找某任务所需时间
task_info_s: 字典，键为文件"tasks"里的"name"，值为"success_rate"，用于定向查找某任务成功率
adj_graph: 字典，键为文件"tasks"里的"dependencies"，值为"name"，将依赖关系反过来

#2.图与入度
nodes: 集合，存储任务图中的所有节点
value: 元组，任务图里的["dependencies"]
indegree: 字典，计算任务图各节点的入度
report_data: 字典，按照report.json文件中的tasks列表中每一个字典的格式设置
report_data_list: 列表，在执行任务时每个任务会记录到report_data中，该列表用于追加该字典

#3.拓扑排序与模拟执行
result: 列表，每个元素出队列时被追加到该列表，用它的长度与入度中元素个数比较来判断有无依赖环
test: 临时变量，记录任务的一次模拟执行的结果("success" or "failed")

#4.创建文件
json_dict: 按照给出的json文件示例编写的字典
total_time: 程序的结束时间减开始时间得到程序总耗时
json_str: 用json.dumps()将json_dict转化得来的字符串，方可直接写入json文件

                                  # ---运行实例---
#实例1
{'Init': ['Navigate'], 'Navigate': ['DetectQR', 'AvoidObstacle'], 'DetectQR': ['Grasp'], 'Grasp': ['Place'], 'AvoidObstacle': ['Place'], 'Place': ['ReturnHome'], 'ReturnHome': []}
nodes里面的全部节点： {'Init', 'DetectQR', 'Navigate', 'ReturnHome', 'Place', 'AvoidObstacle', 'Grasp'}
各节点入度：
{'Init': 0, 'DetectQR': 1, 'Navigate': 1, 'ReturnHome': 1, 'Place': 2, 'AvoidObstacle': 1, 'Grasp': 1}
任务Init第1次尝试结果：SUCCESS
任务Navigate第1次尝试结果：SUCCESS
任务DetectQR第1次尝试结果：SUCCESS
任务AvoidObstacle第1次尝试结果：SUCCESS
任务Grasp第1次尝试结果：SUCCESS
任务Place第1次尝试结果：SUCCESS
任务ReturnHome第1次尝试结果：SUCCESS
['Init', 'Navigate', 'DetectQR', 'AvoidObstacle', 'Grasp', 'Place', 'ReturnHome']
共耗时 11.0075秒
运行结果已保存到<_io.TextIOWrapper name='report.json' mode='w' encoding='UTF-8'>中

#实例2
{'Init': ['Navigate'], 'Navigate': ['DetectQR', 'AvoidObstacle'], 'DetectQR': ['Grasp'], 'Grasp': ['Place'], 'AvoidObstacle': ['Place'], 'Place': ['ReturnHome'], 'ReturnHome': []}
nodes里面的全部节点： {'DetectQR', 'Navigate', 'Place', 'AvoidObstacle', 'ReturnHome', 'Init', 'Grasp'}
各节点入度：
{'DetectQR': 1, 'Navigate': 1, 'Place': 2, 'AvoidObstacle': 1, 'ReturnHome': 1, 'Init': 0, 'Grasp': 1}
任务Init第1次尝试结果：SUCCESS
任务Navigate第1次尝试结果：FAILED
任务Navigate:RETRY
任务Navigate第2次尝试结果：SUCCESS
任务DetectQR第1次尝试结果：SUCCESS
任务AvoidObstacle第1次尝试结果：FAILED
任务AvoidObstacle:RETRY
任务AvoidObstacle第2次尝试结果：FAILED
任务AvoidObstacle:RETRY
任务AvoidObstacle第3次尝试结果：FAILED
三次都失败！SKIPPED
任务Grasp第1次尝试结果：SUCCESS
['Init', 'Navigate', 'DetectQR', 'AvoidObstacle', 'Grasp', 'Place', 'ReturnHome']
共耗时 14.0047秒
运行结果已保存到<_io.TextIOWrapper name='report.json' mode='w' encoding='UTF-8'>中

#实例3
{'Init': ['Navigate'], 'Navigate': ['DetectQR', 'AvoidObstacle'], 'DetectQR': ['Grasp'], 'Grasp': ['Place'], 'AvoidObstacle': ['Place'], 'Place': ['ReturnHome'], 'ReturnHome': []}
nodes里面的全部节点： {'Navigate', 'Place', 'AvoidObstacle', 'ReturnHome', 'DetectQR', 'Grasp', 'Init'}
各节点入度：
{'Navigate': 1, 'Place': 2, 'AvoidObstacle': 1, 'ReturnHome': 1, 'DetectQR': 1, 'Grasp': 1, 'Init': 0}
任务Init第1次尝试结果：SUCCESS
任务Navigate第1次尝试结果：SUCCESS
任务DetectQR第1次尝试结果：SUCCESS
任务AvoidObstacle第1次尝试结果：FAILED
任务AvoidObstacle:RETRY
任务AvoidObstacle第2次尝试结果：SUCCESS
任务Grasp第1次尝试结果：SUCCESS
任务Place第1次尝试结果：FAILED
任务Place:RETRY
任务Place第2次尝试结果：FAILED
任务Place:RETRY
任务Place第3次尝试结果：SUCCESS
TIMEOUT
