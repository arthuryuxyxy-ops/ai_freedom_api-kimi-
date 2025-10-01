#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
from bs4 import BeautifulSoup
import os


def extract_ai_reply(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    
    ai_reply_selectors = [
        '.segment-assistant .markdown-container',
        '.segment-assistant .markdown',
        '[class*="assistant"] .markdown',
        '.chat-content-item-assistant .markdown'
    ]
    
    for selector in ai_reply_selectors:
        ai_elements = soup.select(selector)
        if ai_elements:
            ai_element = ai_elements[-1]
            return ai_element.get_text(strip=False)

    ai_text_patterns = [
        r'Python.*是一种.*编程语言',
        r'核心特点',
        r'主要应用领域',
        r'版本与兼容性',
        r'入门示例',
        r'学习资源'
    ]
    
    for pattern in ai_text_patterns:
        elements = soup.find_all(text=re.compile(pattern, re.IGNORECASE))
        if elements:
            for element in elements:
                parent = element.parent
                while parent:
                    if parent.name in ['div', 'section', 'article']:
                        text_content = parent.get_text(strip=False)
                        if any(pattern in text_content for pattern in ai_text_patterns):
                            return text_content
                    parent = parent.parent
    

    user_messages = soup.find_all(class_=re.compile(r'user|user-content'))
    if user_messages:

        last_user_msg = user_messages[-1]
        next_elements = last_user_msg.find_next_siblings(class_=re.compile(r'assistant|ai|bot'))
        if next_elements:
            return next_elements[0].get_text(strip=False)
    

    python_intro_pattern = r'(Python.*是一种.*?编程语言.*?)(?=\<|$)'
    match = re.search(python_intro_pattern, html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    
    return None


def clean_text(text):

    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'<[^>]+>', '', text)
    
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    text = text.strip()
    
    return text


def main():
    """
    主函数
    """
    try:
        if not os.path.exists('webpage.html'):
            print("错误: webpage.html 文件不存在")
            return
        
        with open('webpage.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("正在提取AI回复...")
        
        ai_reply = extract_ai_reply(html_content)
        
        if ai_reply:
            cleaned_reply = clean_text(ai_reply)
            
            with open('ans.txt', 'w', encoding='utf-8') as f:
                f.write(cleaned_reply)
            
            print(f"成功提取AI回复并保存到 ans.txt")
            print(f"回复长度: {len(cleaned_reply)} 字符")
            
            preview = cleaned_reply[:200] + "..." if len(cleaned_reply) > 200 else cleaned_reply
            print(f"回复预览: {preview}")
        else:
            print("警告: 未能找到AI回复")
            with open('ans.txt', 'w', encoding='utf-8') as f:
                f.write("")
            print("已创建空的 ans.txt 文件")
            
    except Exception as e:
        print(f"错误: {str(e)}")
        try:
            with open('ans.txt', 'w', encoding='utf-8') as f:
                f.write("")
        except:
            pass


if __name__ == "__main__":
    main()
