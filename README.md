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

![Program Workflow](flow.svg)

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

---

## 🎛️ Enabling Stereo Mix on Windows  

If you want to **record system audio**, you must enable **Stereo Mix** in Windows. Follow these steps to check availability and enable it:  

### **🔹 Phase 1: Enable Stereo Mix via Control Panel**  
1. Open **Control Panel**.  
2. Click on **Hardware and Sound**.  
3. Click on **Sound** (**Administración de dispositivos de audio**).  
4. Go to the **Recording** tab.  
5. Find **Stereo Mix**, **double-click** it.  
6. In **Device Usage**, select **Enable** (**Habilitar**).  
7. Click **Apply**.  

### **🔹 Phase 2: Set Stereo Mix as the Default Device**  
1. Open **Settings** → **Sound**.  
2. Scroll to **Input Devices**.  
3. Select **Stereo Mix** as the **default recording device**  

---

## 🔹 Use Cases of SunAI

### 📄 1. Automated Information Extraction in Business Environments
**Example:** A support agent needs to extract information from multiple open PDF documents without manually copying text. SunAI allows capturing the text with a simple shortcut and generates an automatic summary.

### 📑 2. Real-Time Screenshot Processing
**Example:** Researchers or journalists can take screenshots of articles, process them with OCR, and get an AI-generated summary within seconds, avoiding manual transcription.

### 🎤 3. Audio Transcription for Meetings or Classes
**Example:** A student records a university lecture and later uses SunAI to convert the audio into text, generating an AI-powered summary.

### 🤖 4. Assistance for Visually or Motor-Impaired Users
**Example:** A user with vision problems uses SunAI to capture on-screen text and obtain a spoken summary (if integrated with a TTS system).

### 🎮 5. Data Capture in Games or Applications Without Copy-Pasting
**Example:** An MMORPG player needs to quickly extract quest information or statistics without manually typing, using screenshots processed by SunAI.

### 🏢 6. Workflow Optimization in IT Support
**Example:** An IT technician can take error screenshots, extract the error code, and use AI to generate possible solutions without manually searching in forums.

### 📊 7. Financial Document Analysis and Summarization
**Example:** A financial analyst uses SunAI to capture bank statements or PDF reports and generate an automated AI summary.

### 📰 8. Real-Time News and Report Summarization
**Example:** A journalist captures parts of online articles and generates an AI summary for quick understanding.

### 📷 9. Data Extraction from Images or Graphs
**Example:** A data scientist captures graphs from a report and extracts text or values for easier analysis.

### 🕵️ 10. Security and Cybersecurity Support
**Example:** A security analyst uses SunAI to capture logs of attacks or alerts on the screen and analyze the data with AI.

---

## 🚀 Future Expansions and Improvements:
✔ **Integration with voice APIs (TTS)** to read the results aloud.  
✔ **Automatic language detection in OCR** for better compatibility.  
✔ **Scheduled capture mode** to monitor and extract text automatically at set intervals.  
✔ **Implement a User Interface (UI)** to enhance user experience and improve accessibility.

---

### **Install and run**
Apart from cloning the repository, you also need to create a `.env` file to store the `OPENAI_API_KEY`.
```sh
pip install pyautogui pytesseract pynput pillow openai python-dotenv numpy sounddevice speechrecognition scipy
python script.py "Your OpenAI system role prompt"
