const { app, BrowserWindow, Tray, Menu, ipcMain, Notification, nativeImage } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let tray = null;
let isQuitting = false;

// 窗口创建
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    icon: path.join(__dirname, '../assets/icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    titleBarStyle: 'default',
    backgroundColor: '#1a1a2e',
  });

  // 加载 Web 界面
  mainWindow.loadFile(path.join(__dirname, '../../web/index.html'));

  // 开发模式下打开 DevTools
  // mainWindow.webContents.openDevTools();

  // 窗口关闭事件
  mainWindow.on('close', (event) => {
    if (!isQuitting) {
      event.preventDefault();
      mainWindow.hide();
      mainWindow.setSkipTaskbar(true);
      
      // 显示托盘通知
      if (Notification.isSupported()) {
        new Notification({
          title: 'Indie AI',
          body: '应用已最小化到系统托盘，点击图标重新打开',
          icon: path.join(__dirname, '../assets/icon.png'),
        }).show();
      }
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// 创建系统托盘
function createTray() {
  const iconPath = path.join(__dirname, '../assets/icon.png');
  const icon = nativeImage.createFromPath(iconPath);
  const trayIcon = icon.resize({ width: 16, height: 16 });
  
  tray = new Tray(trayIcon);
  
  const contextMenu = Menu.buildFromTemplate([
    {
      label: '打开主窗口',
      click: () => {
        mainWindow.show();
        mainWindow.setSkipTaskbar(false);
        mainWindow.focus();
      },
    },
    {
      label: '运行综合实验',
      click: () => runExperiment('综合实验.py'),
    },
    {
      label: '运行真实任务执行',
      click: () => runExperiment('真实任务执行.py'),
    },
    {
      label: '运行长期学习实验',
      click: () => runExperiment('长期学习实验.py'),
    },
    {
      label: '运行多 Agent 协作',
      click: () => runExperiment('多 Agent 协作演示.py'),
    },
    { type: 'separator' },
    {
      label: '退出',
      click: () => {
        isQuitting = true;
        app.quit();
      },
    },
  ]);
  
  tray.setToolTip('Indie AI - 独立思考 AI 系统');
  tray.setContextMenu(contextMenu);
  
  // 双击托盘图标打开窗口
  tray.on('double-click', () => {
    mainWindow.show();
    mainWindow.setSkipTaskbar(false);
    mainWindow.focus();
  });
}

// 运行实验
function runExperiment(scriptName) {
  const demoPath = path.join(__dirname, '../../demo', scriptName);
  const pythonProcess = spawn('python3', [demoPath], {
    cwd: path.join(__dirname, '../..'),
  });
  
  let output = '';
  let error = '';
  
  pythonProcess.stdout.on('data', (data) => {
    const text = data.toString();
    output += text;
    console.log(`[实验输出] ${text}`);
    
    // 发送到前端
    if (mainWindow) {
      mainWindow.webContents.send('experiment-output', {
        type: 'stdout',
        data: text,
        script: scriptName,
      });
    }
  });
  
  pythonProcess.stderr.on('data', (data) => {
    const text = data.toString();
    error += text;
    console.error(`[实验错误] ${text}`);
    
    if (mainWindow) {
      mainWindow.webContents.send('experiment-output', {
        type: 'stderr',
        data: text,
        script: scriptName,
      });
    }
  });
  
  pythonProcess.on('close', (code) => {
    console.log(`[实验完成] ${scriptName} 退出码：${code}`);
    
    if (mainWindow) {
      mainWindow.webContents.send('experiment-complete', {
        script: scriptName,
        code: code,
        output: output,
        error: error,
      });
    }
    
    // 显示完成通知
    if (Notification.isSupported()) {
      const status = code === 0 ? '成功' : '失败';
      new Notification({
        title: '实验完成',
        body: `${scriptName} - ${status}`,
        icon: path.join(__dirname, '../assets/icon.png'),
      }).show();
    }
  });
  
  return pythonProcess.pid;
}

// 读取实验数据
function readExperimentData(filePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        reject(err);
      } else {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data });
        }
      }
    });
  });
}

// Electron 就绪
app.whenReady().then(() => {
  createWindow();
  createTray();
  
  // 注册 IPC 处理器
  ipcMain.handle('run-experiment', (event, scriptName) => {
    return runExperiment(scriptName);
  });
  
  ipcMain.handle('read-data', async (event, filePath) => {
    try {
      const data = await readExperimentData(filePath);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });
  
  ipcMain.handle('get-python-version', async () => {
    const { exec } = require('child_process');
    return new Promise((resolve) => {
      exec('python3 --version', (error, stdout) => {
        if (error) {
          resolve('未知');
        } else {
          resolve(stdout.trim());
        }
      });
    });
  });
});

// 所有窗口关闭时
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// 退出前清理
app.on('before-quit', () => {
  isQuitting = true;
  if (tray) {
    tray.destroy();
  }
});
