import tkinter as tk
from tkinter import ttk


class frame_statusbar:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_rowconfigure(0, weight=1)

        self.init_progress_bar()
        self.progress_bar_set_value(0)

    def frame(self):
        return self._frame

    def status_label_set_text(self, text):
        pass
    def init_progress_bar(self):
        self.bar = ttk.Progressbar(
            self._frame, orient="horizontal", mode="determinate")
        self.bar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    def progress_bar_set_value(self, value):
        self.bar["value"] = value
