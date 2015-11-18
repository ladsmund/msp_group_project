import unittest
from time import sleep

from dac import DAC
from scales import PythagSeries
from instruments.scalesynth import MonophonicScaleSynth, ScaleSynth

BASE_FREQUENCY = 528
BUFFER_SIZE = 512
SAMPLE_RATE = 44100


class TestInstrument(unittest.TestCase):
    def setUp(self):
        self.scale = PythagSeries(BASE_FREQUENCY)
        self.dac = DAC(BUFFER_SIZE, SAMPLE_RATE)
        self.dac.start()

    def tearDown(self):
        self.dac.stop()

    def test_instantiation(self):
        instrument = MonophonicScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        self.assertIsNotNone(instrument)

    def test_play(self):
        instrument = ScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        # instrument = ScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)

        self.dac.connect(instrument.callback)

        instrument.on(0)
        sleep(.5)
        instrument.off(0)
        sleep(.1)
        instrument.on(1)
        instrument.on(4)
        sleep(.5)
        instrument.off(1)
        sleep(.5)



if __name__ == '__main__':
    unittest.main()
