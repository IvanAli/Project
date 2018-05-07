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
from bs4 import BeautifulSoup

# Read the friendship graph
graph_data = open("facebook_names.json")
facebook_friends = json.load(graph_data)

total = 0

for key, value in facebook_friends.items():
  total += 1

finished = 0

missing_graph = {}

names = [key for key in facebook_friends]
ids = {key:i for i, key in enumerate(facebook_friends)}


def get_friend_list(my_name):
  ret = []
  try:
    html_file = open('./htmls/' + my_name + '.html')
    soup = BeautifulSoup(html_file)
    friends = soup.select('div[data-testid="friend_list_item"]')
    my_id = ids[my_name]
    for friend in friends:
      # profile_div_obj = friend.select('div[class="fsl fwb fcb"]')
      find_all_list = friend.find_all("div", class_="fsl fwb fcb")
      if not find_all_list:
        continue
      profile_div_obj = find_all_list[0]
      profile_link_obj = profile_div_obj.find_all('a')[0]
      friend_name = profile_link_obj.string
      if friend_name == None:
        continue
      friend_name = friend_name.strip()
      # print("friend is %s" % friend_name)
      if friend_name not in facebook_friends:
        continue
      ret.append(ids[friend_name])
  except IOError:
    pass
    import random
    how_many = random.randint(1, 7)
    friends_numbers = [random.randint(0, len(names) - 1) for x in range(how_many)]
    my_id = ids[my_name]
    for friend_id in friends_numbers:
      if friend_id == my_id:
        continue
      friend_name = names[friend_id]
      ret.append(friend_id)
      # facebook_friends[friend_name]["friends"].add(key)
    """
    print(my_name + '.html does not exist')
    missing_graph[my_name] = {"image": facebook_friends[my_name]["image"], "friends_link": facebook_friends[my_name]["friends_link"]}
    print(missing_graph[my_name])
    """
    pass
  global finished
  print_progress_bar(finished + 1, total)
  finished += 1
  return ret

def save_json(graph, name):
  print("saving json file")
  with open(name, 'w') as json_file:
    json.dump(graph, json_file, ensure_ascii=False)
                      

def get_users_with_friends(chunk):
  ret = []
  for key, value in chunk.items():
    user_obj = {"image": value["image"], "friends": get_friend_list(key)}
    ret.append((ids[key], user_obj))
  return ret

from itertools import islice 
# Get chunks
def chunks(data, SIZE):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k:data[k] for k in islice(it, SIZE)}


users_chunks = chunks(facebook_friends, 150)

# Visit everyone's friends list (in parallel)
users = Parallel(n_jobs=-1)(delayed(get_users_with_friends)(chunk) for chunk in users_chunks) 
users = [j for i in users for j in i]
graph = {}
"""
for i in range(len(users)):
  print(names[i])
  print(ids[names[i]])
"""

for name_id, obj in users:
  graph[name_id] = {}
  graph[name_id]["name"] = names[name_id]
  graph[name_id]["friends"] = set()
  graph[name_id]["photo_filename"] = names[name_id] + ".jpg"

for name_id, obj in users:
  for friend_id in obj["friends"]:
    # print("%d and %d are friends" % name_id, friend_id)
    graph[name_id]["friends"].add(friend_id)
    graph[friend_id]["friends"].add(name_id)

print(missing_graph)

for key, value in graph.items():
  value["friends"] = list(value["friends"])
  # value["friends"] = [names[x] for x in value["friends"]]

save_json(graph, "facebook_graph.json") 
save_json(missing_graph, "facebook_missing.json")
