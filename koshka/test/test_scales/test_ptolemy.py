import unittest
from fractions import Fraction

from scales.ptolemy_natural_chromatic import PtolemyNaturalChromatic


class TestPtolemy(unittest.TestCase):
    def test_interval_ratios(self):
        base_frequency = 528
        scale = PtolemyNaturalChromatic(base_frequency)
        static_ratios = [Fraction(1, 1),
                         Fraction(16, 15),
                         Fraction(9, 8),
                         Fraction(6, 5),
                         Fraction(5, 4),
                         Fraction(4, 3),
                         Fraction(64, 45),
                         Fraction(3, 2),
                         Fraction(8, 5),
                         Fraction(5, 3),
                         Fraction(16, 9),
                         Fraction(15, 8)]
        
        for i, interval in enumerate(static_ratios):
            generated_ratio = scale.get_ratio(i)
            self.assertEqual(static_ratios[i], generated_ratio)


if __name__ == '__main__':
    unittest.main()
