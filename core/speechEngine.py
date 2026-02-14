import speech_recognition as sr
import pyttsx3
import time
from core.config import *

recognizer = sr.Recognizer()
recognizer.energy_threshold = energy_threshold
recognizer.pause_threshold = pause_threshold 
recognizer.phrase_threshold = phrase_threshold 
recognizer.dynamic_energy_threshold = dynamic_energy_threshold
recognizer.non_speaking_duration = non_speaking_duration 

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 175)

voices = engine.getProperty('voices')
male_voice = voices[0].id
female_voice = voices[1].id if len(voices) > 1 else voices[0].id

def speak(text, interrupt_event, isAlexa=False):
    try:
        engine.stop()  # clear previous speech

        voice = female_voice if isAlexa else male_voice
        engine.setProperty('voice', voice)

        engine.say(text)

        # Non-blocking speech loop
        engine.startLoop(False)

        while engine.isBusy():
            if interrupt_event.is_set():
                engine.stop()   # interrupt immediately
                break
            engine.iterate()
            time.sleep(0.01)   # prevents CPU spike

        engine.endLoop()

    except Exception:
        pass
