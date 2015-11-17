#!/usr/bin/python

import unittest

from instruments import SingleSoundSampler

BASE_FREQUENCY = 528
BUFFER_SIZE = 512
SAMPLE_RATE = 44100

class TestSampler(unittest.TestCase):

    def test_instantiation(self):
        sample = SingleSoundSampler("./samples/anxious_16.wav")
        self.assertIsNotNone(sample)

#    def test_polyphonic_play(self):
#        dac = DAC(BUFFER_SIZE, SAMPLE_RATE)
#        sampler = PolyphonicSampler()
#        sampler.add_sample(0, "./samples/anxious_16.wav")
#        sampler.add_sample(1, "./samples/guitar_5th_c_16.wav")
#        dac.connect(sampler.callback)
#        dac.start()
#
#        sampler.on(0)
#        sleep(1)
#        sampler.off(1)
#        sleep(2)
#        sampler.off(0)
#        dac.stop()

if __name__ == '__main__':
    unittest.main()
