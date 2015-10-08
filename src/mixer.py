class Mixer:
    def __init__(self):
        self.devices = []
        self.volume = 1
        pass

    def setVolume(self, volume):
        self.volume = volume

    def getVolume(self):
        return self.volume

    def callback(self, in_data, frame_count, time_info, status):
        output = None
        for d in self.devices:
            devOutput = d.callback(in_data, frame_count, time_info, status)
            if output is None:
                output = devOutput
            else:
                output += devOutput
        if output is None:
            print "output is None:"
            print len(self.devices)
        if self.volume is None:
            print "self.volume is None"
        return self.volume * output

    def addDevice(self, device):
        self.devices.append(device)
        pass
