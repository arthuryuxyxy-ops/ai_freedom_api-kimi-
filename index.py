import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

loop = 0
url = "https://www.kimi.com/chat/"
response = requests.get(url)
html_content = response.text

while loop != 10:
    if response.status_code == 200:
       print("连接成功，状态码：200")
       with open('webpage.html','w',encoding='utf-8') as file:
          file.write(html_content)
       break
    else:
       print(f"请求失败")
       loop = loop + 1
os.system('python api_free.py')