import scipy.io.wavfile

from instrument import Instrument, PolyphonicInstrument
import numpy

_DEFAULT_AUDIO_GAIN = 0.00005


class SingleSoundSampler(Instrument):
    name = "Single Sound Sampler"

    def __init__(self, filename):
        Instrument.__init__(self)
        self.filename = None
        self.audio_data = None
        self.enabled = False
        self.offset = 0
        self.trigger_start = 0

        self.load_file(filename)

    def load_file(self, filename):
        self.filename = filename
        (rate, audio_data) = scipy.io.wavfile.read(filename)
        if len(audio_data.shape) > 1:
            self.audio_data = numpy.array(audio_data[:, 0], dtype=float)
        else:
            self.audio_data = numpy.array(audio_data, dtype=float)

        self.audio_data *= _DEFAULT_AUDIO_GAIN
        self.offset = 0
        self.trigger_start = 0

    def on(self, tone, time=0):
        self.offset = 0
        Instrument.on(self, tone, time=0)

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


class Sampler(PolyphonicInstrument):
    name = "Sampler"

    def __init__(self, file_list=[]):
        PolyphonicInstrument.__init__(self)
        for sample_id, filename in enumerate(file_list):
            self.add_sample(sample_id, filename)

    def add_sample(self, sample_id, filename):
        sample = SingleSoundSampler(filename)
        self.add_device(sample)
        self.sub_instruments[sample_id] = sample
