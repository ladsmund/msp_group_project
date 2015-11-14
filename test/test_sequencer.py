
import unittest
from src.scales.pythag_series import PythagSeriesDodecaphpnic
from src.scales.even_tempered import EvenTempered
from src.instruments.scalesynth import ScaleSynth, PolyphonicScaleSynth
from src.sequencer import Sequencer

BASE_FREQUENCY = 528
BUFFER_SIZE = 512
SAMPLE_RATE = 44100

class TestInstrument(unittest.TestCase):
    def setUp(self):
        self.scale = PythagSeriesDodecaphpnic(BASE_FREQUENCY)
        # self.scale = EvenTempered(BASE_FREQUENCY)
        self.sequencer = Sequencer(BUFFER_SIZE, SAMPLE_RATE)

    def test_instantiation(self):
        self.assertIsNotNone(self.sequencer)

    def test_play(self):
        instrument = PolyphonicScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        self.sequencer.add_device(instrument)
        self.sequencer.play([(0,0,1,1),
                             (0,4,1,0),
                             (0,7,1,1),
                             (0,4,0,0),
                             (0,3,1,1)])
        pass


if __name__ == '__main__':
    unittest.main()
