import unittest
from fractions import Fraction

from scales.meantone import Meantone


class TestMeantone(unittest.TestCase):
    def test_interval_ratios(self):
        base_frequency = 528
        scale = Meantone(base_frequency)
        static_ratios = [1,
                         1.04490,
                         1.06998,
                         1.11803,
                         1.16824,
                         1.19627,
                         1.25,
                         1.33748,
                         1.39754,
                         1.43108,
                         1.49535,
                         1.5625,
                         1.6,
                         1.67185,
                         1.74693,
                         1.78885,
                         1.86919]

        for i, interval in enumerate(static_ratios):
            generated_ratio = scale.get_ratio(i)
            self.assertAlmostEqual(static_ratios[i], generated_ratio, 
                                   places = 4)


if __name__ == '__main__':
    unittest.main()
