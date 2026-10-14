import time
import json

dictionary = {}

with open("tasks_demo.json", "r") as f:
    dictionary = json.load(f)
    
for k in dictionary.keys():
    print(k,dictionary[k])
