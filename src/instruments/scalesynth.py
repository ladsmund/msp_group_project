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
