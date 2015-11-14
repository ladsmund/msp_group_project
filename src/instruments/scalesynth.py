import time

from oscilator import Oscilator
from instrument import Instrument


class ScaleSynth(Instrument):
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

    def __str__(self):
        string = "SineSynth\n  Frequency: %0.1f" % self.frequency
        return string

class PolyphonicScaleSynth(Mixer):

    def __init__(self, sample_rate, buffer_size, scale):
        Mixer.__init__(self)
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.scale = scale
        self.sub_synths = {}
        
    def _add_synth(self, tone):
        synth = ScaleSynth(self.sample_rate, self.buffer_size, self.scale)
        Mixer.add_device(self, synth)
        self.sub_synths[tone] = synth

    def on(self, tone):
        if tone not in self.sub_synths:
            self._add_synth(tone)
        self.sub_synths[tone].on(tone)

    def off(self, tone):
        if tone in self.sub_synths:
            self.sub_synths[tone].off()
