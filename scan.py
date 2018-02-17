from binascii import unhexlify

from bluepy.btle import Scanner, DefaultDelegate, BTLEException


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        if isNewData:
            print("Received new data from", dev.addr)


class AttendanceTracker(object):
    def __init__(self):
        self.data = dict()
        self.devices = []
        self.scanner = Scanner().withDelegate(ScanDelegate())

    def start_scanning(self):
        try:
            devices = self.scanner.scan(15.0)
            for dev in devices:
                for adtype, desc, value in dev.getScanData():
                    if adtype == 0x16 and value.startswith('192f'):
                        decoded_data = unhexlify(value).decode()
                        if self.data.get(decoded_data):
                            self.data[decoded_data] += 1
                        else:
                            self.data[decoded_data] = 1
        except BTLEException as e:
            print("No devices currently broadcasting")
            print(e)

    def print_data(self):
        print(self.data)


tracker = AttendanceTracker()
tracker.start_scanning()
tracker.print_data()
