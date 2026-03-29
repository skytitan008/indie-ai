#!/usr/bin/env python3
"""
自主学习核心模块

让 AI 能够：
- 自主上网搜索学习
- 提取并存储知识
- 下载新技能
- 自我扩展能力
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class KnowledgeBase:
    """知识库 - 存储 AI 学到的所有内容"""
    
    def __init__(self, db_path: str = "ai_memory.db"):
        self.db_path = PROJECT_ROOT / db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 知识表
        c.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                title TEXT,
                content TEXT,
                source_url TEXT,
                category TEXT,
                tags TEXT,
                confidence REAL DEFAULT 1.0,
                learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_count INTEGER DEFAULT 0,
                last_used_at TIMESTAMP
            )
        ''')
        
        # 技能表
        c.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                module_path TEXT,
                version TEXT,
                dependencies TEXT,
                installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                enabled INTEGER DEFAULT 1
            )
        ''')
        
        # 学习历史表
        c.execute('''
            CREATE TABLE IF NOT EXISTS learning_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                action TEXT,
                result TEXT,
                duration_seconds REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        c.execute('CREATE INDEX IF NOT EXISTS idx_topic ON knowledge(topic)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_category ON knowledge(category)')
        
        conn.commit()
        conn.close()
        print("✅ 知识库初始化完成")
    
    def store_knowledge(self, topic: str, content: Dict, source_url: str = "", 
                       category: str = "general", tags: List[str] = None):
        """存储知识"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO knowledge (topic, title, content, source_url, category, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            topic,
            content.get('title', ''),
            content.get('content', ''),
            source_url,
            category,
            json.dumps(tags if tags else [])
        ))
        
        conn.commit()
        conn.close()
        print(f"   📚 存储知识：{topic}")
    
    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索知识"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''
            SELECT * FROM knowledge 
            WHERE topic LIKE ? OR content LIKE ? OR tags LIKE ?
            ORDER BY learned_at DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
        
        results = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return results
    
    def register_skill(self, name: str, description: str, module_path: str,
                      version: str = "1.0.0", dependencies: List[str] = None):
        """注册新技能"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                INSERT OR REPLACE INTO skills 
                (name, description, module_path, version, dependencies)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                name,
                description,
                module_path,
                version,
                json.dumps(dependencies if dependencies else [])
            ))
            
            conn.commit()
            print(f"   🎯 注册技能：{name} v{version}")
        except sqlite3.IntegrityError:
            print(f"   ⚠️  技能已存在：{name}")
        finally:
            conn.close()
    
    def get_skills(self) -> List[Dict]:
        """获取所有技能"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM skills WHERE enabled = 1')
        skills = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return skills
    
    def log_learning(self, topic: str, action: str, result: str, duration: float):
        """记录学习历史"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO learning_history (topic, action, result, duration_seconds)
            VALUES (?, ?, ?, ?)
        ''', (topic, action, result, duration))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        stats = {}
        
        # 知识总量
        c.execute('SELECT COUNT(*) as count FROM knowledge')
        stats['total_knowledge'] = c.fetchone()['count']
        
        # 技能数量
        c.execute('SELECT COUNT(*) as count FROM skills WHERE enabled = 1')
        stats['total_skills'] = c.fetchone()['count']
        
        # 学习次数
        c.execute('SELECT COUNT(*) as count FROM learning_history')
        stats['total_learning_sessions'] = c.fetchone()['count']
        
        # 最近学习
        c.execute('''
            SELECT topic, action, timestamp 
            FROM learning_history 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        stats['recent_learning'] = [dict(row) for row in c.fetchall()]
        
        conn.close()
        return stats


class WebCrawler:
    """网页爬虫 - AI 的眼睛"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Indie AI Autonomous Learner)'
        })
        self.visited_urls = set()
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """抓取网页"""
        if url in self.visited_urls:
            return None
        
        try:
            print(f"   🕷️  抓取：{url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            self.visited_urls.add(url)
            return response.text
        except Exception as e:
            print(f"   ❌ 抓取失败：{e}")
            return None
    
    def extract_content(self, html: str, url: str = "") -> Dict:
        """从 HTML 提取结构化内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除无用标签
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # 提取标题
        title = ""
        if soup.title:
            title = soup.title.string
        else:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
        
        # 提取正文
        content_parts = []
        for tag in soup.find_all(['p', 'article', 'section']):
            text = tag.get_text(strip=True)
            if len(text) > 50:
                content_parts.append(text)
        
        # 提取代码块
        code_blocks = []
        for code in soup.find_all(['pre', 'code']):
            code_text = code.get_text(strip=True)
            if code_text:
                code_blocks.append(code_text)
        
        return {
            'title': title,
            'content': '\n\n'.join(content_parts[:10]),
            'code_snippets': code_blocks[:5],
            'source_url': url
        }
    
    def search_duckduckgo(self, query: str, num_results: int = 5) -> List[str]:
        """使用 DuckDuckGo 搜索"""
        print(f"   🔍 搜索：{query}")
        
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            html = self.fetch_page(search_url)
            
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            for result in soup.find_all('a', class_='result__url', limit=num_results):
                url = result.get('href')
                if url and url.startswith('http'):
                    results.append(url)
                    print(f"      找到：{url}")
            
            return results
        except Exception as e:
            print(f"   ❌ 搜索失败：{e}")
            return []
    
    def crawl_topic(self, query: str, max_pages: int = 5) -> List[Dict]:
        """搜索并抓取一个主题"""
        print(f"\n🔍 开始搜索：{query}")
        
        urls = self.search_duckduckgo(query, max_pages)
        
        if not urls:
            print("   ❌ 未找到结果")
            return []
        
        knowledge_list = []
        for url in urls:
            html = self.fetch_page(url)
            if html:
                content = self.extract_content(html, url)
                knowledge_list.append(content)
        
        print(f"   ✅ 抓取完成：{len(knowledge_list)} 页")
        return knowledge_list


class SkillDownloader:
    """技能下载器"""
    
    def __init__(self):
        self.skills_dir = PROJECT_ROOT / "src" / "skills"
        self.skills_dir.mkdir(exist_ok=True)
    
    def download_skill(self, name: str, code: str, description: str = ""):
        """下载并安装技能"""
        skill_path = self.skills_dir / f"{name}.py"
        
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"   📥 下载技能：{name}")
        print(f"      路径：{skill_path}")
        
        return str(skill_path)
    
    def create_skill_template(self, skill_name: str, functionality: str) -> str:
        """创建技能模板"""
        template = f'''#!/usr/bin/env python3
"""
{functionality}
自动生成时间：{datetime.now().isoformat()}
"""

class {skill_name.replace(" ", "").capitalize()}:
    """{functionality}"""
    
    def __init__(self):
        self.name = "{skill_name}"
        self.version = "1.0.0"
    
    def execute(self, *args, **kwargs):
        """执行技能"""
        print(f"🎯 执行技能：{{self.name}}")
        pass
    
    def get_info(self) -> dict:
        return {{
            'name': self.name,
            'version': self.version,
            'functionality': "{functionality}"
        }}


if __name__ == '__main__':
    skill = {skill_name.replace(" ", "").capitalize()}()
    skill.execute()
'''
        return template


class AutonomousLearner:
    """自主学习器"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.crawler = WebCrawler()
        self.skill_downloader = SkillDownloader()
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         🧠 自主学习器已激活                            ║")
        print("╚════════════════════════════════════════════════════════╝\n")
    
    def learn_topic(self, topic: str, max_pages: int = 5, category: str = "general"):
        """学习一个主题"""
        print(f"\n📚 开始学习：{topic}")
        start_time = datetime.now()
        
        knowledge_list = self.crawler.crawl_topic(topic, max_pages)
        
        if not knowledge_list:
            print(f"   ❌ 未找到关于 '{topic}' 的知识")
            return False
        
        for knowledge in knowledge_list:
            self.knowledge_base.store_knowledge(
                topic=topic,
                content=knowledge,
                source_url=knowledge.get('source_url', ''),
                category=category,
                tags=[topic]
            )
        
        duration = (datetime.now() - start_time).total_seconds()
        self.knowledge_base.log_learning(
            topic=topic,
            action="learn_topic",
            result=f"learned {len(knowledge_list)} pages",
            duration=duration
        )
        
        print(f"   ✅ 学习完成：{topic} ({duration:.2f}秒)")
        return True
    
    def learn_programming(self, language: str, topic: str):
        """学习编程主题"""
        query = f"{language} {topic} tutorial best practices"
        self.learn_topic(query, category="programming")
    
    def install_skill(self, skill_name: str, functionality: str):
        """安装新技能"""
        print(f"\n🎯 安装技能：{skill_name}")
        
        code = self.skill_downloader.create_skill_template(skill_name, functionality)
        module_path = self.skill_downloader.download_skill(skill_name, code, functionality)
        
        self.knowledge_base.register_skill(
            name=skill_name,
            description=functionality,
            module_path=module_path,
            version="1.0.0"
        )
        
        print(f"   ✅ 技能安装完成：{skill_name}")
        return module_path
    
    def get_status(self) -> Dict:
        """获取学习状态"""
        stats = self.knowledge_base.get_statistics()
        
        return {
            'knowledge_count': stats['total_knowledge'],
            'skills_count': stats['total_skills'],
            'learning_sessions': stats['total_learning_sessions'],
            'recent_learning': stats['recent_learning']
        }
    
    def show_status(self):
        """显示状态"""
        stats = self.get_status()
        
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         📊 自主学习状态                                ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        print(f"   📚 知识总量：{stats['knowledge_count']}")
        print(f"   🎯 技能数量：{stats['skills_count']}")
        print(f"   📖 学习次数：{stats['learning_sessions']}")
        
        if stats['recent_learning']:
            print("\n   最近学习:")
            for item in stats['recent_learning']:
                print(f"      • {item['topic']}: {item['action']}")
        
        print()


def demo():
    """演示"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 自主学习演示                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    learner = AutonomousLearner()
    
    # 学习 Python
    learner.learn_programming("Python", "async await")
    
    # 安装技能
    learner.install_skill("web_scraper", "网页抓取和数据提取")
    
    # 显示状态
    learner.show_status()
    
    print("✅ 自主学习演示完成！\n")


if __name__ == '__main__':
    demo()
