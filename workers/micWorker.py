import speech_recognition as sr
from core.speechEngine import recognizer

def micWorker(text_queue,stop_event,mic_stop_event,ui):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        
        while not stop_event.is_set():
            if mic_stop_event.is_set():
                continue
            try:
                ui.update_status("🎙️Listening...")
                audio=recognizer.listen(source,timeout=10,phrase_time_limit=8)
                
                ui.update_status("⚙️ Recognizing...")
                text=recognizer.recognize_google(audio, language="en-IN").lower()
                
                # True if at least one value is True
                if any(w in text for w in ["jarvis", "alexa", "help", "use"]):
                    ui.update_heard(text)
                    text_queue.put(text)
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                ui.update_status(" Error:- " + str(e))