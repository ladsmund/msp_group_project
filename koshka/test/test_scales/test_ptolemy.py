import unittest
from fractions import Fraction

from scales import PythagSeries


class TestPtolemy(unittest.TestCase):

    def test_interval_ratios(self):
        base_frequency = 528
        scale = PythagSeries(base_frequency)
        static_ratios = [ Fraction(1,1), 
                            Fraction(16,15), 
                            Fraction(9,8), 
                            Fraction(6,5), 
                            Fraction(5,4), 
                            Fraction(4,3), 
                            Fraction(64,45), 
                            Fraction(3,2), 
                            Fraction(8,5), 
                            Fraction(5,3), 
                            Fraction(16,9), 
                            Fraction(15,8) ]
        generated_ratios = []
        for i in range(-5, 7):
            generated_ratios.append(scale.get_ptolemy_ratio(i))
        generated_ratios.sort()
        for i, interval in enumerate(static_ratios):
            self.assertEqual(generated_ratios[i], static_ratios[i])

if __name__ == '__main__':
    unittest.main()
