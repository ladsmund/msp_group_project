
import unittest
from src.dac import DAC
from src.scales.pythag_series import PythagSeriesSevenNoteScale
from src.instruments.scalesynth import ScaleSynth
from time import sleep

BASE_FREQUENCY = 528
BUFFER_SIZE = 512
SAMPLE_RATE = 44100

class TestInstrument(unittest.TestCase):
    def setUp(self):
        self.scale = PythagSeriesSevenNoteScale(BASE_FREQUENCY)


    def test_instantiation(self):
        instrument = ScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        self.assertIsNotNone(instrument)

    def test_play(self):
        dac = DAC(BUFFER_SIZE, SAMPLE_RATE)
        instrument = ScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        dac.connect(instrument.callback)

        dac.start()
        instrument.on(0)
        sleep(.5)
        instrument.off()
        sleep(.1)
        instrument.on(1)
        sleep(.5)


if __name__ == '__main__':
    unittest.main()