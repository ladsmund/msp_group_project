__author__ = 'mads'

import scipy.io.wavfile
import numpy
import time


class Sampler():
    def __init__(self, filename):
        (rate, audio_data) = scipy.io.wavfile.read(filename)
        self.audio_data = 0.001 * audio_data[:, 0]


        self.audio_data_offset = 0

        self.on = False
        self.length = 0
        self.trigger_start = 0

    def trigger(self, length=.1):
        self.audio_data_offset = 0
        self.on = True
        self.length = length
        self.trigger_start = time.time()

    def callback(self, in_data, frame_count, time_info, status):
        output_buffer = numpy.zeros(frame_count)

        if self.on and self.audio_data_offset >= len(self.audio_data):
            self.on = False
            return output_buffer

        audio_data_length = len(self.audio_data[self.audio_data_offset:])

        if frame_count > audio_data_length:
            # print len(output_buffer)
            # print audio_data_length
            # print len(self.audio_data)
            # print len(self.audio_data_offset)
            output_buffer[:audio_data_length] = self.audio_data[self.audio_data_offset:]
            self.audio_data_offset += audio_data_length

        if audio_data_length >= frame_count:
            output_buffer = self.audio_data[self.audio_data_offset:(frame_count + self.audio_data_offset)]
            self.audio_data_offset += frame_count

        return output_buffer
