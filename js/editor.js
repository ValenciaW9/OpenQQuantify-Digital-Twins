/*Valencia Walker's editor.js*/

require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.21.2/min/vs' }});
require(['vs/editor/editor.main'], function () {
    const editor = monaco.editor.create(document.getElementById('editor'), {
        value: "# Write Python code to simulate motor\nprint('Motor spinning at 2000 RPM')",
        language: "python"
    });

    document.getElementById("runCode").addEventListener("click", async () => {
        const code = editor.getValue();
        const res = await fetch("/api/execute", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        const result = await res.json();
        document.getElementById("output").innerText = result.output;
    });
});
