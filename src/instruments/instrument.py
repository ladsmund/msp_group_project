from mixer import Mixer
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



class PolyPhonicScaleSynth(Instrument):
    def __init__(self):
        Instrument.__init__(self)
        self.active_notes = []
        self.sub_instruments = []
