from instrument import Instrument
from oscilator import Oscilator


class SineSynth(Instrument, Oscilator):
    name = "Sine Synth"

    def __init__(self, samplerate, bufferSize):
        Instrument.__init__(self)
        Oscilator.__init__(self, samplerate, bufferSize)
        Oscilator.start(self)

    def _callback(self, in_data, frame_count, time_info, status):
        output_buffer = Oscilator.callback(self, in_data, frame_count, time_info, status)
        if not self.enabled:
            output_buffer *= 0
        return output_buffer

    def on(self, frequency):
        self.setFreq(frequency)
        Instrument.on(self, 0)

    def __str__(self):
        string = "SineSynth\n  Frequency: %0.1f" % self.frequency
        return string

