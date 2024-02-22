import ctypes
import time
import sys
import os
from ctypes import create_string_buffer


class ch341_class(object):

    def __init__(self):
        self.dll = None
        self.target = -1
        self.status = 0 # idle
        self.dll_name = "CH341DLL.DLL"

        self.target_id = 0
        self.fw_path = ""

        self.iolength = 6
        self.iobuffer = create_string_buffer(65544)
        self.write_crc = 0

        try:
            self.dll = ctypes.WinDLL(self.dll_name)
        except:
            print("please install driver")

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
        return (int.from_bytes(self.iobuffer[1], byteorder='big') & 1)

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

            self.write_crc += int.from_bytes(
                self.iobuffer[4 + i], byteorder='big')
            self.write_crc &= 0xffff

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

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

my_ch341 = ch341_class()


def ch341_thread_proc():

    while True:
        if my_ch341.status == 255:
            sys.exit()
        if my_ch341.status == 1: # connect vtx
            while True:
                if my_ch341.connect_vtx() == 1:
                    my_ch341.status = 2
                    break
                else:
                    time.sleep(0.1)
        elif my_ch341.status == 3: # update vtx
            my_ch341.flash_erase_vtx()
            my_ch341.flash_write_target_id()
            my_ch341.flash_write_fw()
            my_ch341.status = 4
        time.sleep(0.01)
