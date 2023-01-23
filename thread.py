import threading
import time


def doit():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print("working on")
        time.sleep(1)
    print("Stopping as you wish.")


def main():
    t = threading.Thread(target=doit)
    t.start()
    time.sleep(5)
    t.do_run = False


if __name__ == "__main__":
    main()