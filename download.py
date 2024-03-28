import requests
import sys
import time
from global_var import *
import os


class download:
    def __init__(self):

        self.status = download_status.IDLE.value
        self.url = ""
        self.save_path = ""

    def download_file(self, url, save_path, clear):
        print(f"Downloading {url}")
        if clear:
            if os.path.exists(save_path):
                os.remove(save_path)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(response.content)
                if self.status == download_status.DOWNLOAD_EXIT.value:
                    sys.exit()
                return 1
            else:
                if self.status == download_status.DOWNLOAD_EXIT.value:
                    sys.exit()
                print("Failed to download file.")
                return 0
        except:
            return 0


my_download = download()


def download_thread_proc():
    ret0 = 0
    ret1 = 0
    ret2 = 0
    ret3 = 0
    ret0 = my_download.download_file(
        "https://api.github.com/repos/hd-zero/hdzero-vtx/releases", "resource/vtx_releases", 1)
    ret1 = my_download.download_file(
        "https://raw.githubusercontent.com/hd-zero/hdzero-vtx/main/src/common.h", "resource/vtx_common", 0)
    ret2 = my_download.download_file(
        "https://api.github.com/repos/ligenxxxx/event-vrx/releases", "resource/event_vrx_releases", 1)
    ret3 = my_download.download_file(
        "https://api.github.com/repos/ligenxxxx/hv/releases", "resource/hybrid_view_releases", 1)
    time.sleep(1)
    my_download.status = download_status.FILE_PARSE.value

    while True:
        if my_download.status == download_status.DOWNLOAD_VTX_FW.value:
            if my_download.download_file(my_download.url, my_download.save_path, 1):
                my_download.status = download_status.DOWNLOAD_VTX_FW_DONE.value
            else:
                my_download.status = download_status.DOWNLOAD_VTX_FW_FAILED.value

        elif my_download.status == download_status.DOWNLOAD_HYBRID_VIEW_FW.value:
            if my_download.download_file(my_download.url, my_download.save_path, 1):
                my_download.status = download_status.DOWNLOAD_HYBRID_VIEW_FW_DONE.value
            else:
                my_download.status = download_status.DOWNLOAD_HYBRID_VIEW_FW_FAILED.value

        elif my_download.status == download_status.DOWNLOAD_EVENT_VRX_FW.value:
            if my_download.download_file(my_download.url, my_download.save_path, 1):
                my_download.status = download_status.DOWNLOAD_EVENT_VRX_FW_DONE.value
            else:
                my_download.status = download_status.DOWNLOAD_EVENT_VRX_FW_FAILED.value

        elif my_download.status == download_status.DOWNLOAD_EXIT.value:
            sys.exit()

        time.sleep(0.01)
