import unittest

from src.scales.pythag_series import PythagSeriesDodecaphpnic
from src.instruments.scalesynth import ScaleSynth
from src.sequencers.sequencer import Sequencer

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
        instrument = ScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        self.sequencer.add_device(instrument)

        # melody = [(0, t-64, on, time/1024.) for (i, t, on, time) in bach]
        #
        # print melody
        #
        # self.sequencer.play(melody)

        self.sequencer.play([(0,0,1,0),
                             # (0,4,1,1),
                             # (0,7,1,0),
                             # (0,4,0,1),
                             # (0,3,1,0),
                             (0,3,0,1)],
                            block=True)

        pass


if __name__ == '__main__':
    unittest.main()
