import * as vscode from "vscode";
import axios from "axios";

export function activate(context: vscode.ExtensionContext) {
    console.log("CodeXR extension is now active!");

    // --- Ask CodeXR Command ---
    const askCodeXR = vscode.commands.registerCommand("CodeXR.ask", async () => {
        const query = await vscode.window.showInputBox({
            placeHolder: "Ask CodeXR anything about your code..."
        });

        if (!query) {
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:8000/query", {
                user_query: query,
                error_logs: ""
            });

            CodeXRPanel.showResponse(response.data);
        } catch (err: any) {
            vscode.window.showErrorMessage("CodeXR server not reachable: " + err.message);
        }
    });

    // --- Explain with CodeXR (context menu) ---
    const explainError = vscode.commands.registerCommand("CodeXR.explainError", async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }

        const selection = editor.document.getText(editor.selection);
        if (!selection) {
            vscode.window.showInformationMessage("Select some error logs or code first.");
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:8000/query", {
                user_query: "",
                error_logs: selection
            });
            CodeXRPanel.showResponse(response.data);
        } catch (err: any) {
            vscode.window.showErrorMessage("CodeXR server not reachable: " + err.message);
        }
    });

    context.subscriptions.push(askCodeXR, explainError);
}

// --- CodeXR Side Panel ---
class CodeXRPanel {
    public static currentPanel: CodeXRPanel | undefined;
    private readonly panel: vscode.WebviewPanel;

    private constructor(panel: vscode.WebviewPanel) {
        this.panel = panel;

        // ✅ Listen for messages from the Webview
        this.panel.webview.onDidReceiveMessage(
            (message: { command: string; snippet?: string }) => {
                const editor = vscode.window.activeTextEditor;
                if (message.command === "insertSnippet" && message.snippet && editor) {
                    editor.insertSnippet(new vscode.SnippetString(message.snippet));
                }
            },
            undefined,
            []
        );
    }

    public static createOrShow(): CodeXRPanel {
        if (CodeXRPanel.currentPanel) {
            CodeXRPanel.currentPanel.panel.reveal(vscode.ViewColumn.Beside);
            return CodeXRPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            "codexr",
            "CodeXR Assistant",
            vscode.ViewColumn.Beside,
            { enableScripts: true }
        );

        CodeXRPanel.currentPanel = new CodeXRPanel(panel);
        panel.webview.html = this.getHtml("<p>Ask CodeXR to get started...</p>");
        return CodeXRPanel.currentPanel;
    }

    public static showResponse(data: any): void {
        if (!CodeXRPanel.currentPanel) {
            this.createOrShow();
        }
        CodeXRPanel.currentPanel!.panel.webview.html = this.getHtml(`
            <h2>CodeXR Response</h2>
            <pre>${JSON.stringify(data, null, 2)}</pre>
            <button onclick="vscode.postMessage({ command: 'insertSnippet', snippet: 'console.log(\"Hello from CodeXR\")' })">
                Insert Example Snippet
            </button>
        `);
    }

    private static getHtml(body: string): string {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <style>
            body { font-family: sans-serif; padding: 10px; }
            pre { background: #1e1e1e; color: #dcdcdc; padding: 10px; border-radius: 6px; white-space: pre-wrap; }
            button { margin-top: 10px; padding: 6px 12px; background: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #005a9e; }
          </style>
        </head>
        <body>
          ${body}
          <script>
            const vscode = acquireVsCodeApi();
          </script>
        </body>
        </html>`;
    }
}

export function deactivate() {}
