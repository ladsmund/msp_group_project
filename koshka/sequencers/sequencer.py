import sys

from mixer import Mixer
import time




def read_monophonic_score(score):
    for (tone, length) in score:
        yield (0, tone, 1, 0)
        yield (0, tone, 0, length)


class Sequencer(Mixer):
    DEFAULT_SPEED = 120

    def __init__(self,
                 buffer_size=512,
                 sample_rate=44100,
                 speed=DEFAULT_SPEED):
        Mixer.__init__(self)
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.start_time = 0
        self.speed = speed
        self.instruments = []

    def add_instrument(self, instrument):
        id = len(self.instruments)
        self.instruments.append(instrument)
        self.add_device(instrument)
        return id

    def set_speed(self, speed):
        self.speed = speed

    def play_monophonic(self, score=[]):
        self.play(self, read_monophonic_score(score))

    def play(self, score=[]):
        for (instrument_id, tone, on, wait_time) in score:
            print(instrument_id, tone, on, wait_time)
            if wait_time:
                time.sleep(60. / (self.speed * wait_time))
            if on:
                self.instruments[instrument_id].on(tone)
            else:
                self.instruments[instrument_id].off(tone)

    @staticmethod
    def parse_mono_score(score_string):
        for line in score_string.splitlines():
            if len(line) > 0:
                tone, length = line.split()
                yield (0, tone, 1, 0)
                yield (0, tone, 0, length)

    @staticmethod
    def parse_score(score_string):
        for line in score_string.splitlines():
            if len(line) > 0:
                return line.split()
