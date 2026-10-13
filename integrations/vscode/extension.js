// VS Code extension for SmartSeal — runs the tool on the active file/workspace
// and reports the result. Minimal, dependency-free; calls the shipped adapter.py.
const vscode = require('vscode');
const path = require('path');
const { spawnSync } = require('child_process');

function activate(context) {
  const cmd = vscode.commands.registerCommand('smartseal.run', async () => {
    const ed = vscode.window.activeTextEditor;
    const folder = (vscode.workspace.workspaceFolders || [])[0];
    const target = ed && ed.document ? ed.document.fileName : (folder && folder.uri.fsPath);
    if (!target) { vscode.window.showWarningMessage('SmartSeal: nothing to run on'); return; }
    const adapter = path.join(context.extensionPath, 'adapter.py');
    const py = vscode.workspace.getConfiguration('smartseal').get('python', 'python3');
    const res = spawnSync(py, [adapter, '--file', target], { encoding: 'utf8' });
    if (res.status !== 0) { vscode.window.showErrorMessage('SmartSeal: ' + (res.stderr || 'failed')); return; }
    const out = res.stdout.trim();
    vscode.window.showInformationMessage('SmartSeal: ' + out.slice(0, 400));
    const ch = vscode.window.createOutputChannel('SmartSeal');
    ch.appendLine(out); ch.show(true);
  });
  context.subscriptions.push(cmd);
}

function deactivate() {}
module.exports = { activate, deactivate };
