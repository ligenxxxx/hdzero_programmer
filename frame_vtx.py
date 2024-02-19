import tkinter as tk


class frame_vtx:
    def __init__(self, parent, winWidth, winHeight):
        self._parent = parent
        
        # main frame
        self._frame = tk.Frame(parent, bg="yellow")
        parent.add(self._frame, text="VTX")
        
        # top frame
        self._top_frame = tk.Frame(self._frame, bg="red")
        self._top_frame.grid(row=0, column=0, sticky="nsew")
        
        # bottom frame
        self._bottom_frame = tk.Frame(self._frame, bg="gray")
        self._bottom_frame.grid(row=1, column=0, sticky="nsew")

        # weight
        self._frame.grid_rowconfigure(0, weight=7)
        self._frame.grid_rowconfigure(1, weight=3)
        self._frame.grid_columnconfigure(0, weight=1)

    def frame(self):
        return self._frame
    
    def top_frame(self):
        return self._top_frame
    
    def bottom_frame(self):
        return self._bottom_frame