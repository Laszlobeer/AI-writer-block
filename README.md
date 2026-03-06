# 📝 AI Writer's Block Helper
[!logo](logo.png)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-brightgreen.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-orange.svg)](https://ollama.com)

> A desktop application that connects to your **local Ollama instance** to help writers overcome creative blocks with AI-powered suggestions — completely offline and private.

🔗 **Repository**: [Laszlobeer/AI-writer-block](https://github.com/Laszlobeer/AI-writer-block)

---

## ✨ Features

- 🔒 **100% Local & Private**: Runs entirely on your machine using Ollama (`localhost:11434`). No data leaves your computer.
- 🧠 **Smart Creative Assistance**:
  - **Deep Questions**: 3-5 thought-provoking prompts to explore characters, motivations, or plot holes.
  - **Continuation Suggestions**: 3-5 concrete plot ideas or twists to spark your next paragraph.
- 🧵 **Non-Blocking UI**: Background threads (`QThread`) keep the interface responsive during AI generation.
- 🌓 **Theme Toggle**: Instantly switch between **Light Mode** and **Dark Mode** (styled with Qt Fusion).
- 🔄 **Auto Model Detection**: Scans available Ollama models on startup; manual refresh supported.
- 🎨 **Polished Qt Interface**: Clean splitter layout, monospace editor fonts, and custom stylesheets.

---

## 📦 Prerequisites

1. **Python 3.6 or higher**
2. **Ollama** installed and running locally:
   - Download: [https://ollama.com](https://ollama.com)
   - Verify server: `http://localhost:11434`
   - Pull a model (example):  
     ```bash
     ollama pull llama3
     ```
3. **Python dependencies**:
   ```bash
   pip install PyQt5 requests
   ```

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Laszlobeer/AI-writer-block.git
   cd AI-writer-block
   ```

2. Install dependencies:
   ```bash
   pip install PyQt5 requests
   ```
  

3. Ensure Ollama is running:
   ```bash
   ollama serve  # Usually auto-starts with the desktop app
   ```

---

## ▶️ Usage

1. **Launch the app**:
   > **Note**: The filename contains a space. Wrap it in quotes when running.
   ```bash
   python "ai writer block.py"
   ```

2. **Select a model**:
   - Models are auto-detected on startup.
   - Click **🔄 Refresh** if your model doesn't appear.

3. **Write or paste your story** in the *"Your Story So Far"* panel.

4. **Click** ✨ **Help Me Continue (Generate Suggestions)**.

5. **Review the AI output**:
   - 🤔 *Deep Questions* to deepen your narrative
   - 💡 *Continuation Suggestions* to move forward

6. **Toggle theme** anytime with the 🌙/☀️ button.

---

## ⚙️ Configuration

Edit constants directly in `ai writer block.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `OLLAMA_BASE_URL` | `"http://localhost:11434"` | Change if Ollama runs on a different host/port |
| `system_prompt` | *(inside `OllamaWorker`)* | Customize the AI's coaching behavior. Currently configured to **not rewrite** the story, but provide questions and suggestions. |

> 💡 **Tip**: The system prompt is intentionally designed to make the AI act as a *coach*, not a ghostwriter — preserving your creative voice.

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| ❌ *"Cannot connect to Ollama"* | Ensure `ollama serve` is running. Visit `http://localhost:11434` in your browser to verify. |
| ❌ *"No models found"* | Pull a model via CLI: `ollama pull mistral` → then click **🔄 Refresh**. |
| ❌ *UI freezes during generation* | Check firewall/antivirus settings; ensure localhost traffic isn't blocked. |
| ❌ *Generation fails or returns empty* | Try a different model. Some smaller models may struggle with complex prompts. |
| ❌ *CSS styling looks broken* | The app uses Qt Fusion style. Ensure PyQt5 is correctly installed. |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Laszlobeer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/Laszlobeer/AI-writer-block/issues).

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) for making local LLMs accessible
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the powerful GUI framework
- Writers everywhere who keep creating, one word at a time ✍️

---

> **Made with ❤️ by [Laszlobeer](https://github.com/Laszlobeer)**  
> *Empowering creativity through local AI.*
