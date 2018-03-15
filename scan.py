import datetime
import time

from binascii import unhexlify

from bluepy.btle import Scanner, DefaultDelegate, BTLEException, Peripheral, UUID


student_number_service = UUID("4CC28E11-4465-4136-B84C-AB34109B3D87")
student_number_characteristic = UUID("8FB63C83-2AAC-44DC-8FB6-6BE9257CBDD1")


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.connectable and dev.addrType == "random":
            print("We got a live one in here")
            # for adtype, desc, value in dev.getScanData():
            #     if adtype == 0x07:
            #         device = Peripheral(dev.addr, addrType="random")
            #         service = device.getServiceByUUID(student_number_service)
            #         chars = device.getCharacteristics(uuid=student_number_characteristic)
            #         print(service)
            #         print(chars[0].read())
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
            print(len(devices))
            for dev in devices:
                for adtype, desc, value in dev.getScanData():
                    if adtype == 0x07:
                        if dev.connectable and dev.addrType == "random":
                            student_number = self.read_student_number(dev.addr)
                            print("Student Num: {0}".format(student_number))
                            self.register_student(student_number)
                            students_scanned += 1
                        print("Connectable: {0}".format(dev.connectable))
        except BTLEException as e:
            print("No devices currently broadcasting")
            print(e)
        return students_scanned

    def read_student_number(self, mac_address):
        device = Peripheral(mac_address, addrType="random")
        service = device.getServiceByUUID(student_number_service)
        chars = device.getCharacteristics(uuid=student_number_characteristic)
        print(service)

        student_number = chars[0].read()
        return student_number

    def register_student(self, student_number):
        if self.data.get(student_number):
            self.data[student_number] += 1
        else:
            self.data[student_number] = 1

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
