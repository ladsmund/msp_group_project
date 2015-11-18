import unittest
from scales.even_tempered import EvenTempered


class TestEvenTemperedScale(unittest.TestCase):
    def setUp(self):
        self.base_frequency = 528
        self.scale = EvenTempered(self.base_frequency)

    def test_get_spacing(self):
        '''
        This harness test is testing features related to Homework 4
        '''
        for i in range(0, 100):
            self.assertAlmostEqual(self.scale.get_spacing(i, i + 1), pow(2, 1. / 12))

    def test_interval_frequecies(self):
        # base_frequency = 528;
        # scale = EvenTempered12ToneScale(base_frequency)
        interval_frequencies = [528, 559, 593, 628, 665, 705, 747, 791, 838, 888, 941, 997, 1056]
        i = 0
        for f in interval_frequencies:
            self.assertAlmostEqual(f, self.scale.get_frequency(i), 0)
            i += 1

        for i in range(-40,40):
            f = self.base_frequency * (2**(1./12)) ** i
            self.assertAlmostEqual(f, self.scale.get_frequency(i), 0)

    def test_interval_cents(self):
        # base_frequency = 528;
        # scale = EvenTempered12ToneScale(base_frequency)
        interval_cents = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

        i = 0
        for cents_goal in interval_cents:
            cents = self.scale.get_cents(i)
            self.assertAlmostEqual(cents_goal, cents, 0)
            i += 1


if __name__ == '__main__':
    unittest.main()
