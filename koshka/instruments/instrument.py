from exceptions import NotImplementedError
import numpy as np
from mixer import Mixer


class InstrumentEvent:
    def __init__(self, instrument):
        self.instrument = instrument


class ToneEvent(InstrumentEvent):
    def __init__(self, instrument, tone):
        InstrumentEvent.__init__(self, instrument)
        self.tone = tone


class ToneOnEvent(ToneEvent):
    pass


class ToneOffEvent(ToneEvent):
    pass


class Instrument(object):
    name = "instrument"

    def __init__(self, id_variable=None):
        self.tone = None
        self.enabled = False
        self.id_variable = id_variable
        self.name_id = self.name
        self.update_time = 0
        self.update_tone = None
        self.update_enable = False

    def on(self, tone, time=0):
        self.update_time = time
        if time == 0:
            self.tone = tone
            self.enabled = True
        else:
            self.update_enable = True
            self.update_tone = tone

    def off(self, time=0):
        self.update_time = time
        if time == 0:
            self.enabled = False
        else:
            self.update_enable = False


    def _callback(self, in_data, frame_count, time_info, status):
        raise NotImplementedError()

    def callback(self, in_data, frame_count, time_info, status):
        offset = 0

        if self.update_time != 0:
            self.update_time -= frame_count
            if self.update_time < 0:
                self.enabled = self.update_enable
                self.tone = self.update_tone
                offset = -self.update_time
                self.update_time = 0

        if self.enabled:
            data = self._callback(in_data, frame_count - offset, time_info, status)
            return np.concatenate((np.zeros(offset), data), 0)
        else:
            return None

    def __str__(self):
        return self.name


class PolyphonicInstrument(Mixer):
    name = "poly instrument"

    def __init__(self, id_variable=None):
        Mixer.__init__(self)
        self.sub_instruments = {}
        self.observers = set()
        self.id_variable = id_variable
        self.name_id = self.name

    def add_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def remove_all_observers(self):
        self.observers = set()

    def notify_observers(self, event):
        for observer in self.observers:
            observer.notify(event)

    def on(self, tone, time=0):
        if tone in self.sub_instruments:
            self.sub_instruments[tone].on(tone, time)
        self.notify_observers(ToneOnEvent(self, tone))

    def off(self, tone=None, time=0):
        if tone is None:
            for s in self.sub_instruments.values():
                s.off(time)
                self.notify_observers(ToneOffEvent(self, s.tone))
        elif tone in self.sub_instruments:
            self.sub_instruments[tone].off(time)
            self.notify_observers(ToneOffEvent(self, tone))

    def __str__(self):
        return type(self).__name__
