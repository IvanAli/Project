from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from collections import defaultdict
import time
import json
from selenium.webdriver.firefox.options import Options

my_username = "ivan.alisv"
my_password = "bambinito123"

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options, executable_path="/home/ivan/Documents/ITESM/10th/ProjectMobile/geckodriver")
fp = webdriver.FirefoxProfile()
fp.DEFAULT_PREFERENCES['frozen']["dom.webnotifications.enabled"] = False
fp.DEFAULT_PREFERENCES['frozen']["dom.webnotifications.serviceworker.enabled"] = False

# Print iterations progress
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
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

# Visit URL
login_url = "https://www.facebook.com/login"
members_url = "https://www.facebook.com/groups/487833417915346/members"

# Login
driver.get(members_url)
email_input = driver.find_element_by_name("email")
email_input.send_keys(my_username)
pass_input = driver.find_element_by_name("pass");
pass_input.send_keys(my_password)
login_button = driver.find_element_by_name('login')
login_button.click()

# driver.get(members_url)

SCROLL_PAUSE_TIME = 1.5

time.sleep(SCROLL_PAUSE_TIME)
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

def save_json(graph):
  print("saving json file")
  with open('facebook_names.json', 'w') as json_file:
    json.dump(graph, json_file, ensure_ascii=False)

def work():
  person_class = "_60ri"
  users = driver.find_elements_by_css_selector('div[data-name="GroupProfileGridItem"]')

  facebook_users = {}

  for user in users:
    # print("user found")
    image_obj = user.find_element_by_tag_name("img")
    image_url = image_obj.get_attribute("src")
    profile_div_obj = user.find_element_by_class_name("_60ri")
    profile_link_obj = profile_div_obj.find_elements_by_tag_name("a")[0]
    link = profile_link_obj.get_attribute("href")
    friend_link = link.split("?")[0] + "/friends";
    user_obj = {}
    user_obj["image"] = image_url
    user_obj["friends_link"] = friend_link
    name = profile_link_obj.text
    if name not in facebook_users:
      facebook_users[name] = user_obj

  save_json(facebook_users)

iteration = 0
try:
  while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
      break
    last_height = new_height
    print_progress_bar(iteration + 1, 500)
    iteration += 1
except KeyboardInterrupt:
  print("Interruption detected")
  work()
  driver.close()
  exit(0)

work()
driver.close()