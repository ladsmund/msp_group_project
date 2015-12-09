from exceptions import NotImplementedError
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

    def __init__(self, id_variable = None):
        self.tone = None
        self.enabled = False
        self.id_variable = id_variable
        self.name_id = self.name

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

    def __str__(self):
        return self.name


class PolyphonicInstrument(Mixer):
    name = "poly instrument"

    def __init__(self, id_variable = None):
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

    def on(self, tone):
        if tone in self.sub_instruments:
            self.sub_instruments[tone].on(tone)
        self.notify_observers(ToneOnEvent(self, tone))

    def off(self, tone=None):
        if tone is None:
            for s in self.sub_instruments.values():
                s.off()
                self.notify_observers(ToneOffEvent(self, s.tone))
        elif tone in self.sub_instruments:
            self.sub_instruments[tone].off()
            self.notify_observers(ToneOffEvent(self, tone))

    def __str__(self):
        return type(self).__name__
