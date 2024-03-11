import ctypes
import time
import sys
import os
from ctypes import create_string_buffer
from frame_hybrid_view import frame_hybrid_viewer
import tkinter as tk
from tkinter import ttk
from global_var import *
from ctypes import *
import global_var

class ch341_class(object):

    def __init__(self):
        FW_5680SIZE = 65536
        FW_FPGASIZE = 2*1024*1024
        FW_8339SIZE = 10*1024*1024
        self.fw_5680_size = 0
        self.fw_5680_buf = create_string_buffer(FW_5680SIZE)
        self.fw_fpga_size = 0
        self.fw_fpga_buf = create_string_buffer(FW_FPGASIZE)
        self.fw_8339_size = 0
        self.fw_8339_buf = create_string_buffer(FW_8339SIZE)
        
        self.dll = None
        self.target = -1
        self.status = ch341_status.IDLE.value        # idle
        self.read_setting_flag = 1
        self.dll_name = "CH341DLL.DLL"

        self.addr_brightness = 0x22
        self.addr_contrast = 0x23
        self.addr_saturation = 0x24
        self.addr_backlight = 0x25
        self.addr_cell_count = 0x26
        self.addr_warning_cell_voltage = 0x27
        self.addr_fpga_device = 0x65  # 7bit address

        self.target_id = 0
        self.fw_path = ""
        
        self.written_len = 0
        self.to_write_len = 100
        
        self.connected = 0
        self.iolength = 6
        self.iobuffer = create_string_buffer(65544)
        self.rdbuffer = [0] * 256
        self.write_crc = 0
        self.read_crc = 0
        
        try:
            self.dll = ctypes.WinDLL(self.dll_name)
        except:
            print("please install driver")
            
    def parse_hybridview_fw(self, fw_path):
        with open(fw_path, "rb") as file:
            file.seek(2)
            self.fw_5680_size = int.from_bytes(file.read(4), byteorder='little')
            self.fw_fpga_size = int.from_bytes(file.read(4), byteorder='little')
            self.fw_8339_size = int.from_bytes(file.read(4), byteorder='little')
            self.fw_5680_buf = file.read(self.fw_5680_size)
            self.fw_fpga_buf = file.read(self.fw_fpga_size)
            self.fw_8339_buf = file.read(self.fw_8339_size)
            
    def ch341read_i2c(self, addr):
        self.dll.CH341ReadI2C(0, self.addr_fpga_device, addr, self.iobuffer)
        return int.from_bytes(self.iobuffer[0], byteorder='big')
        
    def read_setting(self):
        global_var.brightness = self.ch341read_i2c(self.addr_brightness)
        global_var.contrast = self.ch341read_i2c(self.addr_contrast)
        global_var.saturation = self.ch341read_i2c(self.addr_saturation)
        global_var.backlight = self.ch341read_i2c(self.addr_backlight)
        global_var.cell_count = self.ch341read_i2c(self.addr_cell_count)
        global_var.warning_cell_voltage = self.ch341read_i2c(self.addr_warning_cell_voltage)
        fpga_version = self.ch341read_i2c(0xff)
        #print(f"bri:{global_var.brightness:d} con:{global_var.contrast:d}\
        #    sat:{global_var.saturation:d} bac:{global_var.backlight:d}\
        #    cell:{global_var.cell_count:d} warning_cell:{global_var.warning_cell_voltage:d} fpga_version:{fpga_version:x}")

    def set_stream(self, cs):
        if cs == True:
            self.dll.CH341SetStream(0, 0x80)
        else:
            self.dll.CH341SetStream(0, 0x81)

    def stream_spi4(self):
        self.dll.CH341StreamSPI4(0, 0x80, self.ilength, self.iobuffer)

    def flash_switch0(self):
        self.dll.CH341SetOutput(0, 0x03, 0x0000FF00, 0x4300)

    def flash_switch1(self):
        self.dll.CH341SetOutput(0, 0x03, 0x0000FF00, 0x8300)

    def flash_switch2(self):
        self.dll.CH341SetOutput(0, 0x03, 0x0000FF00, 0xc800)

    def flash_release(self):
        self.dll.CH341SetOutput(0, 0x03, 0x0000FF00, 0xc200)

    def flash_read_id(self):
        self.iobuffer[0] = 0x9f
        self.iobuffer[1] = 0x9f
        self.iobuffer[2] = 0x9f
        self.iobuffer[3] = 0x9f
        self.iobuffer[4] = 0x9f
        self.iobuffer[5] = 0x9f
        self.ilength = 6

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

        return int.from_bytes(self.iobuffer[1], byteorder='big') * 256 * 256 \
            + int.from_bytes(self.iobuffer[2], byteorder='big') * 256 \
            + int.from_bytes(self.iobuffer[3], byteorder='big')

    def flash_write_enable(self):
        self.iobuffer[0] = 0x06
        self.ilength = 1

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_erase_block64(self):
        self.iobuffer[0] = 0xd8
        self.iobuffer[1] = 0
        self.iobuffer[2] = 0
        self.iobuffer[3] = 0
        self.ilength = 4

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)
        
    def flash_erase_block64_m(self, addr):
        self.iobuffer[0] = 0xd8
        self.iobuffer[1] = (addr >> 16) & 0xff
        self.iobuffer[2] = (addr >> 8) & 0xff
        self.iobuffer[3] = (addr >> 0) & 0xff
        self.ilength = 4

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)
        
    def flash_erase_section(self, addr):
        self.iobuffer[0] = 0x20
        self.iobuffer[1] = (addr >> 16) & 0x1f
        self.iobuffer[2] = (addr >> 8) & 0x1f
        self.iobuffer[3] = (addr >> 0) & 0x1f
        self.ilength = 4

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_write_disable(self):
        self.iobuffer[0] = 0x04
        self.ilength = 1

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_is_busy(self):
        self.iobuffer[0] = 0x05
        self.iobuffer[1] = 0x00
        self.ilength = 2

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)
        
        return (int.from_bytes(self.iobuffer[1], byteorder='little') & 1)
    
    def flash_erase_flash(self, block):
        self.flash_write_enable()
        self.flash_erase_block64_m(block)
        self.flash_wait_busy()
        self.flash_write_disable()

    def flash_wait_busy(self):
        while True:
            if self.flash_is_busy() == 0:
                return

    def flash_erase_vtx(self):
        self.flash_write_enable()
        self.flash_erase_block64()
        self.flash_wait_busy()
        self.flash_write_disable()

        self.flash_write_enable()
        self.flash_erase_section(65536)
        self.flash_wait_busy()
        self.flash_write_disable()

    def flash_write_page(self, base_address, length, fw):
        self.iobuffer[0] = 0x02
        self.iobuffer[1] = (base_address >> 16) & 0xff
        self.iobuffer[2] = (base_address >> 8) & 0xff
        self.iobuffer[3] = (base_address >> 0) & 0xff
        self.ilength = 4 + length

        for i in range(length):
            try:
                self.iobuffer[4+i] = fw[i]
            except:
                self.iobuffer[4+i] = 0xff
                
            #self.write_crc += int.from_bytes(self.iobuffer[4 + i], byteorder='little')
        
        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)  
                    
    def flash_read_page(self, base_address, length):
        self.iobuffer[0] = 0x03
        self.iobuffer[1] = (base_address >> 16) & 0xff
        self.iobuffer[2] = (base_address >> 8) & 0xff
        self.iobuffer[3] = (base_address >> 0) & 0xff
        self.ilength = 4 + length

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

        for i in range(256):
            self.rdbuffer[i] = self.iobuffer[i+4]

    def connect_vtx(self):
        if self.dll.CH341OpenDevice(0) < 0:
            return 0
        else:
            self.flash_switch0()
            flash_id_0 = self.flash_read_id()
            self.flash_switch1()
            flash_id_1 = self.flash_read_id()
            self.flash_switch2()
            flash_id_2 = self.flash_read_id()
            if flash_id_0 == flash_id_1 and flash_id_1 == flash_id_2:
                if flash_id_0 == 0xEF4014 or flash_id_0 == 0x5E6014:
                    return 1

            return 0

    def flash_write_target_id(self):
        self.flash_write_enable()
        self.flash_write_page(65536, 1, [self.target_id])
        self.flash_write_disable()
        self.flash_wait_busy()

    def flash_write_fw(self):
        size = os.path.getsize(self.fw_path)
        file = open(self.fw_path, "rb")
        fw = file.read()
        page_number = (size + (1 << 8) - 1) >> 8

        for page in range(page_number):
            base_address = page << 8
            self.flash_write_enable()
            self.flash_write_page(base_address, 256, fw[base_address:])
            self.flash_write_disable()
            self.flash_wait_busy()
            
            my_ch341.written_len += 256
            
    def connect_hybridview(self, sleep_sec):
        if self.dll.CH341OpenDevice(0) < 0:
            return 0
        else:
            #self.dll.CH341SetStream(0, 0x82)
            time.sleep(sleep_sec)
            self.flash_switch1()
            flash_id_2 = self.flash_read_id()
            if flash_id_2 == 0xEF4018:
                return 1
            else:
                return 0
            
    def fw_write_to_flash(self, fw_buf, fw_size):
        page_number = (fw_size + (1 << 8) - 1) >> 8
        for page in range(page_number):
            block = page << 8
            if (block & 0xffff) == 0:
                self.flash_erase_flash(block)
    
            base_address = page << 8
            self.flash_write_enable()
            self.flash_write_page(base_address, 256, fw_buf[base_address:])
            self.flash_write_disable()
            self.flash_wait_busy()        
            my_ch341.written_len += 256
"""
        for page in range(page_number):
            base_address = page << 8
            self.flash_read_page(base_address, 256)
            
            for i in range(256):
                self.read_crc += int.from_bytes(self.rdbuffer[i], byteorder='little')
"""

my_ch341 = ch341_class()

def ch341_thread_proc():
    while True:
        if my_ch341.status == ch341_status.STATUS_EXIT.value:
            sys.exit()
            
        if my_ch341.status == ch341_status.VTX_NOTCONNECTED.value:  # connect vtx
            if my_ch341.connect_vtx() == 1:
                my_ch341.status = ch341_status.VTX_CONNECTED.value

        elif my_ch341.status == ch341_status.VTX_UPDATE.value:  # update vtx
            my_ch341.written_len = 0
            my_ch341.to_write_len = os.path.getsize(my_ch341.fw_path)
            my_ch341.flash_erase_vtx()
            my_ch341.flash_write_target_id()
            my_ch341.flash_write_fw()
            my_ch341.status = ch341_status.VTX_UPDATEDONE.value
            
        #-------- HybridView ----------------- 
        elif  my_ch341.status == ch341_status.HYBRIDVIEW_NOTCONNECTED.value:     #connect HybridView
            if my_ch341.connect_hybridview(2) == 1:
                my_ch341.status = ch341_status.HYBRIDVIEW_CONNECTED.value
                my_ch341.connected = 1
                my_ch341.read_setting_flag = 1    

        elif my_ch341.status == ch341_status.HYBRIDVIEW_GET_FW.value:  # get HybridView firmware
            my_ch341.written_len = 0
            my_ch341.to_write_len = os.path.getsize(my_ch341.fw_path)
            my_ch341.parse_hybridview_fw(my_ch341.fw_path)
            
        elif my_ch341.status == ch341_status.HYBRIDVIEW_UPDATE.value: # update HybridView
            my_ch341.flash_switch0()
            my_ch341.fw_write_to_flash(my_ch341.fw_5680_buf, my_ch341.fw_5680_size)
            #my_ch341.flash_switch1()            
            #my_ch341.fw_write_to_flash(my_ch341.fw_fpga_buf, my_ch341.fw_fpga_size)
            #my_ch341.flash_switch2()
            #my_ch341.fw_write_to_flash(my_ch341.fw_8339_buf, my_ch341.fw_8339_size)
            my_ch341.dll.CH341CloseDevice(0)
            my_ch341.flash_release()
            my_ch341.status = ch341_status.HYBRIDVIEW_UPDATEDONE.value
        else:
            time.sleep(0.1)    
        
            
