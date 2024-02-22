import tkinter as tk
from tkinter import ttk


class frame_statusbar:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent, bg="red")

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=0)
        self._frame.grid_rowconfigure(0, weight=1)

        self.init_status_label()
        self.status_label_set_text("Downloading Release Note ...")
        self.init_progress_bar()
        self.progress_bar_set_value(100)

    def frame(self):
        return self._frame

    def init_status_label(self):
        font = ("")
        self.label = ttk.Label(
            self._frame, text=" ", border=2, relief='ridge', width=30)
        self.label.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    def status_label_set_text(self, text):
        self.label["text"] = text

    def init_progress_bar(self):
        self.bar = ttk.Progressbar(
            self._frame, orient="horizontal", mode="determinate")
        self.bar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    def progress_bar_set_value(self, value):
        self.bar["value"] = value
        print(value)
