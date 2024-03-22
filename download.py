import requests
import sys
import time
from global_var import *


class download:
    def __init__(self):

        self.status = download_status.IDLE.value
        self.url = ""
        self.save_path = ""

    def download_file(self, url, save_path):
        print(f"Downloading {url}")
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


my_download = download()


def download_thread_proc():
    my_download.download_file(
        "https://api.github.com/repos/hd-zero/hdzero-vtx/releases", "vtx_releases")
    my_download.download_file(
        "https://raw.githubusercontent.com/hd-zero/hdzero-vtx/main/src/common.h", "vtx_common")
    my_download.download_file(
        "https://api.github.com/repos/ligenxxxx/event-vrx/releases", "event_vrx_releases")
    my_download.download_file(
        "https://api.github.com/repos/ligenxxxx/hv/releases", "hybrid_view_releases")
    my_download.status = download_status.FILE_PARSE.value

    while True:
        if my_download.status == download_status.DOWNLOAD_VTX_FW.value:
            if my_download.download_file(my_download.url, my_download.save_path):
                my_download.status = download_status.DOWNLOAD_VTX_FW_DONE.value

        elif my_download.status == download_status.DOWNLOAD_HYBRID_VIEW_FW.value:
            if my_download.download_file(my_download.url, my_download.save_path):
                my_download.status = download_status.DOWNLOAD_HYBRID_VIEW_FW_DONE.value

        elif my_download.status == download_status.DOWNLOAD_EVENT_VRX_FW.value:
            if my_download.download_file(my_download.url, my_download.save_path):
                my_download.status = download_status.DOWNLOAD_EVENT_VRX_FW_DONE.value

        elif my_download.status == download_status.DOWNLOAD_EXIT.value:
            sys.exit()

        time.sleep(0.01)
