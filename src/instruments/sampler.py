__author__ = 'mads'

import scipy.io.wavfile
import numpy
import time

_DEFAULT_AUDIO_GAIN = 0.00005


class Sampler():
    def __init__(self, filename):
        self.filename = None
        self.audio_data = None
        self.on = False
        self.audio_data_offset = 0
        self.length = 0
        self.trigger_start = 0

        self.load_file(filename)

    def load_file(self, filename):
        self.filename = filename
        self.on = False
        (rate, audio_data) = scipy.io.wavfile.read(filename)
        if len(audio_data.shape) > 1:
            self.audio_data = numpy.array(audio_data[:, 0], dtype=float)
        else:
            self.audio_data = numpy.array(audio_data, dtype=float)

        self.audio_data *= _DEFAULT_AUDIO_GAIN
        self.audio_data_offset = 0
        self.length = 0
        self.trigger_start = 0

    def trigger(self, tone=1, length=.4):
        self.audio_data_offset = 0
        self.on = True
        self.length = length
        self.trigger_start = time.time()

    def callback(self, in_data, frame_count, time_info, status):
        output_buffer = numpy.zeros(frame_count)

        if not self.on:
            return output_buffer

        if self.audio_data_offset >= len(self.audio_data):
            self.on = False
            return output_buffer

        audio_data_length = len(self.audio_data[self.audio_data_offset:])

        if frame_count > audio_data_length:
            output_buffer[:audio_data_length] = self.audio_data[self.audio_data_offset:]
            self.audio_data_offset += audio_data_length

        if audio_data_length >= frame_count:
            output_buffer = self.audio_data[self.audio_data_offset:(frame_count + self.audio_data_offset)]
            self.audio_data_offset += frame_count

        return output_buffer

    def __str__(self):
        string = "Sampler\n  filename: %s" % (self.filename)
        return string
