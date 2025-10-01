from playwright.sync_api import sync_playwright
import time
import os

def login_and_save_state():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto('https://www.kimi.com/')
        print("已打开网站")
        
        input("请手动完成登录，然后按回车键继续...")
        
        context.storage_state(path="auth_state.json")
        print("登录状态已保存")
        
    
    while True:
        time.sleep(1)
if __name__ == "__main__":
    login_and_save_state()