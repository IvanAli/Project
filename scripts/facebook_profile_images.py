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
import urllib.request

# Read the friendship graph
graph_data = open("facebook_names.json")
facebook_friends = json.load(graph_data)

total = len(facebook_friends)
iteration = 0

def get_image(key, value):
  image_link = value["image"]
  urllib.request.urlretrieve(image_link, "profile_images/" + key + ".jpg")
  global iteration
  print_progress_bar(iteration + 1, total)
  iteration += 1

Parallel(n_jobs=-1)(delayed(get_image)(key, value) for key, value in facebook_friends.items())
