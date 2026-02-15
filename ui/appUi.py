import tkinter as tk
import queue

class appUi:
    def __init__(self):
        self.root = tk.Tk()

        self.root.attributes("-alpha", 0.95)  # transparent background  
        
        # BLACK BACKGROUND
        self.bg = "#000000"
        self.root.configure(bg=self.bg)
        
        # Window size
        width = self.root.winfo_screenwidth()
        self.root.geometry(f"{width}x40+0+0")
        self.root.minsize(width, 40)
        self.root.maxsize(width, 40)

        # Keeps window above all other apps
        self.root.attributes("-topmost", True)

        # Borderless window
        self.root.overrideredirect(True)

        # Drag support
        self.root.bind("<Button-1>", self.start_move) # left mouse button press
        self.root.bind("<B1-Motion>", self.move) # Move mouse while holding left button

        self.offset_x = 0
        self.offset_y = 0

        # Thread-safe queue
        self.ui_queue = queue.Queue()

        # A dynamic variable linked to a label. When the variable changes, the label updates automatically.
        self.status_text = tk.StringVar(value="Starting...")
        self.heard_text = tk.StringVar(value="")

        self.build_ui()

        # Runs process_queue() every 100ms.
        self.root.after(100, self.process_queue)

    # UI Layout
    def build_ui(self):
        frame = tk.Frame(self.root, bg=self.bg)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        frame.grid_columnconfigure(0, weight=1)  # Title 
        frame.grid_columnconfigure(1, weight=3)  # Status
        frame.grid_columnconfigure(2, weight=2)  # Heard
        
        tk.Label(
            frame,
            text="🧠 Personal Assistant",
            fg="#00FFFF",
            bg=self.bg,
            font=("Segoe UI Emoji", 13, "bold"),
        ).grid(row=0, column=0, sticky="w") 

        # Status line
        status = tk.Label(
            frame,
            textvariable=self.status_text,
            fg="#00FF88", 
            bg=self.bg,
            font=("Segoe UI Emoji", 12),
        )
        status.grid(row=0, column=1, sticky="nsew")
        heard = tk.Label(
            frame,
            textvariable=self.heard_text,
            fg="#FFFFFF",
            bg=self.bg,
            font=("Segoe UI Emoji", 12),
        )
        heard.grid(row=0, column=2, sticky="w")

        # Close button (top-right)
        close_btn = tk.Label(
            frame,
            text="✕",
            fg="#FF4444",
            bg=self.bg,
            font=("Segoe UI", 14, "bold"),
            cursor="hand2"
        )
        close_btn.place(relx=1.0, x=-10, y=0, anchor="ne")
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())

    # Drag Window
    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def move(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    # Thread-safe Updates
    def update_status(self, text):
        self.ui_queue.put(("status", text))

    def update_heard(self, text):
        self.ui_queue.put(("heard", text))

    def process_queue(self):
        while not self.ui_queue.empty():
            kind, value = self.ui_queue.get()

            if kind == "status":
                self.status_text.set(value)

            elif kind == "heard":
                self.heard_text.set(f"Heard :- {value}")

        self.root.after(100, self.process_queue)

    # Run
    def run(self):
        self.root.mainloop()

    def exit(self):
        self.root.destroy()