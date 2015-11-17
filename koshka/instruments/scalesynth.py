from oscilator import Oscilator
from instrument import Instrument, PolyphonicInstrument


class MonophonicScaleSynth(Instrument):
    def __init__(self, samplerate, buffer_size, scale):
        Instrument.__init__(self)
        self.scale = scale
        self.oscillator = Oscilator(samplerate, buffer_size)
        self.oscillator.start()

    def on(self, tone):
        frequency = self.scale.get_interval_frequency(tone)
        self.oscillator.setFreq(frequency)
        Instrument.on(self, tone)

    def _callback(self, in_data, frame_count, time_info, status):
        return self.oscillator.callback(in_data, frame_count, time_info, status)


class ScaleSynth(PolyphonicInstrument):
    def __init__(self, sample_rate, buffer_size, scale):
        PolyphonicInstrument.__init__(self)
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.scale = scale

    def _add_synth(self, tone):
        synth = MonophonicScaleSynth(self.sample_rate, self.buffer_size, self.scale)
        self.add_device(self, synth)
        self.sub_instruments[tone] = synth

    def on(self, tone):
        if tone not in self.sub_instruments:
            self._add_synth(tone)
        PolyphonicInstrument.on(self, tone)
