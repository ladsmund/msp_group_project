
import scipy.io.wavfile
import time

from src.mixer import Mixer
from instrument import Instrument
import numpy

_DEFAULT_AUDIO_GAIN = 0.00005


class Sampler(Instrument):
    def __init__(self, filename):
        Instrument.__init__(self)
        self.filename = None
        self.audio_data = None
        self.enabled = True
        self.offset = 0
        self.trigger_start = 0

        self.load_file(filename)

    def load_file(self, filename):
        self.filename = filename
        self.enabled = True
        (rate, audio_data) = scipy.io.wavfile.read(filename)
        if len(audio_data.shape) > 1:
            self.audio_data = numpy.array(audio_data[:, 0], dtype=float)
        else:
            self.audio_data = numpy.array(audio_data, dtype=float)

        self.audio_data *= _DEFAULT_AUDIO_GAIN
        self.offset = 0
        self.trigger_start = 0

    def on(self, tone):
        self.offset = 0
        Instrument.on(self, tone)

    def _callback(self, in_data, frame_count, time_info, status):
        output_buffer = numpy.zeros(frame_count)

        if not self.enabled:
            return None

        if self.offset >= len(self.audio_data):
            self.off()
            return output_buffer

        audio_data_length = len(self.audio_data[self.offset:])

        if frame_count > audio_data_length:
            output_buffer[:audio_data_length] = \
                self.audio_data[self.offset:]
            self.offset += audio_data_length

        if audio_data_length >= frame_count:
            output_buffer = self.audio_data[
                                self.offset:(frame_count + self.offset)]
            self.offset += frame_count

        return output_buffer

    def __str__(self):
        string = "Sampler\n  filename: %s" % (self.filename)
        return string

class PolyphonicSampler(Mixer):
    
    def __init__(self):
        Mixer.__init__(self)
        self.sub_samples = {}

    def add_sample(self, sample_id, filename):
        sample = Sampler(filename)
        Mixer.add_device(self, sample)
        self.sub_samples[sample_id] = sample

    def on(self, sample_id):
        if sample_id in self.sub_samples:
            self.sub_samples[sample_id].on(0)

    def off(self, sample_id):
        if sample_id in self.sub_samples:
            self.sub_samples[sample_id].off()

#if __name__ == '__main__':
#    from src.dac import DAC
#    from src.instruments.sampler import Sampler, PolyphonicSampler
#    from time import sleep
#
#    BASE_FREQUENCY = 528
#    BUFFER_SIZE = 512
#    SAMPLE_RATE = 44100
#
#    dac = DAC(BUFFER_SIZE, SAMPLE_RATE)
#
#    s = Sampler("./samples/anxious.wav")
#    dac.connect(s.callback)
#    dac.start()
#    
#    s.on()
