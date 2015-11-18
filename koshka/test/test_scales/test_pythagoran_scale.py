__author__ = 'Mads Christian Lund (mcl574)'
import unittest
from scales.pythag_series import PythagSeries, PythagSeriesDodecaphonic
from fractions import Fraction


class TestPythagoranScale(unittest.TestCase):
    def setUp(self):
        self.base_frequency = 528
        self.scale = PythagSeries(self.base_frequency)

    def test_get_spacing(self):
        '''
        This harness test is testing features related to Homework 4
        '''

        space_fractions = {(0, 1): Fraction(9, 8),
                           (1, 2): Fraction(9, 8),
                           (2, 3): Fraction(256, 243),
                           (3, 4): Fraction(9, 8),
                           (4, 5): Fraction(9, 8),
                           (5, 6): Fraction(9, 8),
                           (6, 7): Fraction(256, 243)}

        for (l, h) in space_fractions.keys():
            self.assertEqual(self.scale.get_spacing(l, h), space_fractions[(l, h)])

    # def test_get_modes(self):
    #     '''
    #     This harness test is testing features related to Homework 3
    #     '''
    #
    #     # Theses mode frequencies are values copied from the excel spreadsheet.
    #     mode_frequencies = {0: [528.00, 594.00, 668.25, 704.00, 792.00, 891.00, 1002.375, 1056.00],
    #                         1: [594.00, 668.25, 704.00, 792.00, 891.00, 1002.375, 1056.00, 1188.00],
    #                         2: [668.25, 704.00, 792.00, 891.00, 1002.375, 1056.00, 1188.00, 1336.50],
    #                         3: [704.00, 792.00, 891.00, 1002.375, 1056.00, 1188.00, 1336.50, 1408.00],
    #                         4: [792.00, 891.00, 1002.375, 1056.00, 1188.00, 1336.50, 1408.00, 1584.00],
    #                         5: [891.00, 1002.375, 1056.00, 1188.00, 1336.50, 1408.00, 1584.00, 1782.00],
    #                         6: [1002.375, 1056.00, 1188.00, 1336.50, 1408.00, 1584.00, 1782.00, 2004.75],
    #                         7: [1056.00, 1188.00, 1336.50, 1408.00, 1584.00, 1782.00, 2004.75, 2112.00]}
    #
    #     for mode in mode_frequencies.keys():
    #         base_frequency = mode_frequencies[mode][0]
    #         ps = get_mode(base_frequency, mode)
    #
    #         tone = 0
    #         for frequency_expected in mode_frequencies[mode]:
    #             frequency = ps.get_frequency(tone)
    #             self.assertAlmostEqual(frequency, frequency_expected,
    #                                    msg='Mode: %i, tone: %i. Got %0.3fHz expexted %0.3fHz' % (
    #                                        mode, tone, frequency, frequency_expected))
    #             tone += 1

    # def test_get_frequencies(self):
    #     '''
    #     This harness test is testing features related to Homework 2
    #     '''
    #
    #     values = [(-1, 704.),
    #               (0, 528.),
    #               (1, 792.),
    #               (2, 594.),
    #               (3, 891.),
    #               (4, 668.25),
    #               (5, 1002.375),
    #               (6, 751.78125),
    #               (7, 563.8359375),
    #               (8, 845.75390625),
    #               (9, 634.3154296875),
    #               (10, 951.47314453125),
    #               (11, 713.604858398437),
    #               (12, 535.203643798828)]
    #
    #     for (i, f) in values:
    #         freq = self.scale.get_frequency(i)
    #         self.assertAlmostEqual(freq, f, places=11)

    def test_frequecies(self):
        # base_frequency = 528;
        # scale = Pythagorean7ToneScale(base_frequency)
        interval_frequencies = [528, 594, 668, 704, 792, 891, 1002]

        i = 0
        for f in interval_frequencies:
            self.assertAlmostEqual(f, self.scale.get_frequency(i), 0)
            i += 1

    # def test_interval_names(self):
    #     interval_names = ["1","M2","M3","4","5","M6","M7","1"]
    #     # scale = Pythagorean7ToneScale()
    #
    #     i = 0
    #     for name in interval_names:
    #         self.assertSequenceEqual(self.scale.interval_to_interval_name(i),name)
    #         i += 1
    #
    # def test_tone_names(self):
    #     tone_names = ['C','D','E','F','G','A','B','C']
    #     scale = Pythagorean7ToneScale()
    #
    #     i = 0
    #     for name in tone_names:
    #         self.assertSequenceEqual(scale.interval_to_tone_name(i).strip(' '),name)
    #         i += 1

    def test_get_fraction(self):
        fractions = [Fraction(1, 1), Fraction(9, 8), Fraction(81, 64), Fraction(4, 3), Fraction(3, 2), Fraction(27, 16),
                     Fraction(243, 128), Fraction(2, 1)]
        i = 0
        for fraction in fractions:
            self.assertEqual(self.scale.get_ratio(i), fraction)
            i += 1

    def test_interval_cents(self):
        interval_cents = [0, 204, 408, 498, 702, 906, 1110, 1200]

        i = 0
        for cents_goal in interval_cents:
            cents = self.scale.get_cents(i)
            self.assertAlmostEqual(cents_goal, cents, 0)
            i += 1


class TestPythagoranDodecaphinicScale(unittest.TestCase):
    def setUp(self):
        self.base_frequency = 528
        self.scale = PythagSeriesDodecaphonic(self.base_frequency)

    def test_interval_frequecies(self):
        interval_frequencies = [528, 556, 594, 626, 668, 704, 742, 752, 792, 834, 891, 939, 1002]

        i = 0
        for f in interval_frequencies:
            self.assertAlmostEqual(f, self.scale.get_frequency(i), 0)
            i += 1


if __name__ == '__main__':
    unittest.main()
