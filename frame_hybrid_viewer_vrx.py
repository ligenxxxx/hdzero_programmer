import tkinter as tk
from frame_programmer import frame_programmer


class frame_hybrid_viewer_vrx:
    def __init__(self, parent, winWidth, winHeight):
        self._parent = parent
        self._frame = tk.Frame(parent, bg="green")
        parent.add(self._frame, text="Hybrid Viewer VRX")

    def frame(self):
        return self._frame

'''
    def create_setting(self):
        length = 160
        x1 = 2
        x2 = 100
        x3 = length + x2 + 10

        # Brightness
        brightness_y = 20
        # label 1
        self.brightness_label1 = ttk.Label(
            self._parent, text="Brightness", style="TLabel")
        self.brightness_label1.place(x=x1, y=brightness_y)
        # scale
        self.brightness_scale = ttk.Scale(
            self._parent, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale", length=length)
        self.brightness_scale.place(x=x2, y=brightness_y)
        # label 2
        self.brightness_label2 = ttk.Label(
            self._parent, text="% ")
        self.brightness_label2.place(x=x3, y=brightness_y)

        # Contrast
        contrast_y = 60
        # label1
        self.contrast_label1 = ttk.Label(
            self._parent, text="Contrast")
        self.contrast_label1.place(x=x1, y=contrast_y)
        # scale
        self.contrast_scale = ttk.Scale(
            self._parent, from_=0, to=255, orient=tk.HORIZONTAL, length=length)
        self.contrast_scale.place(x=x2, y=contrast_y)
        # label2
        self.contrast_label2 = ttk.Label(
            self._parent, text=" ")
        self.contrast_label2.place(x=x3, y=contrast_y)

        # Saturation
        saturation_y = 100
        # label1
        self.saturation_label1 = ttk.Label(
            self._parent, text="Saturation")
        self.saturation_label1.place(x=x1, y=saturation_y)
        # scale
        self.saturation_scale = ttk.Scale(
            self._parent, from_=0, to=100, orient=tk.HORIZONTAL, length=length)
        self.saturation_scale.place(x=x2, y=saturation_y)
        # label2
        self.saturation_label2 = ttk.Label(
            self._parent, text=" ")
        self.saturation_label2.place(x=x3, y=saturation_y)

        # Backlight
        backlight_y = 140
        # label1
        self.backlight_label1 = ttk.Label(
            self._parent, text="Backlight")
        self.backlight_label1.place(x=x1, y=backlight_y)
        # scale
        self.backlight_scale = ttk.Scale(
            self._parent, from_=0, to=100, orient=tk.HORIZONTAL, length=length)
        self.backlight_scale.place(x=x2, y=backlight_y)
        # label2
        self.backlight_label2 = ttk.Label(
            self._parent, text=" ")
        self.backlight_label2.place(x=x3, y=backlight_y)
'''