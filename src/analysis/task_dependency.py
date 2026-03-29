#!/usr/bin/env python3
"""
任务依赖图可视化

功能：
- 解析任务依赖关系
- 生成有向图（Graphviz/DOT 格式）
- 可视化展示（Matplotlib）
- 检测循环依赖
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False
    print("⚠️  未安装 graphviz，使用简单文本输出")

try:
    import matplotlib.pyplot as plt
    import networkx as nx
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class TaskDependencyGraph:
    """任务依赖图"""
    
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self.dependencies: Dict[str, List[str]] = {}
    
    def add_task(self, task_id: str, name: str, dependencies: List[str] = None):
        """添加任务"""
        self.tasks[task_id] = {
            'id': task_id,
            'name': name,
            'dependencies': dependencies or []
        }
        self.dependencies[task_id] = dependencies or []
    
    def add_dependency(self, task_id: str, depends_on: str):
        """添加依赖关系"""
        if task_id not in self.dependencies:
            self.dependencies[task_id] = []
        
        if depends_on not in self.dependencies[task_id]:
            self.dependencies[task_id].append(depends_on)
    
    def detect_cycles(self) -> List[List[str]]:
        """检测循环依赖"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.dependencies.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, path + [neighbor]):
                        return True
                elif neighbor in rec_stack:
                    # 找到循环
                    cycle_start = path.index(neighbor) if neighbor in path else 0
                    cycles.append(path[cycle_start:] + [node])
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.tasks:
            if node not in visited:
                dfs(node, [node])
        
        return cycles
    
    def topological_sort(self) -> List[str]:
        """拓扑排序（执行顺序）"""
        in_degree = {task: 0 for task in self.tasks}
        
        # 计算入度
        for task, deps in self.dependencies.items():
            for dep in deps:
                if task in in_degree:
                    in_degree[task] += 1
        
        # 找到所有入度为 0 的节点
        queue = [task for task, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            for task, deps in self.dependencies.items():
                if node in deps:
                    in_degree[task] -= 1
                    if in_degree[task] == 0:
                        queue.append(task)
        
        if len(result) != len(self.tasks):
            raise ValueError("存在循环依赖，无法拓扑排序")
        
        return result
    
    def get_critical_path(self) -> Tuple[List[str], int]:
        """获取关键路径（最长路径）"""
        # 使用动态规划
        sorted_tasks = self.topological_sort()
        dist = {task: 0 for task in self.tasks}
        predecessor = {task: None for task in self.tasks}
        
        for task in sorted_tasks:
            for other_task, deps in self.dependencies.items():
                if task in deps:
                    if dist[other_task] < dist[task] + 1:
                        dist[other_task] = dist[task] + 1
                        predecessor[other_task] = task
        
        # 找到最长路径的终点
        max_dist = max(dist.values())
        end_task = [task for task, d in dist.items() if d == max_dist][0]
        
        # 回溯找到路径
        path = []
        current = end_task
        while current is not None:
            path.append(current)
            current = predecessor[current]
        
        path.reverse()
        return path, max_dist + 1
    
    def to_dot(self) -> str:
        """生成 DOT 格式"""
        lines = ['digraph TaskDependencies {']
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box, style=filled, fillcolor=lightblue];')
        lines.append('')
        
        # 添加节点
        for task_id, task in self.tasks.items():
            label = f"{task['name']}\\n({task_id})"
            lines.append(f'  "{task_id}" [label="{label}"];')
        
        lines.append('')
        
        # 添加边
        for task_id, deps in self.dependencies.items():
            for dep in deps:
                lines.append(f'  "{dep}" -> "{task_id}";')
        
        lines.append('}')
        return '\n'.join(lines)
    
    def visualize(self, output_file: str = "task_dependency_graph.png"):
        """可视化任务依赖图"""
        if not HAS_MATPLOTLIB:
            print("❌ 未安装 matplotlib，无法可视化")
            return
        
        # 创建网络图
        G = nx.DiGraph()
        
        for task_id, task in self.tasks.items():
            G.add_node(task_id, label=task['name'])
        
        for task_id, deps in self.dependencies.items():
            for dep in deps:
                G.add_edge(dep, task_id)
        
        # 布局
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # 绘制
        plt.figure(figsize=(12, 8))
        
        # 节点
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', alpha=0.8)
        
        # 边
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrows=True, 
                              arrowsize=20, edge_color='gray', width=2)
        
        # 标签
        labels = {task_id: task['name'] for task_id, task in self.tasks.items()}
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
        
        plt.title('任务依赖关系图', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 依赖图已保存到：{output_file}")
    
    def export_json(self, output_file: str = "task_dependencies.json"):
        """导出为 JSON"""
        data = {
            'tasks': self.tasks,
            'dependencies': self.dependencies,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 依赖数据已保存到：{output_file}")
    
    def print_summary(self):
        """打印摘要信息"""
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         📊 任务依赖图分析                              ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        print(f"📋 任务总数：{len(self.tasks)}")
        print(f"🔗 依赖关系数：{sum(len(deps) for deps in self.dependencies.values())}")
        
        # 检测循环
        cycles = self.detect_cycles()
        if cycles:
            print(f"\n❌ 发现循环依赖：{len(cycles)} 个")
            for i, cycle in enumerate(cycles, 1):
                print(f"   循环 {i}: {' -> '.join(cycle)}")
        else:
            print(f"\n✅ 无循环依赖")
        
        # 拓扑排序
        try:
            order = self.topological_sort()
            print(f"\n📝 推荐执行顺序:")
            for i, task_id in enumerate(order, 1):
                task_name = self.tasks[task_id]['name']
                print(f"   {i}. {task_name} ({task_id})")
        except ValueError as e:
            print(f"\n⚠️  无法拓扑排序：{e}")
        
        # 关键路径
        try:
            path, length = self.get_critical_path()
            print(f"\n🎯 关键路径（长度 {length}）:")
            for task_id in path:
                task_name = self.tasks[task_id]['name']
                print(f"   → {task_name} ({task_id})")
        except:
            pass
        
        print()


def create_sample_graph() -> TaskDependencyGraph:
    """创建示例任务依赖图"""
    graph = TaskDependencyGraph()
    
    # AIGC 视频项目任务
    graph.add_task("T1", "需求分析", [])
    graph.add_task("T2", "脚本创作", ["T1"])
    graph.add_task("T3", "分镜设计", ["T2"])
    graph.add_task("T4", "角色设计", ["T3"])
    graph.add_task("T5", "场景设计", ["T3"])
    graph.add_task("T6", "视频生成", ["T4", "T5"])
    graph.add_task("T7", "音频合成", ["T2"])
    graph.add_task("T8", "后期剪辑", ["T6", "T7"])
    graph.add_task("T9", "质量审核", ["T8"])
    graph.add_task("T10", "发布上线", ["T9"])
    
    return graph


def demo():
    """演示"""
    print("\n🚀 任务依赖图可视化演示\n")
    
    graph = create_sample_graph()
    graph.print_summary()
    
    # 导出
    graph.export_json()
    
    # 生成 DOT 文件
    dot_content = graph.to_dot()
    with open("task_dependencies.dot", 'w') as f:
        f.write(dot_content)
    print(f"✅ DOT 文件已保存到：task_dependencies.dot")
    
    # 可视化
    if HAS_MATPLOTLIB:
        graph.visualize()
    
    # 如果有 graphviz，生成 PDF
    if HAS_GRAPHVIZ:
        dot = graphviz.Source(dot_content)
        dot.render("task_dependency_graph", format="pdf")
        print(f"✅ PDF 已保存到：task_dependency_graph.pdf")
    
    print("\n✅ 演示完成！\n")


if __name__ == '__main__':
    demo()
