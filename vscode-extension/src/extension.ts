// VS Code 插件主入口

import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('Indie AI');
    outputChannel.appendLine('🤖 Indie AI Helper 已激活');

    // 注册命令
    registerCommands(context);

    // 自动格式化监听
    setupAutoFormat(context);
}

function registerCommands(context: vscode.ExtensionContext) {
    // 格式化代码
    const formatCmd = vscode.commands.registerCommand('indie-ai.formatCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('没有活动的编辑器');
            return;
        }

        const document = editor.document;
        const filePath = document.fileName;

        outputChannel.appendLine(`\n📝 格式化代码：${filePath}`);
        outputChannel.show(true);

        try {
            const config = vscode.workspace.getConfiguration('indieAi');
            const pythonPath = config.get('pythonPath', 'python3');
            const projectPath = config.get('projectPath', '');

            const command = `${pythonPath} -m src.integration.formatter "${filePath}"`;
            
            outputChannel.appendLine(`执行：${command}`);
            
            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    outputChannel.appendLine(`❌ 错误：${error.message}`);
                    vscode.window.showErrorMessage(`格式化失败：${error.message}`);
                    return;
                }
                
                outputChannel.appendLine(stdout);
                if (stderr) {
                    outputChannel.appendLine(`⚠️  警告：${stderr}`);
                }
                
                vscode.window.showInformationMessage('✅ 代码格式化完成！');
            });
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : '未知错误';
            vscode.window.showErrorMessage(`格式化失败：${errorMessage}`);
        }
    });

    // 运行实验
    const runExpCmd = vscode.commands.registerCommand('indie-ai.runExperiment', async () => {
        const experiments = [
            { label: '学习曲线实验', script: 'demo/学习曲线实验.py' },
            { label: 'SARSA 对比实验', script: 'demo/SARSA 对比实验.py' },
            { label: '多 Agent 协作', script: 'demo/多 Agent 协作演示.py' },
            { label: '真实任务执行', script: 'demo/真实任务执行.py' },
            { label: '长期学习实验', script: 'demo/长期学习实验.py' },
            { label: '实际应用集成', script: 'demo/实际应用集成演示.py' },
            { label: '新功能演示', script: 'demo/新功能快速演示.py' }
        ];

        const selected = await vscode.window.showQuickPick(
            experiments.map(e => e.label),
            { placeHolder: '选择要运行的实验' }
        );

        if (!selected) return;

        const experiment = experiments.find(e => e.label === selected);
        if (!experiment) return;

        outputChannel.appendLine(`\n🚀 运行实验：${selected}`);
        outputChannel.show(true);

        try {
            const config = vscode.workspace.getConfiguration('indieAi');
            const pythonPath = config.get('pythonPath', 'python3');
            const projectPath = config.get('projectPath', '');

            const command = `${pythonPath} "${experiment.script}"`;
            
            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    outputChannel.appendLine(`❌ 错误：${error.message}`);
                    return;
                }
                
                outputChannel.appendLine(stdout);
                vscode.window.showInformationMessage(`✅ 实验完成：${selected}`);
            });
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : '未知错误';
            vscode.window.showErrorMessage(`实验失败：${errorMessage}`);
        }
    });

    // 显示状态
    const statusCmd = vscode.commands.registerCommand('indie-ai.showStatus', async () => {
        outputChannel.appendLine('\n📊 获取 Indie AI 状态...');
        outputChannel.show(true);

        try {
            const config = vscode.workspace.getConfiguration('indieAi');
            const pythonPath = config.get('pythonPath', 'python3');
            const projectPath = config.get('projectPath', '');

            const command = `${pythonPath} cli.py status`;
            
            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    outputChannel.appendLine(`❌ 错误：${error.message}`);
                    return;
                }
                
                outputChannel.appendLine(stdout);
            });
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : '未知错误';
            vscode.window.showErrorMessage(`获取状态失败：${errorMessage}`);
        }
    });

    // 运行任务
    const runTaskCmd = vscode.commands.registerCommand('indie-ai.runTask', async () => {
        const tasks = [
            { label: '代码格式化', command: 'python3 -m src.integration.formatter src/' },
            { label: '运行测试', command: 'python3 -m pytest tests/ -v' },
            { label: '生成日报', command: 'python3 -m src.integration.daily_report' },
            { label: '安装 Git Hooks', command: 'bash scripts/install-hooks.sh' }
        ];

        const selected = await vscode.window.showQuickPick(
            tasks.map(t => t.label),
            { placeHolder: '选择要执行的任务' }
        );

        if (!selected) return;

        const task = tasks.find(t => t.label === selected);
        if (!task) return;

        outputChannel.appendLine(`\n🔧 执行任务：${selected}`);
        outputChannel.show(true);

        try {
            const config = vscode.workspace.getConfiguration('indieAi');
            const projectPath = config.get('projectPath', '');

            exec(task.command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    outputChannel.appendLine(`❌ 错误：${error.message}`);
                    return;
                }
                
                outputChannel.appendLine(stdout);
                vscode.window.showInformationMessage(`✅ 任务完成：${selected}`);
            });
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : '未知错误';
            vscode.window.showErrorMessage(`任务失败：${errorMessage}`);
        }
    });

    // 生成日报
    const reportCmd = vscode.commands.registerCommand('indie-ai.generateReport', async () => {
        outputChannel.appendLine('\n📝 生成工作日报...');
        outputChannel.show(true);

        try {
            const config = vscode.workspace.getConfiguration('indieAi');
            const pythonPath = config.get('pythonPath', 'python3');
            const projectPath = config.get('projectPath', '');

            const command = `${pythonPath} -m src.integration.daily_report`;
            
            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    outputChannel.appendLine(`❌ 错误：${error.message}`);
                    return;
                }
                
                outputChannel.appendLine(stdout);
                vscode.window.showInformationMessage('✅ 日报已生成！');
            });
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : '未知错误';
            vscode.window.showErrorMessage(`生成日报失败：${errorMessage}`);
        }
    });

    context.subscriptions.push(
        formatCmd,
        runExpCmd,
        statusCmd,
        runTaskCmd,
        reportCmd
    );
}

function setupAutoFormat(context: vscode.ExtensionContext) {
    vscode.workspace.onWillSaveTextDocument(async (event) => {
        const config = vscode.workspace.getConfiguration('indieAi');
        const autoFormat = config.get('autoFormat', false);

        if (!autoFormat) return;
        if (event.document.languageId !== 'python') return;

        const filePath = event.document.fileName;
        
        try {
            const pythonPath = config.get('pythonPath', 'python3');
            const projectPath = config.get('projectPath', '');

            await new Promise<void>((resolve, reject) => {
                exec(`${pythonPath} -m src.integration.formatter "${filePath}"`, 
                    { cwd: projectPath }, 
                    (error) => {
                        if (error) reject(error);
                        else resolve();
                    }
                );
            });
        } catch (err) {
            vscode.window.showWarningMessage(`自动格式化失败：${err instanceof Error ? err.message : '未知错误'}`);
        }
    });
}

export function deactivate() {
    outputChannel.appendLine('⏸️  Indie AI Helper 已停用');
}
