import threading
from main_window import ui_thread_proc
from download import download_thread_proc


def main():

    download_thread = threading.Thread(
        target=download_thread_proc, name="download")
    download_thread.start()

    ui_thread = threading.Thread(
        target=ui_thread_proc, name="ui")
    ui_thread.start()


if __name__ == '__main__':
    main()
