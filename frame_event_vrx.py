import tkinter as tk
from frame_programmer import frame_programmer


class frame_event_vrx:
    def __init__(self, parent, winWidth, winHeight):
        self._parent = parent

        # main frame
        self._frame = tk.Frame(parent, bg="blue")
        parent.add(self._frame, text="Event VRX")

    def frame(self):
        return self._frame
