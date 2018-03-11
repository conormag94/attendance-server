import datetime
import time

from binascii import unhexlify

from bluepy.btle import Scanner, DefaultDelegate, BTLEException


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass
        #if isNewDev:
        #    print("Discovered device", dev.addr)
        #if isNewData:
        #    print("Received new data from", dev.addr)


class AttendanceTracker(object):
    def __init__(self, lecture):
        self.lecture = lecture
        self.data = dict()
        self.scanner = Scanner().withDelegate(ScanDelegate())

    def start_scanning(self, duration):
        students_scanned = 0
        try:
            devices = self.scanner.scan(duration)
            for dev in devices:
                for adtype, desc, value in dev.getScanData():
                    if adtype == 0x16 and value.startswith('192f'):
                        student_number = unhexlify(value).decode()
                        if self.data.get(student_number):
                            self.data[student_number] += 1
                        else:
                            self.data[student_number] = 1
                        students_scanned += 1
        except BTLEException as e:
            print("No devices currently broadcasting")
            print(e)
        return students_scanned

    def print_data(self):
        print(self.data)

    def record(self):
        print("Recording attendance for: {0}".format(self.lecture))

        print("Scanning attendance for 1st time...(1/2)")
        scans = self.start_scanning(duration=15.0)
        print("{0} student numbers scanned during first scan".format(scans))

        print("Sleeping")
        time.sleep(3)

        print("Scanning attendance for 2nd time...(2/2)")
        scans = self.start_scanning(duration=15.0)
        print("{0} student numbers scanned during first scan".format(scans))

        self.print_data()

tracker = AttendanceTracker(lecture="Security & Privacy")
tracker.record()
