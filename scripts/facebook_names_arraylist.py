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

def save_json(graph, name):
  print("Saving " + name)
  with open(name, 'w') as json_file:
    json.dump(graph, json_file, ensure_ascii=False)
 
save_json(names, "all_names.json") 
