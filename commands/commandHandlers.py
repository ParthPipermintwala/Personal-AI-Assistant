import webbrowser
import subprocess
import os
import requests
from datetime import datetime
from data.musicData import songs
from data.appData import apps

def handle_open(command, isAlexa, response_queue):
    name = command.replace("open", "").strip()
    if name =="":
        response_queue.put({"text": "Please specify what to open.", "isAlexa": isAlexa, "micAccess": False})
        return
    if name in apps:
        response_queue.put({"text": f"Opening {name}", "isAlexa": isAlexa, "micAccess": False})
        try:
            subprocess.Popen(f"start {apps[name]}", shell=True)
        except Exception as e:
            webbrowser.open(f"https://www.{name}.com")
        return
    webbrowser.open(f"https://www.{name}.com")


def handle_close(command, isAlexa, response_queue):
    name = command.replace("close", "").strip()
    if name =="":
        response_queue.put({"text": "Please specify what to close.", "isAlexa": isAlexa, "micAccess": False})
        return
    if name in apps:  
        proc = apps[name].split("\\")[-1]
        if not proc.lower().endswith(".exe"):
            proc += ".exe"
        response_queue.put({"text": f"Closing {name}", "isAlexa": isAlexa, "micAccess": False})
        try:
            subprocess.Popen(["taskkill", "/F", "/IM", proc], shell=True)
        except Exception as e:
            response_queue.put({"text": f"Failed to close {name}", "isAlexa": isAlexa, "micAccess": False})
        return

    response_queue.put({"text": f"{name} not found", "isAlexa": isAlexa, "micAccess": False})


def handle_play(command, isAlexa, response_queue):
    name = command.replace("play", "").strip()
    if name =="":
        response_queue.put({"text": "Please specify what to play.", "isAlexa": isAlexa, "micAccess": False})
        return
    if name in songs:
        response_queue.put({"text": f"Playing {name}", "isAlexa": isAlexa, "micAccess": False})
        webbrowser.open(songs[name])
        return
    webbrowser.open(f"https://www.youtube.com/results?search_query={name}")


def handle_system(command, isAlexa, response_queue):
    if "sleep" in command:
        response_queue.put({"text": "Sleeping the computer", "isAlexa": isAlexa, "micAccess": False})
        subprocess.Popen(["powershell","-Command","Start-Sleep -Milliseconds 300; rundll32.exe powrprof.dll,SetSuspendState 0,1,0"])
        return

    if "restart" in command:
        response_queue.put({"text": "Restarting the computer", "isAlexa": isAlexa, "micAccess": False})
        subprocess.Popen(["powershell","-Command","Restart-Computer -Force"])
        return

    if "shutdown" in command:
        response_queue.put({"text": "Shutting down the computer", "isAlexa": isAlexa, "micAccess": False})
        subprocess.Popen(["powershell","-Command","Stop-Computer -Force"])
        return

    if "hibernate" in command:
        response_queue.put({"text": "Hibernating the computer", "isAlexa": isAlexa, "micAccess": False})
        subprocess.Popen(["powershell","-Command","shutdown /h"])
        return

    if "lock" in command:
        response_queue.put({"text": "Locking the computer", "isAlexa": isAlexa, "micAccess": False})
        subprocess.Popen(["powershell","-Command","rundll32.exe user32.dll,LockWorkStation"])
        return

    response_queue.put({"text": "System command not recognized", "isAlexa": isAlexa,"micAccess": False})

def handle_news(command, isAlexa, response_queue):
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        response_queue.put({"text": "API key not configured.", "isAlexa": isAlexa, "micAccess": False})
        return

    try:
        res = requests.get(
            f"https://newsdata.io/api/1/latest?apikey={api_key}&q=technology",
            timeout=5
        )
    except requests.RequestException:
        response_queue.put({"text": "Failed to fetch news.", "isAlexa": isAlexa, "micAccess": False})
        return

    if res.status_code == 200:
        data = res.json()
        if data.get("status") == "success":
            for article in data.get("results", [])[:5]:
                response_queue.put({
                    "text": article["title"],
                    "isAlexa": isAlexa,
                    "micAccess":True
                })


def handle_search(command, isAlexa, response_queue):
    query = command.replace("search", "").strip()
    if query =="":
        response_queue.put({"text": "Please specify what to search for.", "isAlexa": isAlexa,"micAccess": False})
        return
    response_queue.put({"text": f"Searching for {query}", "isAlexa": isAlexa,"micAccess": False})
    webbrowser.open(f"https://www.google.com/search?q={query}")


def handle_time(command, isAlexa, response_queue):
    now = datetime.now().strftime("%H:%M:%S")
    response_queue.put({"text": f"The current time is {now}", "isAlexa": isAlexa,"micAccess": False})
