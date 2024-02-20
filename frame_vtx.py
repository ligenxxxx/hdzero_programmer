import tkinter as tk


class frame_vtx:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent, bg="red")
        parent.add(self._frame, text="VTX")

    def frame(self):
        return self._frame
