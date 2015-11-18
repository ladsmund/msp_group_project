from exceptions import NotImplementedError
from mixer import Mixer


class Instrument:
    name = "instrument"

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


class PolyphonicInstrument(Mixer):
    name = "poly instrument"

    def __init__(self):
        Mixer.__init__(self)
        self.sub_instruments = {}

    def on(self, tone):
        if tone in self.sub_instruments:
            self.sub_instruments[tone].on(tone)

    def off(self, tone=None):
        if tone is None:
            [s.off() for s in self.sub_instruments.values()]
        elif tone in self.sub_instruments:
            self.sub_instruments[tone].off()
