import threading
from queue import Queue
from workers.processorWorker import processorWorker
from workers.ttsWorker import ttsWorker
from workers.micWorker import micWorker
from ui.appUi import appUi

if __name__ == "__main__":
    ui=appUi() # Create the UI instance
    
    text_queue = Queue()
    response_queue = Queue()
    
    mic_stop_event = threading.Event() # Event to signal threads to stop
    stop_event = threading.Event() # Event to signal threads to stop
    interrupt_event = threading.Event() # Event to signal interruption
    
    response_queue.put({
        "text": "Welcome to voice assistant.",
        "isAlexa": False,
        "micAccess":False
    })
    
    # Create and start threads
    mic_thread = threading.Thread(target=micWorker, args=(text_queue, stop_event, mic_stop_event, ui), daemon=True) # Daemon thread will automatically exit when the main program exits
    process_thread = threading.Thread(target=processorWorker, args=(text_queue, response_queue, stop_event, interrupt_event, ui), daemon=True)
    tts_thread = threading.Thread(target=ttsWorker, args=(response_queue, stop_event, interrupt_event, mic_stop_event, ui), daemon=True)
    
    tts_thread.start()
    process_thread.start()
    mic_thread.start()
    
    ui.run() # Start the UI (this will block until the UI is closed)
    
    # Tell all threads to stop
    stop_event.set()
    mic_stop_event.set()
    interrupt_event.set()
    
    # main Wait for threads to finish (with timeout to prevent hanging)
    mic_thread.join(timeout=1)
    process_thread.join(timeout=1)
    tts_thread.join(timeout=1)