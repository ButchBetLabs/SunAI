import time  # For delays
import pyautogui  # For additional automation
import pytesseract  # For OCR (Optical Character Recognition) text extraction
import threading  # For handling multiple tasks
from pynput import mouse, keyboard  # For detecting mouse clicks and keyboard inputs
from PIL import ImageGrab  # For taking screenshots
import openai  # For AI processing (ChatGPT)
import os  # For file operations
from dotenv import load_dotenv  # For loading environment variables
import numpy as np  # For efficient numerical operations, particularly with large arrays like the audio buffer
import sounddevice as sd # To audio recording
import speech_recognition as sr # For trascribing audio to text
from scipy.io.wavfile import write # Allows us to save audio data as a WAV file

# Load environment variables
load_dotenv()

# Global Variables
clickCount = 0  # Stores the number of clicks detected
compiledText = ""  # Stores concatenated OCR text
startX, startY, endX, endY = None, None, None, None  # Variables for region selection
selectingRegion = False  # Flag to track if the user is selecting a region
ctrlAltPressed = False  # Flag to detect Control + Shift combination
isRecording = False # Flag to tack wheter recording is ongoing
audioBuffer = []  # Stores recorded audio data
recordingStream = None # Variable to store the active recording stream

# Initialize OpenAI client
openaAIAPIKey = os.getenv("openaAIAPIKey")
client = openai.OpenAI(api_key=openaAIAPIKey)

# Function to capture screenshots and process text
def takeScreenshot(region=None):
    """ Captures a screenshot, extracts text, and appends it to compiledText. """
    global compiledText
    screenshot = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
    extractedText = pytesseract.image_to_string(screenshot)
    compiledText += "\n" + extractedText
    print("Screenshot taken and text extracted.")
    print(compiledText)

# Function to process compiled text with AI
def processCompiledText():
    """ Processes the compiled text with AI and saves the result. """
    if not compiledText.strip():
        print("No text to process.")
        return

    processedText = processWithAI(compiledText)
    print(processedText)
    print("AI processing completed.")

# Function to process text with AI
def processWithAI(text):
    """ Uses OpenAI's GPT to analyze and generate a response based on the extracted text. """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "system", "content": "You are an AI assistant that processes text from screenshots and show a short result of the correct option, indicating the index of the response."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# Function to clear compiled text
def clearCompiledText():
    """ Clears the stored text data. """
    global compiledText
    compiledText = ""
    print("Compiled text cleared.")

# Function to get the Stereo Mix 
def getStereoMixDevice():
    """Finds the device ID for Stereo Mix if available."""
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if "Stereo Mix" in device["name"]:
            print(f"Stereo Mix ID: {idx}")
            return idx
    return None

# Function to handle audio recording
def recordAudio():
    """ Starts recording audio and stores data in audioBuffer. """
    global audioBuffer, recordingStream, isRecording
    audioBuffer = []
    stereo_mix_device = getStereoMixDevice()
    if stereo_mix_device is None:
        print("Stereo Mix not found. Please enable it in the audio settings.")
        return
    
    def callback(indata, frames, time, status):
        if status:
            print(status)
        audioBuffer.append(indata.copy())
    
    recordingStream = sd.InputStream(
        callback=callback, samplerate=44100, channels=2, device=stereo_mix_device, dtype='int16'
    )
    recordingStream.start()
    isRecording = True
    print("Recording from Stereo Mix...")


# Function to stop the recording and process the audio
def stopRecording():
    """ Stops the recording, transcribes audio, and appends the text to compiledText. """
    global recordingStream, audioBuffer, isRecording, compiledText
    if not recordingStream:
        return
    
    recordingStream.stop()
    recordingStream.close()
    recordingStream = None
    isRecording = False
    
    if not audioBuffer:
        print("No audio recorded.")
        return
    
    recordedAudio = np.concatenate(audioBuffer, axis=0)
    file_path = "temp_audio.wav"
    write(file_path, 44100, recordedAudio)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio_chunk = recognizer.record(source, duration=10)  # 10 seconds per chunk
            if len(audio_chunk.frame_data) == 0:
                break  # Stop when no more data

            try:
                chunk_text = recognizer.recognize_google(audio_chunk)
                compiledText += "\n" + chunk_text
                # print("Chunk transcribed:", chunk_text)  # Debugging output
            except sr.UnknownValueError:
                print("Chunk unclear, skipping...")
            except sr.RequestError:
                print("Speech-to-text service unavailable.")
        
        with open("transcription.txt", "w", encoding="utf-8") as file:
            file.write("\n" + compiledText)
    
    print(compiledText)
    print("Transciption finished...")

# Function to mouse click listener
def onClick(x, y, button, pressed):
    """ Detects mouse clicks and triggers the corresponding actions. """
    global clickCount, startX, startY, endX, endY, selectingRegion
    
    if selectingRegion:
        if pressed:
            startX, startY = x, y  # Start point of selection
        else:
            endX, endY = x, y  # End point of selection
            selectingRegion = False
            print("Taking screenshot of selected region...")
            threading.Thread(target=takeScreenshot, args=((startX, startY, endX, endY),)).start()
            return
    
    if pressed:
        clickCount += 1
        threading.Thread(target=resetClickCount).start()

# Function to reset click count and execute actions based on clicks        
def resetClickCount():
    global clickCount, isRecording
    time.sleep(1.5)

    if clickCount == 3:
        print("Processing AI analysis...")
        threading.Thread(target=processCompiledText).start()
    elif clickCount == 4:
        threading.Thread(target=clearCompiledText).start()
    elif clickCount == 5:
        if isRecording:
            # Stop the recording and display message
            print("Recording finished...")
            threading.Thread(target=stopRecording).start()
            # Set isRecording to False as recording is stopped
            isRecording = False
        else:
            # Start recording and display message
            print("Recording in progress...")
            threading.Thread(target=recordAudio).start()
            # Set isRecording to True as recording is started
            isRecording = True

    clickCount = 0

# Function to reset click count and execute actions based on clicks
def resetClickCount():
    """ Waits and processes actions based on the number of clicks. """
    global clickCount, isRecording

    time.sleep(1.5)

    if clickCount == 3:
        print("Processing AI analysis...")
        threading.Thread(target=processCompiledText).start()
    elif clickCount == 4:
        threading.Thread(target=clearCompiledText).start()
    elif clickCount == 5:
        if isRecording:
            print("Recording finished...")
            threading.Thread(target=stopRecording).start()
            isRecording = False
        else:
            print("Recording in progress...")
            threading.Thread(target=recordAudio).start()
            isRecording = True
            
    clickCount = 0
    print("Click count reseted")


# Function to keyboard listener to detect Control + Shift
def onKeyPress(key):
    global ctrlAltPressed, selectingRegion

    try:
        if key == keyboard.Key.esc:
            print("Stopping listeners...")
            return False  # Stops the keyboard listener
        
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrlAltPressed = True
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            if ctrlAltPressed:
                print("Press and drag the mouse to select a region...")
                selectingRegion = True
                ctrlAltPressed = False
    except AttributeError:
        pass

# Keyboard listener to reset Control + Shift flag
def onKeyRelease(key):
    global ctrlAltPressed, selectingRegion
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrlAltPressed = False
    if key in (keyboard.Key.alt_l, keyboard.Key.alt_r) and selectingRegion:
        selectingRegion = False
        print("Region selection cancelled.")

# Start mouse and keyboard listeners
print("Mouse and keyboard listeners started. Press ESC to stop.")
with keyboard.Listener(on_press=onKeyPress, on_release=onKeyRelease) as keyboardListener:
    with mouse.Listener(on_click=onClick) as mouseListener:
        keyboardListener.join()
        mouseListener.stop()  