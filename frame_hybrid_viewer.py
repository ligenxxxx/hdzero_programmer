import tkinter as tk
from tkinter import ttk


class frame_hybrid_viewer:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="Hybrid Viewer")

        self.scale_brightness = 0
        self.scale_contrast = 0
        self.scale_saturation = 0

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_columnconfigure(0, weight=0)
        self._frame.grid_columnconfigure(1, weight=0)
        self._frame.grid_columnconfigure(2, weight=0)

        self.init_image_setting()
        self.init_power_setting()

    def frame(self):
        return self._frame

    def on_brightness_scale_changed(self, value):
        self.scale_brigheness = int(float(value))
        self.brighrness_label.config(text=f"{self.scale_brigheness}")

    def on_contrast_scale_changed(self, value):
        self.scale_contrast = int(float(value))
        self.contrast_label.config(text=f"{self.scale_contrast}")
        
    def on_saturation_scale_changed(self, value):
        self.scale_saturation = int(float(value))
        self.saturation_label.config(text=f"{self.scale_saturation}")

    def init_image_setting(self):
        # brighrness
        row = 0
        label = ttk.Label(self._frame, text="Brightness")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        brightbess_scale = ttk.Scale(self._frame, from_=0, to=100, orient="horizontal",
                                     length=350, command=self.on_brightness_scale_changed)
        brightbess_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.brighrness_label =  ttk.Label(self._frame, text="0")
        self.brighrness_label.grid(row=row, column=2, sticky="w", padx=10)

        # contrast
        row += 1
        label = ttk.Label(self._frame, text="Contrast")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        contrast_scale = ttk.Scale(self._frame, from_=0, to=100, orient="horizontal",
                                   length=350, command=self.on_contrast_scale_changed)
        contrast_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.contrast_label =  ttk.Label(self._frame, text="0")
        self.contrast_label.grid(row=row, column=2, sticky="w", padx=10)

        # saturation
        row += 1
        label = ttk.Label(self._frame, text="Saturation")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        saturation_scale = ttk.Scale(self._frame, from_=0, to=100, orient="horizontal",
                                   length=350, command=self.on_saturation_scale_changed)
        saturation_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.saturation_label =  ttk.Label(self._frame, text="0")
        self.saturation_label.grid(row=row, column=2, sticky="w", padx=10)

    def on_cell_count_scale_changed(self, value):
        option = ["Auto", "2S", "3S", "4S"]
        
        self.cell_count = int(float(value))
        self.cell_count_label.config(text=option[self.cell_count])
    
    def on_warning_cell_voltage_scale_changed(self, value):
        self.warning_cell_voltage = int(float(value))
        self.warning_cell_voltage_label.config(text=f"{self.warning_cell_voltage/10}")
        
    
    def init_power_setting(self):
        row = 3
        label = ttk.Label(self._frame, text="Cell Count")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        cell_count_scale = ttk.Scale(self._frame, from_=0, to=3, orient="horizontal",
                                   length=350, command=self.on_cell_count_scale_changed)
        cell_count_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.cell_count_label = ttk.Label(self._frame, text="Auto")
        self.cell_count_label.grid(row=row, column=2, sticky="w", padx=10)
        
        row += 1
        label = ttk.Label(
            self._frame, text="Warning Cell Voltage")
        label.grid(row=4, column=0, sticky="w", padx=20)
        
        warning_cell_voltage_scale = ttk.Scale(self._frame, from_=28, to=42, orient="horizontal",
                                   length=350, command=self.on_warning_cell_voltage_scale_changed)
        warning_cell_voltage_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.warning_cell_voltage_label = ttk.Label(self._frame, text="2.8")
        self.warning_cell_voltage_label.grid(row=row, column=2, sticky="w", padx=10)
