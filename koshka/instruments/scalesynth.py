from oscilator import Oscilator
from instrument import Instrument, PolyphonicInstrument, InstrumentEvent

class NewScaleEvent(InstrumentEvent):
    def __init__(self, instrument, new_scale, old_scale):
        InstrumentEvent.__init__(self, instrument)
        self.old_scale = old_scale
        self.new_scale = new_scale

class MonophonicScaleSynth(Instrument):

    def __init__(self, samplerate, buffer_size, scale):
        Instrument.__init__(self)
        self.scale = scale
        self.oscillator = Oscilator(samplerate, buffer_size)
        self.oscillator.start()
        self._callback = self.oscillator.callback

    def set_scale(self, scale):
        self.scale = scale

    def on(self, tone, time=0):
        frequency = self.scale.get_frequency(tone)
        self.oscillator.setFreq(frequency)
        Instrument.on(self, tone, time=time)

    def __str__(self):
        return "MonophonicScaleSynth %s" % str(self.scale)


class ScaleSynth(PolyphonicInstrument):

    name = "Scale Synth"

    def __init__(self, sample_rate, buffer_size, scale):
        PolyphonicInstrument.__init__(self)
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.scale = scale

    def set_scale(self, scale):
        self.notify_observers(NewScaleEvent(self, scale, self.scale))
        self.scale = scale
        for i in self.sub_instruments.values():
            i.set_scale(scale)

    def _add_synth(self, tone):
        synth = MonophonicScaleSynth(self.sample_rate, self.buffer_size, 
                                     self.scale)
        self.add_device(synth)
        self.sub_instruments[tone] = synth

    def on(self, tone, time=0):
        if tone not in self.sub_instruments:
            self._add_synth(tone)
        PolyphonicInstrument.on(self, tone, time=time)

    def __str__(self):
        return "ScaleSynth %s" % str(self.scale)
