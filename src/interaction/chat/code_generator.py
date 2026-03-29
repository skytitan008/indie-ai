#!/usr/bin/env python3
"""
代码生成器

根据用户需求自动生成代码
"""

import sqlite3
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent


# 代码模板库
CODE_TEMPLATES = {
    'python': {
        'quick_sort': '''def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)''',
        
        'hello_world': '''print("Hello, World!")''',
        
        'http_server': '''from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print("Server running at http://localhost:8000")
server.serve_forever()''',
        
        'file_read': '''with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)''',
        
        'class_example': '''class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, I'm {self.name}"''',
    },
    
    'c': {
        'hello_world': '''#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}''',
        
        'linked_list': '''#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* create_node(int data) {
    struct Node* node = malloc(sizeof(struct Node));
    node->data = data;
    node->next = NULL;
    return node;
}''',
        
        'file_read': '''#include <stdio.h>

int main() {
    FILE* fp = fopen("file.txt", "r");
    char buffer[1024];
    fgets(buffer, sizeof(buffer), fp);
    printf("%s\\n", buffer);
    fclose(fp);
    return 0;
}''',
    },
    
    'javascript': {
        'hello_world': '''console.log("Hello, World!");''',
        
        'function': '''function greet(name) {
    return `Hello, ${name}!`;
}

// 或箭头函数
const greet = (name) => `Hello, ${name}!`;''',
        
        'async_await': '''async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}''',
        
        'class': '''class Person {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Hello, I'm ${this.name}`;
    }
}''',
    },
    
    'java': {
        'hello_world': '''public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
        
        'class_example': '''public class Person {
    private String name;
    
    public Person(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}''',
    },
    
    'cpp': {
        'hello_world': '''#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}''',
        
        'vector_example': '''#include <vector>
#include <iostream>

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5};
    for (int n : nums) {
        std::cout << n << " ";
    }
    return 0;
}''',
    },
    
    'go': {
        'hello_world': '''package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}''',
        
        'goroutine': '''package main

import (
    "fmt"
    "time"
)

func say(msg string) {
    fmt.Println(msg)
}

func main() {
    go say("hello")
    time.Sleep(time.Second)
}''',
    },
    
    'rust': {
        'hello_world': '''fn main() {
    println!("Hello, World!");
}''',
        
        'ownership': '''fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // 所有权转移
    println!("{}", s2);
}''',
    },
}


class CodeGenerator:
    """代码生成器"""
    
    def __init__(self):
        self.templates = CODE_TEMPLATES
    
    def generate(self, language: str, task: str) -> Optional[str]:
        """生成代码"""
        lang = language.lower()
        task_lower = task.lower()
        
        if lang not in self.templates:
            return None
        
        # 匹配任务 - 更灵活的匹配
        task_map = {
            'quick': 'quick_sort',
            'sort': 'quick_sort',
            '排序': 'quick_sort',
            'hello': 'hello_world',
            'world': 'hello_world',
            'function': 'function',
            '函数': 'function',
            'http': 'http_server',
            'server': 'http_server',
            'file': 'file_read',
            'read': 'file_read',
            'class': 'class_example',
            '类': 'class_example',
            'async': 'async_await',
            'await': 'async_await',
            'linked': 'linked_list',
            'list': 'linked_list',
            '链表': 'linked_list',
            'vector': 'vector_example',
            'goroutine': 'goroutine',
            'ownership': 'ownership',
        }
        
        for keyword, template_key in task_map.items():
            if keyword in task_lower:
                code = self.templates[lang].get(template_key)
                if code:
                    return code
        
        # 默认返回 hello world
        return self.templates[lang].get('hello_world')
    
    def get_supported_languages(self) -> list:
        """获取支持的语言"""
        return list(self.templates.keys())


# 集成到 AI 系统
def enhance_chat_with_coding(chat_bot):
    """增强聊天机器人的编程能力"""
    original_chat = chat_bot.chat
    
    code_gen = CodeGenerator()
    
    def enhanced_chat(text: str) -> str:
        # 检测编程相关请求
        programming_keywords = ['写代码', '写个', '代码', 'function', 'code', 'program']
        
        if any(kw in text.lower() for kw in programming_keywords):
            # 检测语言
            languages = ['python', 'c', 'java', 'javascript', 'cpp', 'go', 'rust', 'typescript', 'c#', 'ruby']
            detected_lang = None
            
            for lang in languages:
                if lang in text.lower():
                    detected_lang = lang
                    break
            
            if detected_lang:
                code = code_gen.generate(detected_lang, text)
                if code:
                    return f"好的！这是{detected_lang.capitalize()}代码：\n\n```{detected_lang}\n{code}\n```\n\n需要我解释一下吗？"
        
        return original_chat(text)
    
    chat_bot.chat = enhanced_chat
    return chat_bot


if __name__ == '__main__':
    # 测试
    gen = CodeGenerator()
    
    print("支持的語言:", gen.get_supported_languages())
    print("\nPython 快速排序:")
    print(gen.generate('python', 'quick sort'))
    print("\nC Hello World:")
    print(gen.generate('c', 'hello world'))
    print("\nJavaScript 函数:")
    print(gen.generate('javascript', 'function'))
