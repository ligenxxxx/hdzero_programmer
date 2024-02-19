import tkinter as tk


class frame_programmer:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(self._parent, bg="gray")
        
        button1 = tk.Button(self._frame, text="Load Online Firmware")
        button1.grid(row=1, column=0, padx=5, pady=5)

        button2 = tk.Button(self._frame, text="Load Local Firmware")
        button2.grid(row=1, column=1,padx=5, pady=5)

        button3 = tk.Button(self._frame, text="Erase & Flash")
        button3.grid(row=1, column=2, padx=5, pady=5)
        
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)
        
    def frame(self):
        return self._frame