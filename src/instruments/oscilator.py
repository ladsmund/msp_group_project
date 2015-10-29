__author__ = 'mads'

import numpy as np

_DEFAULT_FREQ = 100
_DEFAULT_GAIN = .1


class Oscilator:
    def __init__(self, samplerate, bufferSize):
        self.samplerate = samplerate

        self.bufferSize = bufferSize
        self.phase = 0.0
        self.setFreq(_DEFAULT_FREQ)
        self.running = False

    def setFreq(self, frequency, gain=None):
        self.sample_phase = 0
        self.phases = 0
        self.gain = _DEFAULT_GAIN

        self.sample_phase = 2 * np.pi * frequency / self.samplerate
        self.phases = 0
        if gain is not None:
            self.gain = gain

    def set_gain(self, gain):
        self.gain = gain

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def callback(self, in_data, frame_count, time_info, status):
        if self.running:
            out_array = None

            if out_array is None:
                out_array = self.gain * np.sin(self.phases + self.sample_phase * np.arange(0, frame_count))
            else:
                out_array += self.gain * np.sin(self.phases + self.sample_phase * np.arange(0, frame_count))

            self.phases += self.sample_phase * frame_count

            return out_array
        else:
            return np.zeros(frame_count)
