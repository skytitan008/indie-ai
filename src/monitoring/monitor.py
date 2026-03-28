"""
自我监控系统

监控 AI 系统的性能表现，检测异常并生成反思
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from ..core.models import PerformanceRecord


@dataclass
class Insight:
    """洞察/反思"""
    timestamp: datetime
    type: str  # 'performance', 'anomaly', 'suggestion'
    message: str
    severity: str  # 'low', 'medium', 'high'
    data: Dict = None


class SelfMonitor:
    """
    自我监控系统
    
    持续监控系统表现，检测异常，生成洞察
    """
    
    def __init__(self, window_size: int = 10):
        # 性能记录历史
        self.performance_history: List[PerformanceRecord] = []
        
        # 分析窗口大小
        self.window_size = window_size
        
        # 异常检测阈值
        self.anomaly_threshold = 0.3  # 30% 偏差
        
        # 洞察历史
        self.insights: List[Insight] = []
        
        # 监控指标
        self.metrics: Dict[str, List[float]] = {}
    
    def record_performance(
        self,
        metric_name: str,
        expected: float,
        actual: float,
        context: str = ""
    ):
        """记录性能表现"""
        record = PerformanceRecord(
            timestamp=datetime.now(),
            metric_name=metric_name,
            expected=expected,
            actual=actual,
            context=context
        )
        
        self.performance_history.append(record)
        
        # 更新指标历史
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(actual)
        
        # 限制历史记录大小
        if len(self.performance_history) > 1000:
            self.performance_history.pop(0)
        
        # 检查是否产生洞察
        self._check_for_insights(record)
    
    def _check_for_insights(self, record: PerformanceRecord):
        """检查是否需要生成洞察"""
        # 检查异常
        if record.deviation > self.anomaly_threshold:
            insight = Insight(
                timestamp=datetime.now(),
                type='anomaly',
                message=f"检测到{record.metric_name}异常：偏差{record.deviation:.1%}",
                severity='high' if record.deviation > 0.5 else 'medium',
                data={
                    'expected': record.expected,
                    'actual': record.actual,
                    'deviation': record.deviation
                }
            )
            self.insights.append(insight)
        
        # 检查持续表现不佳
        self._check_persistent_underperformance(record.metric_name)
    
    def _check_persistent_underperformance(self, metric_name: str):
        """检查持续表现不佳"""
        if metric_name not in self.metrics:
            return
        
        recent = self.metrics[metric_name][-self.window_size:]
        if len(recent) < self.window_size:
            return
        
        # 检查是否持续低于预期
        if all(v < 0.7 for v in recent):
            insight = Insight(
                timestamp=datetime.now(),
                type='performance',
                message=f"{metric_name}持续表现不佳（最近{self.window_size}次）",
                severity='high',
                data={'recent_values': recent}
            )
            
            # 避免重复添加
            if not any(
                i.type == 'performance' and metric_name in i.message 
                for i in self.insights[-5:]
            ):
                self.insights.append(insight)
    
    def check_anomaly(self, metric_name: str = None) -> bool:
        """检查是否存在异常"""
        if not self.performance_history:
            return False
        
        recent = self.performance_history[-self.window_size:]
        
        if metric_name:
            recent = [r for r in recent if r.metric_name == metric_name]
        
        if not recent:
            return False
        
        avg_deviation = sum(r.deviation for r in recent) / len(recent)
        return avg_deviation > self.anomaly_threshold
    
    def generate_insight(self) -> str:
        """生成自我反思报告"""
        if not self.insights:
            return "系统表现正常，无异常检测"
        
        # 获取最近的洞察
        recent_insights = self.insights[-5:]
        
        report_lines = ["【自我监控报告】", ""]
        
        for insight in recent_insights:
            severity_icon = {
                'low': '○',
                'medium': '◐',
                'high': '●'
            }.get(insight.severity, '○')
            
            report_lines.append(
                f"{severity_icon} [{insight.type}] {insight.message}"
            )
        
        # 添加建议
        suggestions = self._generate_suggestions()
        if suggestions:
            report_lines.append("")
            report_lines.append("【建议】")
            for sug in suggestions:
                report_lines.append(f"  • {sug}")
        
        return "\n".join(report_lines)
    
    def _generate_suggestions(self) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 分析性能模式
        for metric_name, values in self.metrics.items():
            if len(values) < 5:
                continue
            
            recent = values[-5:]
            avg = sum(recent) / len(recent)
            
            if avg < 0.5:
                suggestions.append(f"{metric_name}表现持续偏低，建议调整策略")
            
            # 检查趋势
            if len(values) >= 10:
                trend = sum(values[-5:]) - sum(values[-10:-5])
                if trend < -0.2:
                    suggestions.append(f"{metric_name}呈下降趋势，需要关注")
        
        return suggestions
    
    def get_performance_summary(self) -> Dict:
        """获取性能摘要"""
        if not self.performance_history:
            return {'status': 'no_data'}
        
        recent = self.performance_history[-self.window_size:]
        
        avg_deviation = sum(r.deviation for r in recent) / len(recent)
        underperforming = sum(1 for r in recent if r.is_underperforming)
        
        return {
            'status': 'good' if avg_deviation < 0.2 else 'warning',
            'avg_deviation': avg_deviation,
            'underperforming_rate': underperforming / len(recent),
            'total_records': len(self.performance_history),
            'total_insights': len(self.insights),
            'metrics_tracked': len(self.metrics)
        }
    
    def get_metrics_trend(self, metric_name: str, window: int = 10) -> Dict:
        """获取指标趋势"""
        if metric_name not in self.metrics:
            return {'error': 'metric not found'}
        
        values = self.metrics[metric_name][-window:]
        
        if len(values) < 2:
            return {'error': 'insufficient data'}
        
        # 计算趋势
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        trend = (sum(second_half) - sum(first_half)) / len(first_half)
        
        return {
            'metric': metric_name,
            'current': values[-1],
            'average': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'trend': 'up' if trend > 0.1 else 'down' if trend < -0.1 else 'stable',
            'values': values
        }
    
    def clear(self):
        """清空监控数据"""
        self.performance_history.clear()
        self.insights.clear()
        self.metrics.clear()
