from google import genai  
import os
from commands.commandHandlers import (
    handle_open,
    handle_close,
    handle_play,
    handle_system,
    handle_news,
    handle_search,
    handle_time,
)

if os.getenv("GEMINI_API_KEY") :
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()

commandRouter = {
    "open": handle_open,
    "close": handle_close,
    "play": handle_play,
    "sleep": handle_system,
    "restart": handle_system,
    "shutdown": handle_system,
    "hibernate": handle_system,
    "lock": handle_system,
    "news": handle_news,
    "headlines": handle_news,
    "search": handle_search,
    "time": handle_time,
}

def routeCommand(command, isAlexa, response_queue):
    for keyword, handler in commandRouter.items():
        if keyword in command:
            handler(command, isAlexa, response_queue)
            return
    
    if os.getenv("GEMINI_API_KEY") :
        response_queue.put({ "text": "command not recognized.", "isAlexa": isAlexa, "micAccess": True })
        return 
    
    # If no command handler is found, use the AI to generate a response.
    try:
        prompt = f"""
        Answer the following question briefly.
        Limit the answer to 3 or 4 short lines.
        Question:
        {command}
        """
        if len(command.split()) >= 2:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            response_queue.put({
                "text": response.text,
                "isAlexa": isAlexa,
                "micAccess": True
            })
            
    except Exception as e:
        response_queue.put({
            "text": "AI quota exceeded.",
            "isAlexa": isAlexa,
            "micAccess": True
        })
