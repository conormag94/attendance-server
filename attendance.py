import datetime
import threading
import time

from scan import AttendanceTracker


def task(lecture):
    print("Starting lecture {0} on thread {1}".format(lecture, threading.current_thread()))
    tracker = AttendanceTracker(lecture)
    tracker.record()
    print("Finished lecture {0}".format(lecture))


def start():
    now = datetime.datetime.now()
    start_time = now + datetime.timedelta(seconds=4)
    delay = (start_time - now).total_seconds()

    threading.Timer(delay, task, ["test1"]).start()
    print("Scheduled lecture, sleeping.... Current thread {0}".format(threading.current_thread()))
    time.sleep(8)
    print("WOKE FAM")


if __name__ == '__main__':
    start()
