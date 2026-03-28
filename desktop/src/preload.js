const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的 API 给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 运行实验
  runExperiment: (scriptName) => ipcRenderer.invoke('run-experiment', scriptName),
  
  // 读取数据文件
  readData: (filePath) => ipcRenderer.invoke('read-data', filePath),
  
  // 获取 Python 版本
  getPythonVersion: () => ipcRenderer.invoke('get-python-version'),
  
  // 监听实验输出
  onExperimentOutput: (callback) => {
    ipcRenderer.on('experiment-output', (event, data) => callback(data));
  },
  
  // 监听实验完成
  onExperimentComplete: (callback) => {
    ipcRenderer.on('experiment-complete', (event, data) => callback(data));
  },
  
  // 移除监听器
  removeExperimentOutputListener: () => {
    ipcRenderer.removeAllListeners('experiment-output');
  },
  
  removeExperimentCompleteListener: () => {
    ipcRenderer.removeAllListeners('experiment-complete');
  },
});
