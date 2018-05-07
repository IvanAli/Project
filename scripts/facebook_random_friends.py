from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from collections import defaultdict
import time
import json
from selenium.webdriver.firefox.options import Options
from joblib import Parallel, delayed
import codecs
from progress_bar import print_progress_bar
import random

# Read the friendship graph
graph_data = open("facebook_names.json")
facebook_friends = json.load(graph_data)


names = [key for key in facebook_friends]
ids = {key:i for i, key in enumerate(facebook_friends)}

"""
for i in range(30):
  print(names[i])
  print(ids[names[i]])
exit(0)
"""

for key, value in facebook_friends.items():
  value["friends"] = set()
  del value["friends_link"]
  facebook_friends[key]["id"] = ids[key]

for key in facebook_friends:
  this_id = ids[key]
  how_many = random.randint(1, 20)
  friends_numbers = [random.randint(0, len(names) - 1) for x in range(how_many)]
  for friend_id in friends_numbers:
    if friend_id == this_id:
      continue
    friend_name = names[friend_id]
    facebook_friends[key]["friends"].add(friend_name)
    facebook_friends[friend_name]["friends"].add(key)

   
def save_json(graph):
  print("saving json file")
  with open('facebook_friends.json', 'w') as json_file:
    json.dump(graph, json_file, ensure_ascii=False)
 
for key, value in facebook_friends.items():
  value["friends"] = list(value["friends"])

save_json(facebook_friends) 
