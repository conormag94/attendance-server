import datetime
import threading
import time

import api
from scan import AttendanceTracker


this_room = "LB04"
scheduled_lectures = dict()


def start_attendance_tracker(lecture):
    print("Starting lecture {0} on thread {1}".format(lecture['subject'], threading.current_thread()))
    tracker = AttendanceTracker(lecture['subject'])
    tracker.record()

    del scheduled_lectures[lecture['id']]
    print("Finished lecture {0}".format(lecture['subject']))


def as_datetime(date_string):
    date_format = '%a, %d %b %Y %H:%M:%S'
    return datetime.datetime.strptime(date_string, date_format)


def schedule_lecture(lecture_dict):
    now = datetime.datetime.now()
    start_time = as_datetime(lecture_dict['start_time'])
    delay = (start_time - now).total_seconds()

    threading.Timer(delay, start_attendance_tracker, [lecture_dict]).start()
    scheduled_lectures[lecture_dict['id']] = lecture_dict
    print("Scheduled Lecture {0} [{1}, {2}] @ {3}".format(
        lecture_dict['id'], lecture_dict['subject'],
        lecture_dict['room'], lecture_dict['start_time']
    ))


def update_schedule():
    schedule = api.get_test_schedule()
    for lecture in schedule:
        if scheduled_lectures.get(lecture['id']) is None:
            schedule_lecture(lecture)
        else:
            print("Lecture {0} already scheduled".format(lecture))


def start():
    update_schedule()
    # now = datetime.datetime.now()
    # start_time = now + datetime.timedelta(seconds=4)
    # delay = (start_time - now).total_seconds()
    #
    # threading.Timer(delay, start_attendance_tracker, ["test1"]).start()
    # print("Scheduled lecture, sleeping.... Current thread {0}".format(threading.current_thread()))
    time.sleep(8)
    print("Main Thread Woken Up")


if __name__ == '__main__':
    start()
