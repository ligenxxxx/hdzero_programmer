import tkinter as tk
from tkinter import ttk
import ctypes
import global_var

class frame_hybrid_viewer:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="Hybrid Viewer")
        
        self.dll_name = "CH341DLL.DLL"
        self.color_background = "#303030"
        self.color_label = "white"
        
        self.heart_cnt = 0
        self.addr_usb_heart = 0x13
        self.addr_usb_write_fpga_device = 0x65  # 7bit address
        self.addr_usb_write_brightness = 0x14
        self.addr_usb_write_contrast = 0x15
        self.addr_usb_write_saturation = 0x16
        self.addr_usb_write_backlight = 0x17
        self.addr_usb_write_cell_count = 0x18
        self.addr_usb_write_warning_cell_voltage = 0x19
        
        self.brightness_min = 0
        self.brightness_max = 254
        self.contrast_min = 0
        self.contrast_max = 254
        self.saturation_min = 0
        self.saturation_max = 254
        self.backlight_min = 1
        self.backlight_max = 100
        self.cell_count_min = 1     # 1 auto 
        self.cell_count_max = 5
        self.warning_cell_voltage_min = 28
        self.warning_cell_voltage_max = 42

        self.brightness_scale = 0
        self.contrast_scale = 0
        self.saturation_scale = 0
        self.backlight_scale = 0
        self.cell_count_scale = 0
        self.warning_cell_voltage_scale = 0
        
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)

        self._frame.grid_columnconfigure(0, weight=0)
        self._frame.grid_columnconfigure(1, weight=0)
        self._frame.grid_columnconfigure(2, weight=0)

        self.init_image_setting()
        self.init_power_setting()
        
        try:
            self.dll = ctypes.WinDLL(self.dll_name)
        except:
            print("please install driver")
                
    def usb_heart(self):
        self.heart_cnt += 1
        if self.heart_cnt == 255:
            self.heart_cnt = 0
        self.write_i2c(self.addr_usb_heart, self.heart_cnt)
    
    def write_i2c(self, addr, byte):
        print(f"addr:{addr:x}  byte: {byte:d}")
        self.dll.CH341WriteI2C(0, self.addr_usb_write_fpga_device, addr, byte)    
        
    def write_brightness(self, b):
        if global_var.brightness != b:
            global_var.brightness = b
            self.write_i2c(self.addr_usb_write_brightness, b)
            print(f"write_brightness {b}")

    def write_contrast(self, c):
        if global_var.contrast != c:
            global_var.contrast = c
            self.write_i2c(self.addr_usb_write_contrast, c)
            print(f"write_contrast {c}")

    def write_saturation(self, s):
        if global_var.saturation != s:
            global_var.saturation = s
            self.write_i2c(self.addr_usb_write_saturation, s)
            print(f"write_saturation {s}")

    def write_backlight(self, l):
        if global_var.backlight != l:
            global_var.backlight = l
            self.write_i2c(self.addr_usb_write_backlight, l)
            print(f"write_backlight {l}")

    def write_setting(self, b, c, s, l):
        """write setting from vrx.
        usually used for sync vrx setting.
        NOTE: Must run after setting_enable
        """

        self.write_brightness(b)
        self.write_contrast(c)
        self.write_saturation(s)
        self.write_backlight(l)
                
        # update scale
        self.brightness_scale.set(b)
        self.contrast_scale.set(c)
        self.saturation_scale.set(s)
        self.backlight_scale.set(l)

        # update label        
        self.brightness_label.config(text=f'{b}')
        self.contrast_label.config(text=f'{c}')
        self.saturation_label.config(text=f'{s}')
        self.backlight_label.config(text=f'{l}')
        
    def setting_disable(self):
        self.brightness_scale.configure(state="disabled")
        self.contrast_scale.configure(state="disabled")
        self.saturation_scale.configure(state="disabled")
        self.backlight_scale.configure(state="disabled")
        self.cell_count_scale.configure(state="disabled")
        self.warning_cell_voltage_scale.configure(state="disabled")

    def setting_enable(self):
        self.brightness_scale.configure(state="normal")
        self.contrast_scale.configure(state="normal")
        self.saturation_scale.configure(state="normal")
        self.backlight_scale.configure(state="normal")
        self.cell_count_scale.configure(state="normal")
        self.warning_cell_voltage_scale.configure(state="normal")
        
    def frame(self):
        return self._frame

    def on_brightness_scale_changed(self, value):
        self.brightness_label.config(text=f"{int(float(value))}")
        self.write_brightness(int(float(value)))

    def on_contrast_scale_changed(self, value):
        self.contrast_label.config(text=f"{int(float(value))}")
        self.write_contrast(int(float(value)))

    def on_saturation_scale_changed(self, value):
        self.saturation_label.config(text=f"{int(float(value))}")
        self.write_saturation(int(float(value)))

    def on_backlight_scale_changed(self, value):
        self.backlight_label.config(text=f"{int(float(value))}")
        self.write_backlight(int(float(value)))

    def init_image_setting(self):
        # brighrness
        row = 0
        label = ttk.Label(self._frame, text="Brightness")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        self.brightness_scale = ttk.Scale(self._frame, from_=self.brightness_min, to=self.brightness_max, orient="horizontal",
                                     length=350, command=self.on_brightness_scale_changed)
        self.brightness_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.brightness_label = ttk.Label(self._frame, text="0")
        self.brightness_label.grid(row=row, column=2, sticky="w", padx=10)

        # contrast
        row += 1
        label = ttk.Label(self._frame, text="Contrast")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        self.contrast_scale = ttk.Scale(self._frame, from_=self.contrast_min, to=self.contrast_max, orient="horizontal",
                                   length=350, command=self.on_contrast_scale_changed)
        self.contrast_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.contrast_label =  ttk.Label(self._frame, text="0")
        self.contrast_label.grid(row=row, column=2, sticky="w", padx=10)

        # saturation
        row += 1
        label = ttk.Label(self._frame, text="Saturation")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        self.saturation_scale = ttk.Scale(self._frame, from_=self.saturation_min, to=self.saturation_max, orient="horizontal",
                                   length=350, command=self.on_saturation_scale_changed)
        self.saturation_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.saturation_label =  ttk.Label(self._frame, text="0")
        self.saturation_label.grid(row=row, column=2, sticky="w", padx=10)
        
        # Backlight
        row += 1
        label = ttk.Label(self._frame, text="Backlight")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        self.backlight_scale = ttk.Scale(self._frame, from_=self.backlight_min, to=self.backlight_max, orient="horizontal",
                                   length=350, command=self.on_backlight_scale_changed)
        self.backlight_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.backlight_label =  ttk.Label(self._frame, text="0")
        self.backlight_label.grid(row=row, column=2, sticky="w", padx=10)

    def on_cell_count_scale_changed(self, value):
        option = ["Auto", "2S", "3S", "4S"]
        
        self.cell_count = int(float(value))
        self.cell_count_label.config(text=option[self.cell_count])
    
    def on_warning_cell_voltage_scale_changed(self, value):
        self.warning_cell_voltage = int(float(value))
        self.warning_cell_voltage_label.config(text=f"{self.warning_cell_voltage/10}")
        
    def init_power_setting(self):
        row = 4
        label = ttk.Label(self._frame, text="Cell Count")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        self.cell_count_scale = ttk.Scale(self._frame, from_=0, to=3, orient="horizontal",
                                   length=350, command=self.on_cell_count_scale_changed)
        self.cell_count_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.cell_count_label = ttk.Label(self._frame, text="Auto")
        self.cell_count_label.grid(row=row, column=2, sticky="w", padx=10)
        
        row += 1
        label = ttk.Label(self._frame, text="Warning Cell Voltage")
        label.grid(row=row, column=0, sticky="w", padx=20)
        
        self.warning_cell_voltage_scale = ttk.Scale(self._frame, from_=28, to=42, orient="horizontal",
                                   length=350, command=self.on_warning_cell_voltage_scale_changed)
        self.warning_cell_voltage_scale.grid(row=row, column=1, sticky="w", padx=20)
        
        self.warning_cell_voltage_label = ttk.Label(self._frame, text="2.8")
        self.warning_cell_voltage_label.grid(row=row, column=2, sticky="w", padx=10)

