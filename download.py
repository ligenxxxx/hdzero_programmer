import requests
import sys
import time

class download:
    def __init__(self):
        self.status = -1
        self.download_file("https://api.github.com/repos/hd-zero/hdzero-vtx/releases", "vtx_releases")
        self.download_file("https://raw.githubusercontent.com/hd-zero/hdzero-vtx/main/src/common.h", "vtx_common")
        self.status = 0
        
        self.url=""
        self.save_path=""
    
    def download_file(self, url, save_path):
        print(f"Downloading {url}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"File {save_path} downloaded successfully.")
            return 1
        else:
            print("Failed to download file.")
            return 0



def download_thread_proc():
    my_download = download()
    
    while True:
        if my_download.status == -1:
            if my_download.download_file(my_download.url, my_download.save_path):
                my_download.status = 0
        elif my_download.status == 255:
            sys.exit()
        
        time.sleep(0.01)
            
            