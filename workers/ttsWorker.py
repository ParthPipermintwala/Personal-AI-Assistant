from core.speechEngine import speak

def ttsWorker(response_queue, stop_event, interrupt_event, mic_stop_event, ui):
    while True:
        if stop_event.is_set() and response_queue.empty():
            break
        response=response_queue.get()
        text=response["text"]
        isAlexa=response["isAlexa"]
        micAccess=response["micAccess"]
        ui.update_status("🎤 Speaking...")
        if not micAccess:
            mic_stop_event.set()
        interrupt_event.clear() # Clear interrupt event before speaking
        speak(text, interrupt_event, isAlexa)
        mic_stop_event.clear()
        response_queue.task_done()