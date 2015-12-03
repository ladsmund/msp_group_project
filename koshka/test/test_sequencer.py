import unittest

# import sys
# print "sys.path"
# print(sys.path[0:3])
# print "--------"
# sys.stderr.write('\n')

from scales.pythag_series import PythagDodecaphonic
from instruments.scalesynth import ScaleSynth
from sequencers.sequencer import Sequencer

BASE_FREQUENCY = 528
BUFFER_SIZE = 512
SAMPLE_RATE = 44100


class TestInstrument(unittest.TestCase):
    def setUp(self):
        self.scale = PythagDodecaphonic(BASE_FREQUENCY)
        # self.scale = EvenTempered(BASE_FREQUENCY)
        self.sequencer = Sequencer(BUFFER_SIZE, SAMPLE_RATE)

    def test_instantiation(self):
        self.assertIsNotNone(self.sequencer)

    def test_play(self):
        instrument = ScaleSynth(SAMPLE_RATE, BUFFER_SIZE, self.scale)
        self.sequencer.add_device(instrument)

        self.sequencer.play([(0, 0, 1, 0),
                             # (0,4,1,1),
                             # (0,7,1,0),
                             # (0,4,0,1),
                             # (0,3,1,0),
                             (0, 3, 0, 1)],
                            block=True)


if __name__ == '__main__':
    unittest.main()
