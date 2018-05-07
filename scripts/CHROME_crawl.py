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


# Print iterations progress
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█'):
  """
  Call in a loop to create terminal progress bar
  @params:
      iteration   - Required  : current iteration (Int)
      total       - Required  : total iterations (Int)
      prefix      - Optional  : prefix string (Str)
      suffix      - Optional  : suffix string (Str)
      decimals    - Optional  : positive number of decimals in percent complete (Int)
      length      - Optional  : character length of bar (Int)
      fill        - Optional  : bar fill character (Str)
  """
  percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
  filledLength = int(length * iteration // total)
  bar = fill * filledLength + '-' * (length - filledLength)
  print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
  # Print New Line on Complete
  if iteration == total: 
    print()

my_username = ""
my_password = ""

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("headless")
login_driver = webdriver.Chrome(chrome_options=options)

# Visit URL
login_url = "https://www.facebook.com/login"
members_url = "https://www.facebook.com/groups/487833417915346/members"

# Login
login_driver.get(login_url)
email_input = login_driver.find_element_by_name("email")
email_input.send_keys(my_username)
pass_input = login_driver.find_element_by_name("pass");
pass_input.send_keys(my_password)
login_button = login_driver.find_element_by_name('login')
login_button.click()

# Read the friendship graph
graph_data = open("facebook_classnames.json")
facebook_friends = json.load(graph_data)

people = set()

# Store login_driver's cookies
all_cookies = login_driver.get_cookies()


total = 0

for key, value in facebook_friends.items():
  total += 1

SCROLL_PAUSE_TIME = 1.1
time.sleep(SCROLL_PAUSE_TIME)

# Press escape to quit notification popup
webdriver.ActionChains(login_driver).send_keys(Keys.ESCAPE).perform()

login_driver.close()

finished = 0

def get_friend_list(my_name, new_driver):
  friends = new_driver.find_elements_by_css_selector('div[data-testid="friend_list_item"]')
  comma = False
  ret = []
  for friend in friends:
    try:
      profile_div_obj = friend.find_element_by_css_selector('div[class="fsl fwb fcb"]')
      profile_link_obj = profile_div_obj.find_elements_by_tag_name("a")[0]
      friend_name = profile_link_obj.text.strip()
      if friend_name not in facebook_friends:
        continue
      if comma:
        print(', ', end='')
      comma = True
      print(friend_name, end='')
      ret.append(friend_name)
    except:
      pass
  global finished
  print_progress_bar(finished + 1, total)
  finished += 1
  return ret

def save_json(graph):
  print("saving json file")
  with open('facebook_friends.json', 'w') as json_file:
    json.dump(graph, json_file, ensure_ascii=False)

def save_html(name, driver):
  with open('./htmls/' + name + '.html', 'w') as html_file:
    html_file.write(driver.page_source)

# Add field for friends
for key, value in facebook_friends.items():
  value["friends"] = []

import os.path

def get_users_with_friends(chunk):
  # new_driver = webdriver.Chrome(chrome_options=options)
  new_driver = webdriver.Chrome(chrome_options=options)
  new_driver.get("https://www.facebook.com/")
  for cookie in all_cookies:
    new_driver.add_cookie(cookie)
  ret = []
  global finished
  for key, value in chunk.items():
    # Get this user's friends list URL
    if os.path.exists('./htmls/' + key + '.html'):
      print_progress_bar(finished + 1, total)
      finished += 1
      print("continuing")
      continue
    friends_link = value["friends_link"] 
    new_driver.get(friends_link)
    current_url = new_driver.current_url
    if "atorrestoledo" in current_url:
      continue
    try:
      # Press escape to quit notification popup
      webdriver.ActionChains(new_driver).send_keys(Keys.ESCAPE).perform()
      # Scroll down until you reach the bottom
      # Get scroll height
      last_height = new_driver.execute_script("return document.body.scrollHeight")
      time.sleep(SCROLL_PAUSE_TIME)
      while True:
        new_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = new_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
          break
        last_height = new_height
        """
        try:
          new_driver.find_element_by_id("medley_header_photos")
          break
        except:
          pass
        try:
          new_driver.find_elements_by_xpath("//*[contains(text(), 'More About')]")
          break
        except:
          pass
        try:
          new_driver.find_element_by_id("medley_header_music")
          break
        except:
          pass
        try:
          new_driver.find_element_by_id("medley_header_sports")
          break
        except:
          pass
        try:
          new_driver.find_element_by_id("medley_header_books")
          break
        except:
          pass
        try:
          new_driver.find_element_by_id("medley_header_likes")
          break
        except:
          pass
        try:
          new_driver.find_element_by_id("medley_header_map")
          break
        except:
          pass
       """
      # save_html(key, new_driver)
      time.sleep(SCROLL_PAUSE_TIME)
      web_page = new_driver.execute_script("return document.body.innerHTML")
      with open('./htmls/' + key + '.html', 'w') as html_file:
        html_file.write(web_page)
      print_progress_bar(finished + 1, total)
      finished += 1
    except:
      pass
  new_driver.close()

from itertools import islice 
# Get chunks
def chunks(data, SIZE):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k:data[k] for k in islice(it, SIZE)}


print("Starting friends extractor...")

users_chunks = chunks(facebook_friends, 7000)

# Visit everyone's friends list (in parallel)
Parallel(n_jobs=-1)(delayed(get_users_with_friends)(chunk) for chunk in users_chunks) 

login_driver.close()
