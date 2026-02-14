import queue
import os
from commands.commandRouter import routeCommand

def processorWorker(text_queue, response_queue, stop_event, interrupt_event, ui):
    while True:
        try:
            command = text_queue.get(timeout=0.5)
        except queue.Empty:
            if stop_event.is_set():
                break
            continue
        os.system("cls")

        ui.update_status("⚙️ Processing command...")
        if "help" in command.replace(" ","") or "use" in command.replace(" ",""):
            response_queue.put({
                "text": """To use this assistant, start your command with 'Jarvis' for male voice or 'Alexa' for female voice.
                    Available actions include opening or closing apps and websites, 
                    playing music, searching on Google, getting news headlines, 
                    checking the current time, and controlling the system 
                    (sleep, restart, shutdown, hibernate, lock).
                    Say 'stop' to interrupt current speech, and 'exit' to close the assistant.""",
                "isAlexa": "alexa" in command,
                "micAccess": True
            })
            text_queue.task_done()
            continue
        
        isAlexa = "alexa" in command
        isJarvis = "jarvis" in command
        
        if not (isAlexa or isJarvis):
            text_queue.task_done()
            continue

        command = command.replace("alexa", "").replace("jarvis", "").strip()
            
        # Stop the program
        if "stop" in command :
            interrupt_event.set()
            try:
                while True:
                    # get item without blocking and remove it from the queue, if queue is empty it raises queue.Empty
                    response_queue.get_nowait() 
                    response_queue.task_done()
            except queue.Empty:
                pass
            text_queue.task_done()
            continue
        
        if "exit" in command or "quit" in command or "leave" in command:
            interrupt_event.set()
            response_queue.put({
                "text": "Exiting the assistant. Goodbye!",
                "isAlexa": isAlexa,
                "micAccess": False
            })
            stop_event.set()
            text_queue.task_done()
            continue
        
        routeCommand(command, isAlexa, response_queue)
        
        text_queue.task_done()
        