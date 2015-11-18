import unittest
from scales.even_tempered import EvenTemperedScale, frequency_to_cents


class TestEvenTemperedScale(unittest.TestCase):
    def setUp(self):
        self.base_frequency = 528
        self.scale = EvenTemperedScale(self.base_frequency)

    def test_get_spacing(self):
        '''
        This harness test is testing features related to Homework 4
        '''
        # scale = EvenTempered12ToneScale()
        for i in range(0, 12):
            self.assertAlmostEqual(self.scale.get_spacing(i, i + 1), pow(2, 1. / 12))

    def test_interval_frequecies(self):
        # base_frequency = 528;
        # scale = EvenTempered12ToneScale(base_frequency)
        interval_frequencies = [528, 559, 593, 628, 665, 705, 747, 791, 838, 888, 941, 997, 1056]

        i = 0
        for f in interval_frequencies:
            self.assertAlmostEqual(f, self.scale.get_interval_frequency(i), 0)
            i += 1

    def test_interval_cents(self):
        # base_frequency = 528;
        # scale = EvenTempered12ToneScale(base_frequency)
        interval_cents = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

        i = 0
        for cents_goal in interval_cents:
            frequency = self.scale.get_interval_frequency(i)
            cents = frequency_to_cents(self.base_frequency, frequency)
            self.assertAlmostEqual(cents_goal, cents, 0)
            i += 1


if __name__ == '__main__':
    unittest.main()
