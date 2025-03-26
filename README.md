# 📌 SunAI

## 📖 Overview
This application automates **OCR-based text extraction**, **AI text processing**, and **audio transcription**.  
It works using **mouse clicks & keyboard shortcuts** to trigger different functions.

---

## 📦 Dependencies
This script requires the following **Python libraries**:
- `time` → Delay execution.
- `pyautogui` → GUI automation.
- `pytesseract` → Optical Character Recognition (OCR).
- `threading` → Multi-threading for concurrent execution.
- `pynput` → Listen to **mouse and keyboard** events.
- `PIL.ImageGrab` → Capture screenshots.
- `openai` → Process text with **ChatGPT API**.
- `os` & `dotenv` → Handle **environment variables**.
- `numpy` → Efficient numerical operations (used for audio processing).
- `sounddevice` → **Record system audio**.
- `speech_recognition` → Convert speech **to text**.
- `scipy.io.wavfile.write` → Save audio as a **WAV file**.
- `sys` → Handle **command-line arguments**.

---

## 📜 Program Workflow

Here’s a **visual flowchart** of how the program works:

![Program Workflow]()

---

## 🖱 Mouse Click Actions

| Clicks | Action |
|--------|----------------------------------|
| **3 Clicks** | 🤖 Process Extracted Text with OpenAI |
| **4 Clicks** | 🗑 Clear Stored Text |
| **5 Clicks** | 🎤 Start/Stop Audio Recording |

---

## ⌨️ Keyboard Shortcuts

| Key Combination | Action |
|----------------|----------------------------------|
| `Ctrl + Alt + Drag Mouse` | 📸 Capture Screenshot |
| `ESC` | 🔴 Stop Program |

---

## 📸 Screenshot & OCR Workflow
1. **Press `Ctrl + Alt`** to enable selection mode.
2. **Drag the mouse** to select a region.
3. A screenshot is captured & **text is extracted** via **OCR**.
4. The extracted text is **stored** for AI processing.

---

## 📊 AI Processing Workflow (Triggered by 3 Clicks)
1. Sends **extracted text** to OpenAI’s GPT.
2. AI **analyzes and generates** a response.
3. **Displays the processed output**.

---

## 🎙 Audio Recording & Transcription (Triggered by 5 Clicks)

### 🔴 Start Recording
1. Detects **Stereo Mix** for system audio.
2. **Records and buffers** audio input.
3. Saves the recording as **WAV file**.

### 🛑 Stop Recording & Transcribe
1. Stops **recording**.
2. **Transcribes audio** to text using Google’s Speech Recognition.
3. Saves the **transcription** for AI processing.

---

## 🛑 Stopping the Application
1. **User presses ESC**.
2. **Keyboard & mouse listeners stop**.
3. **Program exits cleanly**.



### **Install and run**
```sh
pip install pyautogui pytesseract pynput pillow openai python-dotenv numpy sounddevice speechrecognition scipy
python script.py "Your OpenAI system role prompt"