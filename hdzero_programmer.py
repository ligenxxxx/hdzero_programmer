import threading
from main_window import ui_thread_proc


def main():
    ui_thread = threading.Thread(
        target=ui_thread_proc, name="ui")
    ui_thread.start()


if __name__ == '__main__':
    main()
