import tkinter as tk
from frame_programmer import frame_programmer


class frame_vtx:
    def __init__(self, parent, winWidth, winHeight):
        self._parent = parent
        
        # main frame
        self._frame = tk.Frame(parent, bg="red")
        parent.add(self._frame, text="VTX")

    def frame(self):
        return self._frame