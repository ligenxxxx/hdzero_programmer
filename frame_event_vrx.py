import tkinter as tk


class frame_event_vrx:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="Event VRX")
        
    def frame(self):
        return self._frame
