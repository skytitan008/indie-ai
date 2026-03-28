/**
 * 独立 AI MVP - Web 可视化
 * 学习曲线图表展示
 */

let learningChart = null;
let qTableChart = null;
let successChart = null;
let currentData = null;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    loadDefaultData();
});

// 初始化图表
function initCharts() {
    // 学习曲线图表
    const learningCtx = document.getElementById('learningChart').getContext('2d');
    learningChart = new Chart(learningCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '平均奖励',
                data: [],
                borderColor: 'rgb(102, 126, 234)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
    
    // Q 表增长图表
    const qTableCtx = document.getElementById('qTableChart').getContext('2d');
    qTableChart = new Chart(qTableCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Q 表大小',
                data: [],
                borderColor: 'rgb(118, 75, 162)',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // 成功率图表
    const successCtx = document.getElementById('successChart').getContext('2d');
    successChart = new Chart(successCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: '成功率',
                data: [],
                backgroundColor: 'rgba(72, 187, 120, 0.6)',
                borderColor: 'rgb(72, 187, 120)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

// 加载默认数据
async function loadDefaultData() {
    addLog('正在加载默认数据...', 'info');
    
    try {
        const response = await fetch('../learning_curve_data.json');
        if (!response.ok) {
            throw new Error('默认数据文件不存在');
        }
        const data = await response.json();
        updateData(data);
        addLog('✓ 默认数据加载成功', 'success');
    } catch (error) {
        addLog('⚠ 无法加载默认数据：' + error.message, 'warning');
        addLog('请上传 JSON 数据文件', 'info');
    }
}

// 刷新数据
function refreshData() {
    if (currentData) {
        updateData(currentData);
        addLog('✓ 数据已刷新', 'success');
    } else {
        loadDefaultData();
    }
}

// 文件上传处理
document.getElementById('dataFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    document.getElementById('fileName').textContent = file.name;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            updateData(data);
            addLog('✓ 文件加载成功：' + file.name, 'success');
        } catch (error) {
            addLog('✗ 文件解析失败：' + error.message, 'error');
        }
    };
    reader.readAsText(file);
});

// 更新数据
function updateData(data) {
    currentData = data;
    
    if (!data.runs || data.runs.length === 0) {
        addLog('⚠ 数据格式不正确', 'error');
        return;
    }
    
    const runs = data.runs;
    
    // 更新统计
    document.getElementById('totalRuns').textContent = runs.length;
    
    const avgReward = runs.reduce((sum, r) => sum + r.avg_reward, 0) / runs.length;
    document.getElementById('avgReward').textContent = avgReward.toFixed(2);
    
    const finalQSize = runs[runs.length - 1].q_table_size;
    document.getElementById('finalQSize').textContent = finalQSize;
    
    const totalUpdates = runs[runs.length - 1].total_updates;
    document.getElementById('totalUpdates').textContent = totalUpdates.toLocaleString();
    
    // 更新学习曲线
    learningChart.data.labels = runs.map(r => `第${r.run}轮`);
    learningChart.data.datasets[0].data = runs.map(r => r.avg_reward);
    learningChart.update();
    
    // 更新 Q 表增长
    qTableChart.data.labels = runs.map(r => `第${r.run}轮`);
    qTableChart.data.datasets[0].data = runs.map(r => r.q_table_size);
    qTableChart.update();
    
    // 更新成功率
    successChart.data.labels = runs.map(r => `第${r.run}轮`);
    successChart.data.datasets[0].data = runs.map(r => r.success_rate);
    successChart.update();
    
    // 添加日志
    addLog(`数据更新：${runs.length} 轮`, 'info');
    addLog(`平均奖励：${avgReward.toFixed(2)}`, 'info');
    addLog(`Q 表增长：0 → ${finalQSize}`, 'success');
    
    // 分析趋势
    if (runs.length >= 10) {
        const first10Avg = runs.slice(0, 10).reduce((sum, r) => sum + r.avg_reward, 0) / 10;
        const last10Avg = runs.slice(-10).reduce((sum, r) => sum + r.avg_reward, 0) / 10;
        const trend = last10Avg - first10Avg;
        
        if (trend > 0.5) {
            addLog(`📈 学习趋势：显著提升 (+${trend.toFixed(2)})`, 'success');
        } else if (trend > 0) {
            addLog(`📈 学习趋势：稳步提升 (+${trend.toFixed(2)})`, 'success');
        } else {
            addLog(`📉 学习趋势：略有下降 (${trend.toFixed(2)})`, 'warning');
        }
    }
}

// 导出图表
function exportImage() {
    const canvas = document.getElementById('learningChart');
    const link = document.createElement('a');
    link.download = 'learning_curve.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
    addLog('✓ 图表已导出', 'success');
}

// 切换深色模式
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    addLog('主题已切换', 'info');
}

// 添加日志
function addLog(message, type = 'info') {
    const logContent = document.getElementById('logContent');
    const entry = document.createElement('div');
    entry.className = `log-entry log-${type}`;
    
    const timestamp = new Date().toLocaleTimeString();
    entry.textContent = `[${timestamp}] ${message}`;
    
    logContent.insertBefore(entry, logContent.firstChild);
    
    // 限制日志数量
    while (logContent.children.length > 50) {
        logContent.removeChild(logContent.lastChild);
    }
}

// 深色模式样式
document.head.insertAdjacentHTML('beforeend', `
<style>
    body.dark-mode {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    }
    
    body.dark-mode .container {
        background: #1a202c;
        color: #e2e8f0;
    }
    
    body.dark-mode .chart-container {
        background: #2d3748;
    }
    
    body.dark-mode .chart-title {
        color: #e2e8f0;
    }
    
    body.dark-mode .file-upload {
        background: #2d3748;
        border-color: #4a5568;
    }
    
    body.dark-mode .file-name {
        color: #a0aec0;
    }
</style>
`);
