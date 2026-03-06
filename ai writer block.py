import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QPushButton, 
                             QPlainTextEdit, QMessageBox, QStatusBar, QSplitter)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont

# --- Configuration ---
OLLAMA_BASE_URL = "http://localhost:11434"

# --- Stylesheets ---
LIGHT_THEME = """
QMainWindow {
    background-color: #ffffff;
}
QWidget {
    background-color: #ffffff;
    color: #000000;
    font-family: "Segoe UI", Arial, sans-serif;
}
QLabel {
    color: #333333;
    font-weight: bold;
}
QPlainTextEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px;
    font-family: "Consolas", "Courier New", monospace;
}
QPlainTextEdit::placeholder {
    color: #999999;
}
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
    min-width: 150px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    selection-background-color: #e0e0e0;
    color: #000000;
}
QPushButton {
    background-color: #e0e0e0;
    color: #000000;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px 10px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #d0d0d0;
}
QPushButton#btn_generate {
    background-color: #4CAF50;
    color: white;
    border: none;
    font-size: 14px;
    padding: 10px;
}
QPushButton#btn_generate:hover {
    background-color: #45a049;
}
QPushButton#btn_generate:disabled {
    background-color: #a5d6a7;
    color: #e0e0e0;
}
QStatusBar {
    background-color: #f0f0f0;
    color: #333333;
    border-top: 1px solid #cccccc;
}
QSplitter::handle {
    background-color: #cccccc;
    height: 2px;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #2b2b2b;
}
QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-family: "Segoe UI", Arial, sans-serif;
}
QLabel {
    color: #ffffff;
    font-weight: bold;
}
QPlainTextEdit {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #444444;
    border-radius: 5px;
    padding: 5px;
    font-family: "Consolas", "Courier New", monospace;
}
QPlainTextEdit::placeholder {
    color: #666666;
}
QComboBox {
    background-color: #3c3c3c;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px;
    min-width: 150px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #2b2b2b;
    border: 1px solid #555555;
    selection-background-color: #007acc;
    color: #e0e0e0;
}
QPushButton {
    background-color: #3c3c3c;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px 10px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #4c4c4c;
    border: 1px solid #777777;
}
QPushButton#btn_generate {
    background-color: #4CAF50;
    color: white;
    border: none;
    font-size: 14px;
    padding: 10px;
}
QPushButton#btn_generate:hover {
    background-color: #45a049;
}
QPushButton#btn_generate:disabled {
    background-color: #2e5a30;
    color: #888888;
}
QStatusBar {
    background-color: #1e1e1e;
    color: #aaaaaa;
    border-top: 1px solid #444444;
}
QSplitter::handle {
    background-color: #555555;
    height: 2px;
}
"""

# --- Worker Thread for Non-Blocking API Calls ---
class OllamaWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, task_type, model_name=None, story_text=None):
        super().__init__()
        self.task_type = task_type
        self.model_name = model_name
        self.story_text = story_text

    def run(self):
        try:
            if self.task_type == 'scan':
                response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    self.finished.emit(models)
                else:
                    self.error.emit(f"Failed to fetch models: {response.status_code}")

            elif self.task_type == 'generate':
                system_prompt = (
                    "You are an expert creative writing coach. "
                    "Your goal is to help the user overcome writer's block. "
                    "Do NOT rewrite the story. "
                    "Analyze the provided text and output two sections: "
                    "1. 'Deep Questions': 3-5 thought-provoking questions to help the author explore characters or plot holes. "
                    "2. 'Continuation Suggestions': 3-5 concrete plot ideas or twists to help them write the next paragraph. "
                    "Keep the tone encouraging and inspiring."
                )

                payload = {
                    "model": self.model_name,
                    "prompt": f"Here is my story so far:\n\n{self.story_text}",
                    "system": system_prompt,
                    "stream": False
                }
                
                response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    self.finished.emit(data.get('response', 'No response generated.'))
                else:
                    self.error.emit(f"Generation failed: {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.error.emit("Cannot connect to Ollama. Is it running? (localhost:11434)")
        except Exception as e:
            self.error.emit(str(e))

# --- Main GUI Application ---
class WriterBlockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama Writer's Block Helper")
        self.setGeometry(100, 100, 900, 700)
        
        # Theme State
        self.is_dark_mode = False

        # Central Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # --- Top Section: Model Selection & Theme ---
        top_layout = QHBoxLayout()
        
        self.lbl_model = QLabel("Select Model:")
        self.lbl_model.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.combo_models = QComboBox()
        self.combo_models.setMinimumWidth(300)
        self.combo_models.addItem("-- Scan for Models --")
        
        self.btn_scan = QPushButton("🔄 Refresh")
        self.btn_scan.clicked.connect(self.scan_models)
        
        # Theme Toggle Button
        self.btn_theme = QPushButton("🌙 Dark Mode")
        self.btn_theme.setFixedWidth(120)
        self.btn_theme.clicked.connect(self.toggle_theme)
        
        top_layout.addWidget(self.lbl_model)
        top_layout.addWidget(self.combo_models)
        top_layout.addWidget(self.btn_scan)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_theme)
        main_layout.addLayout(top_layout)

        # --- Middle Section: Input & Output (Splitter) ---
        splitter = QSplitter(Qt.Vertical)
        
        # Input Area
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0,0,0,0)
        self.lbl_input = QLabel("Your Story So Far:")
        self.lbl_input.setFont(QFont("Arial", 10, QFont.Bold))
        self.txt_input = QPlainTextEdit()
        self.txt_input.setPlaceholderText("Paste your story or scene here...")
        self.txt_input.setFont(QFont("Consolas", 11))
        input_layout.addWidget(self.lbl_input)
        input_layout.addWidget(self.txt_input)
        
        # Output Area
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.setContentsMargins(0,0,0,0)
        self.lbl_output = QLabel("AI Suggestions:")
        self.lbl_output.setFont(QFont("Arial", 10, QFont.Bold))
        self.txt_output = QPlainTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setFont(QFont("Consolas", 11))
        output_layout.addWidget(self.lbl_output)
        output_layout.addWidget(self.txt_output)

        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)

        # --- Bottom Section: Action Button ---
        self.btn_generate = QPushButton("✨ Help Me Continue (Generate Suggestions)")
        self.btn_generate.setObjectName("btn_generate") # For specific CSS targeting
        self.btn_generate.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_generate.clicked.connect(self.generate_suggestions)
        main_layout.addWidget(self.btn_generate)

        # --- Status Bar ---
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Apply Initial Light Theme
        self.apply_theme()

        # Initial Scan
        self.scan_models()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        app = QApplication.instance()
        if self.is_dark_mode:
            app.setStyleSheet(DARK_THEME)
            self.btn_theme.setText("☀️ Light Mode")
        else:
            app.setStyleSheet(LIGHT_THEME)
            self.btn_theme.setText("🌙 Dark Mode")

    def scan_models(self):
        self.statusBar.showMessage("Scanning for Ollama models...")
        self.btn_scan.setEnabled(False)
        self.combo_models.setEnabled(False)
        
        self.worker = OllamaWorker(task_type='scan')
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_scan_finished(self, models):
        self.combo_models.clear()
        if not models:
            self.combo_models.addItem("No models found. Pull one via CLI.")
        else:
            self.combo_models.addItems(models)
        
        self.btn_scan.setEnabled(True)
        self.combo_models.setEnabled(True)
        self.statusBar.showMessage(f"Found {len(models)} models.")

    def generate_suggestions(self):
        model = self.combo_models.currentText()
        story = self.txt_input.toPlainText()

        if not model or model == "-- Scan for Models --" or "No models" in model:
            QMessageBox.warning(self, "No Model", "Please select a valid model first.")
            return
        
        if not story.strip():
            QMessageBox.warning(self, "Empty Story", "Please paste some story text first.")
            return

        # Lock UI during generation
        self.btn_generate.setEnabled(False)
        self.btn_generate.setText("⏳ Thinking...")
        self.txt_output.setPlaceholderText("Generating suggestions...")
        self.statusBar.showMessage("Generating suggestions...")

        self.worker = OllamaWorker(task_type='generate', model_name=model, story_text=story)
        self.worker.finished.connect(self.on_generate_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_generate_finished(self, response_text):
        self.txt_output.setPlainText(response_text)
        self.btn_generate.setEnabled(True)
        self.btn_generate.setText("✨ Help Me Continue (Generate Suggestions)")
        self.statusBar.showMessage("Suggestions generated.")

    def on_error(self, error_msg):
        QMessageBox.critical(self, "Error", error_msg)
        self.btn_generate.setEnabled(True)
        self.btn_generate.setText("✨ Help Me Continue (Generate Suggestions)")
        self.btn_scan.setEnabled(True)
        self.combo_models.setEnabled(True)
        self.statusBar.showMessage("Error occurred.")

# --- Run Application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set Fusion style for consistent look across OS
    app.setStyle("Fusion")
    
    window = WriterBlockApp()
    window.show()
    sys.exit(app.exec_())