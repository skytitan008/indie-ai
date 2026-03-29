#!/usr/bin/env python3
"""
学习 10 大编程语言 - 快速版

使用内置知识库，不依赖网络搜索
"""

import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI


# 10 大编程语言核心知识
PROGRAMMING_KNOWLEDGE = {
    'C': {
        'description': 'C 语言 - 系统编程基础',
        'topics': {
            '基础语法': '''
C 语言基础：
- 数据类型：int, float, double, char, void
- 控制结构：if/else, for, while, switch
- 函数定义：return_type function_name(params) { body }
- 指针：*ptr 指向变量地址，&var 取地址
- 数组：int arr[10] 声明数组
            ''',
            '内存管理': '''
内存管理：
- malloc(size) - 分配内存
- free(ptr) - 释放内存
- calloc(n, size) - 分配并初始化
- realloc(ptr, new_size) - 重新分配
            ''',
            '数据结构': '''
常用数据结构：
- 链表：struct Node { int data; struct Node* next; }
- 栈：LIFO，push/pop 操作
- 队列：FIFO，enqueue/dequeue
- 树：二叉树、BST、AVL
            ''',
            '文件 I/O': '''
文件操作：
- fopen(filename, mode) - 打开文件
- fclose(fp) - 关闭文件
- fread/fwrite - 读写
- fprintf/fscanf - 格式化读写
            ''',
            '最佳实践': '''
编码规范：
- 使用有意义的变量名
- 添加注释说明复杂逻辑
- 检查返回值和错误
- 避免内存泄漏
- 使用 const 保护不变数据
            '''
        }
    },
    'Python': {
        'description': 'Python - 通用编程语言',
        'topics': {
            '高级特性': '''
Python 高级特性：
- 装饰器：@decorator 修饰函数
- 生成器：yield 返回迭代器
- 上下文管理器：with statement
- 列表推导：[x*2 for x in range(10)]
- 多继承：class Child(Parent1, Parent2)
            ''',
            '异步编程': '''
Async/Await：
- async def func(): 定义协程
- await coro() 等待协程
- asyncio.run(main()) 运行
- async with/for 异步上下文
            ''',
            '数据科学': '''
数据科学生态：
- NumPy：数值计算
- Pandas：数据处理
- Matplotlib：数据可视化
- Scikit-learn：机器学习
- Jupyter：交互式 notebook
            ''',
            'Web 开发': '''
Web 框架：
- Flask：轻量级框架
- Django：全功能框架
- FastAPI：现代 API 框架
- asyncio + aiohttp：异步 Web
            ''',
            '最佳实践': '''
PEP8 规范：
- 4 空格缩进
- 行宽不超过 79 字符
- 函数和类之间空两行
- 使用类型注解
- 编写 docstring
            '''
        }
    },
    'Java': {
        'description': 'Java - 企业级应用',
        'topics': {
            '面向对象': '''
OOP 四大特性：
- 封装：private 字段，public 方法
- 继承：extends 关键字
- 多态：父类引用指向子类对象
- 抽象：abstract class/interface
            ''',
            '集合框架': '''
常用集合：
- List: ArrayList, LinkedList
- Set: HashSet, TreeSet
- Map: HashMap, TreeMap
- Queue: PriorityQueue, LinkedList
            ''',
            '并发编程': '''
多线程：
- Thread 类，Runnable 接口
- synchronized 同步
- volatile 可见性
- ConcurrentHashMap 并发集合
- ExecutorService 线程池
            ''',
            'Spring 框架': '''
Spring 核心：
- IoC 容器：依赖注入
- AOP：面向切面编程
- Spring Boot：快速开发
- Spring MVC：Web 框架
- Spring Data：数据访问
            ''',
            '设计模式': '''
常用模式：
- Singleton：单例
- Factory：工厂
- Observer：观察者
- Strategy：策略
- Builder：构建器
            '''
        }
    },
    'JavaScript': {
        'description': 'JavaScript - Web 开发',
        'topics': {
            'ES6 特性': '''
ES6+ 新特性：
- let/const 块级作用域
- 箭头函数：() => {}
- 模板字符串：`Hello ${name}`
- 解构赋值：const {a, b} = obj
- 展开运算符：...array
            ''',
            '异步编程': '''
异步处理：
- Promise：then/catch
- async/await：同步写法
- fetch：HTTP 请求
- Promise.all：并发处理
            ''',
            'DOM 操作': '''
DOM API：
- document.getElementById()
- document.querySelector()
- element.addEventListener()
- element.innerHTML/textContent
- element.classList.add/remove
            ''',
            'Node.js': '''
Node.js 后端：
- Express：Web 框架
- fs：文件系统
- http：HTTP 服务器
- path：路径处理
- npm：包管理
            ''',
            '框架': '''
主流框架：
- React：组件化 UI
- Vue：渐进式框架
- Angular：完整解决方案
- Next.js：React SSR
- Nuxt.js：Vue SSR
            '''
        }
    },
    'C++': {
        'description': 'C++ - 高性能编程',
        'topics': {
            '面向对象': '''
C++ OOP：
- class/struct 类定义
- 构造函数/析构函数
- 继承：public/protected/private
- 多态：virtual 函数
- 纯虚函数：= 0
            ''',
            '模板': '''
泛型编程：
- template<typename T>
- 函数模板
- 类模板
- 模板特化
- 变长模板参数
            ''',
            'STL': '''
标准库：
- vector：动态数组
- map/unordered_map：映射
- set/unordered_set：集合
- algorithm：排序查找
- iterator：迭代器
            ''',
            '智能指针': '''
内存安全：
- unique_ptr：独占所有权
- shared_ptr：共享所有权
- weak_ptr：弱引用
- make_unique/make_shared
            ''',
            '现代特性': '''
C++17/20：
- auto 类型推导
- range-based for
- structured binding
- concepts (C++20)
- modules (C++20)
            '''
        }
    },
    'Go': {
        'description': 'Go - 云原生语言',
        'topics': {
            '基础语法': '''
Go 基础：
- var name type 变量声明
- func name(params) returns 函数
- if/else, for, switch
- := 短变量声明
- defer 延迟执行
            ''',
            '并发': '''
Goroutine 和 Channel：
- go func() 启动协程
- ch := make(chan T) 创建通道
- ch <- value 发送
- value := <-ch 接收
- select 多路复用
            ''',
            'Web 开发': '''
Web 编程：
- net/http 标准库
- Gin 框架
- Echo 框架
- JSON 编解码
- RESTful API
            ''',
            '微服务': '''
微服务架构：
- gRPC：RPC 框架
- Protocol Buffers
- 服务发现
- 负载均衡
- 链路追踪
            ''',
            '最佳实践': '''
Go 规范：
- go fmt 格式化
- go mod 模块管理
- 错误处理：if err != nil
- 简洁优于复杂
- 组合优于继承
            '''
        }
    },
    'Rust': {
        'description': 'Rust - 内存安全系统语言',
        'topics': {
            '所有权': '''
所有权系统：
- 每个值有一个所有者
- 移动语义：move
- 借用：&T 不可变，&mut T 可变
- 作用域结束自动 drop
            ''',
            '内存安全': '''
内存安全保证：
- 编译时检查借用
- 无数据竞争
- 无空指针
- 无未初始化内存
- 零成本抽象
            ''',
            '异步编程': '''
Async Rust：
- async fn 异步函数
- .await 等待
- Future trait
- tokio 运行时
- async/await 语法
            ''',
            'Web 开发': '''
Web 框架：
- Actix-web
- Rocket
- Warp
- Axum
- serde JSON 序列化
            ''',
            '系统编程': '''
系统级特性：
- 直接内存操作
- FFI 调用 C 代码
- 嵌入式开发
- 操作系统开发
- 高性能网络
            '''
        }
    },
    'TypeScript': {
        'description': 'TypeScript - 类型化 JavaScript',
        'topics': {
            '类型系统': '''
基础类型：
- string, number, boolean
- array: T[]
- tuple: [string, number]
- enum：枚举
- any/unknown/never
            ''',
            '高级类型': '''
高级特性：
- interface：接口
- type：类型别名
- 泛型：<T>
- 联合类型：A | B
- 交叉类型：A & B
            ''',
            'React': '''
TS + React：
- React.FC<Props>
- useState<T>
- useEffect
- 类型安全的 props
- 事件类型处理
            ''',
            'Node.js': '''
后端开发：
- Express + TS
- NestJS 框架
- 类型安全的 API
- 数据库 ORM
- JWT 认证
            ''',
            '最佳实践': '''
编码规范：
- 严格模式：strict: true
- 避免 any
- 使用接口定义结构
- 类型推断优先
- 生成声明文件
            '''
        }
    },
    'C#': {
        'description': 'C# - 微软生态',
        'topics': {
            '面向对象': '''
C# OOP：
- class/struct
- 属性：get/set
- 索引器
- 事件和委托
- LINQ 查询
            ''',
            'LINQ': '''
语言集成查询：
- from x in collection
- where 条件
- select 投影
- orderby 排序
- groupby 分组
            ''',
            '异步': '''
Async/Await：
- async Task<T>
- await 关键字
- Task.Run
- CancellationToken
- async stream
            ''',
            '.NET': '''
.NET 生态：
- .NET Core / .NET 5+
- ASP.NET Core Web
- Entity Framework
- Blazor WebAssembly
- MAUI 跨平台
            ''',
            'Unity': '''
游戏开发：
- MonoBehaviour
- Component 系统
- Physics 物理
- Animation 动画
- Shader 着色器
            '''
        }
    },
    'Ruby': {
        'description': 'Ruby - 优雅简洁',
        'topics': {
            '基础语法': '''
Ruby 基础：
- 动态类型
- 一切皆对象
- 块：{ } 或 do/end
- 符号：:symbol
- 插值："#{var}"
            ''',
            '面向对象': '''
OOP 特性：
- class 定义
- attr_accessor
- 继承：< Parent
- mixin：include Module
- 元编程
            ''',
            'Rails': '''
Ruby on Rails：
- MVC 架构
- ActiveRecord ORM
- 路由配置
- 视图模板 ERB
- 迁移数据库
            ''',
            '元编程': '''
元编程技术：
- define_method
- method_missing
- eval
- class_eval
- 动态方法调用
            ''',
            '最佳实践': '''
Ruby 规范：
- 约定优于配置
- DRY 原则
- 简洁优雅
- 测试驱动
- Ruby Style Guide
            '''
        }
    }
}


def learn_all_languages(ai: AutonomousAI):
    """学习所有编程语言"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         📚 学习 10 大编程语言                           ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    total_topics = sum(len(lang['topics']) for lang in PROGRAMMING_KNOWLEDGE.values())
    learned = 0
    
    for lang, info in PROGRAMMING_KNOWLEDGE.items():
        print(f"\n{'='*60}")
        print(f"📖 学习：{lang} - {info['description']}")
        print(f"{'='*60}\n")
        
        for topic_name, content in info['topics'].items():
            learned += 1
            print(f"[{learned}/{total_topics}] {topic_name}")
            
            # 存储知识到数据库
            ai.learner.knowledge_base.store_knowledge(
                topic=f"{lang}_{topic_name}",
                content={'content': content, 'language': lang},
                category="programming",
                tags=[lang.lower(), 'programming', topic_name]
            )
            
            time.sleep(0.1)  # 短暂延迟
        
        print(f"\n✅ {lang} 学习完成！")


def main():
    """主函数"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎓 AI 学习 10 大编程语言 (快速版)              ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    
    # 初始化
    ai.initialize()
    
    # 学习编程语言
    print("\n开始学习 10 大编程语言...\n")
    
    start_time = time.time()
    learn_all_languages(ai)
    elapsed = time.time() - start_time
    
    # 显示状态
    print("\n")
    ai.show_status()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 编程语言学习完成！                          ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print(f"⏱️  用时：{elapsed:.1f}秒")
    print("\n现在小七可以:")
    print("   ✅ 理解 10 大编程语言")
    print("   ✅ 帮你写代码")
    print("   ✅ 代码审查和优化")
    print("   ✅ 生成测试用例")
    print("   ✅ 编写文档")
    
    print("\n💬 输入 'chat' 开始聊天，输入 'quit' 退出\n")
    
    while True:
        try:
            cmd = input("命令：").strip().lower()
            
            if cmd in ['quit', 'exit', 'q']:
                print("小七：再见！👋")
                break
            elif cmd == 'chat':
                ai.start_chat()
            elif cmd == 'status':
                ai.show_status()
            else:
                # 直接聊天
                response = ai.chat(cmd)
                print(f"小七：{response}\n")
        except KeyboardInterrupt:
            print("\n小七：再见！👋")
            break


if __name__ == '__main__':
    main()
