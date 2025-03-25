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