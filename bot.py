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
stopFlag = False  # Flag to stop listeners
startX, startY, endX, endY = None, None, None, None  # Variables for region selection
selectingRegion = False  # Flag to track if the user is selecting a region
awaitingSelection = False  # Flag to track if the system is waiting for a region selection
ctrlShiftPressed = False  # Flag to detect Control + Shift combination
isRecording = False # Flag to tack wheter recording is ongoing
audioBuffer = []  # Stores recorded audio data
recordingStream = None # Variable to store the active recording stream

# Initialize OpenAI client
openaAIAPIKey = os.getenv("openaAIAPIKey")
client = openai.OpenAI(api_key=openaAIAPIKey)

# Function to capture screenshots and get text
def takeScreenshot(region=None):
    """ Captures a screenshot, extracts text, and appends it to compiledText. """
    global compiledText
    screenshot = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
    extractedText = pytesseract.image_to_string(screenshot)
    compiledText += "\n" + extractedText
    print("Screenshot taken and text extracted.")
    print(compiledText)

# Function to process text with AI and then show the result
def processWithAI(text):
     """ Uses OpenAI's GPT to analyze and generate a response based on the extracted text. """
    if not text.strip():
        print("No text to process.")
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "system", "content": "You are an AI assistant that processes text from screenshots and show a short result of the correct option, indicating the index of the response."},
            {"role": "user", "content": text}
        ]
    )

    print(response.choices[0].message.content)


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