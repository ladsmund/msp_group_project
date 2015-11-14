from exceptions import NotImplementedError


class Instrument():
    def __init__(self):
        self.tone = None
        self.enabled = False

    def on(self, tone):
        self.tone = tone
        self.enabled = True

    def off(self):
        self.enabled = False

    def _callback(self, in_data, frame_count, time_info, status):
        raise NotImplementedError()

    def callback(self, in_data, frame_count, time_info, status):
        if self.enabled:
            return self._callback(in_data, frame_count, time_info, status)
        else:
            return None

#class PolyphonicInstrument(Mixer):
#    def __init__(self):
#        Mixer.__init__(self)
#        self.sub_instruments = []
#        self.active_instruments = []
#
#    def on(self, ):
#        self.sub_instruments[0].on(tone)

