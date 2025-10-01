from playwright.sync_api import sync_playwright
import time
import os

def use_saved_state():
    with sync_playwright() as p:

        if not os.path.exists("auth_state.json"):
            print("没有找到保存的登录状态，请先运行登录函数")
            return
        
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="auth_state.json")
        page = context.new_page()
        
        page.goto('https://www.kimi.com/')
        print("已使用保存的登录状态打开网站")
        
        page.wait_for_timeout(5000)
        
        try:
            user_element = page.query_selector(".user-info, [class*='avatar'], [class*='user']")
            if user_element:
                print("已成功使用保存的登录状态")
            else:
                print("登录状态可能已过期，需要重新登录")

        except:
            print("无法确定登录状态")
        
        try:
            with open("que.txt", "r", encoding="utf-8") as f:
                question = f.read().strip()
            if not question:
                print("que.txt 文件为空，请输入问题内容")
                browser.close()
                return
        except FileNotFoundError:
            print("que.txt 文件不存在")
            browser.close()
            return
        
        print(f"从 que.txt 读取的问题: {question}")
        
        print("正在寻找输入框...")
        
        input_selectors = [
            "textarea",
            "input[type='text']",
            "input[placeholder*='输入']",
            "input[placeholder*='问']",
            "[contenteditable='true']",
            ".input-box",
            ".chat-input",
            ".message-input",
            "[class*='input']",
            "[class*='textarea']"
        ]
        
        input_element = None
        for selector in input_selectors:
            input_element = page.query_selector(selector)
            if input_element:
                print(f"找到输入框，选择器: {selector}")
                break
        
        if not input_element:
            print("未找到输入框，请手动检查页面结构")
            browser.close()
            return
        
        print("正在输入问题...")
        input_element.click()
        input_element.fill("")
        input_element.type(question, delay=100)

        print("正在发送消息...")
        input_element.press("Enter")

        print("等待回复开始...")
        page.wait_for_timeout(3000)

        print("等待回复完成...")
        max_wait_time = 120
        wait_interval = 2
        waited_time = 0
        
        last_content = ""
        same_content_count = 0
        
        while waited_time < max_wait_time:
            current_html = page.content()

            if current_html == last_content:
                same_content_count += 1
            else:
                same_content_count = 0
                last_content = current_html

            if same_content_count >= 3:
                print("回复已完成")
                break
            
            print(f"等待回复中... ({waited_time}/{max_wait_time}秒)")
            page.wait_for_timeout(wait_interval * 1000)
            waited_time += wait_interval
            
        print("正在保存网页内容到 webpage.html...")
        final_html = page.content()
        with open("webpage.html", "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print("网页内容已保存到 webpage.html")
        
        browser.close()

if __name__ == "__main__":
    use_saved_state()

    os.system("python extract_reply.py")
