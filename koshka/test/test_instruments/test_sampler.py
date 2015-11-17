#!/usr/bin/python

import unittest
from time import sleep
from dac import DAC
from instruments import SingleSoundSampler, Sampler

import os
SAMPLE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.wav")

BASE_FREQUENCY = 528
BUFFER_SIZE = 512
SAMPLE_RATE = 44100


class TestSampler(unittest.TestCase):
    def setUp(self):
        self.dac = DAC(BUFFER_SIZE, SAMPLE_RATE)
        self.dac.start()

    def tearDown(self):
        self.dac.stop()

    def test_instantiation(self):
        sample = SingleSoundSampler(SAMPLE_FILE)
        self.assertIsNotNone(sample)

    def test_polyphonic_play(self):
        sampler = Sampler()
        sampler.add_sample(0, SAMPLE_FILE)
        sampler.add_sample(1, SAMPLE_FILE)
        self.dac.connect(sampler.callback)
        sampler.on(0)
        sleep(.5)
        sampler.on(0)
        sleep(.5)
        sampler.on(1)
        sleep(2)
        sampler.off(0)
        sampler.off(1)


if __name__ == '__main__':
    unittest.main()
