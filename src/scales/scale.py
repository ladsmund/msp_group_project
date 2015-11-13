#!/usr/bin/python

import math
from fractions import Fraction


class Scale:
    def __init__(self, base_frequency):
        self.base_frequency = base_frequency

    # Given a ratio, returns an integer in cents
    # Given a low and high interval, an interval lists, and a degree list,
    # will find the proper ratio and call itself
    def get_cents(self, ratio=None, low=None, high=None, \
                  intervals=None, degrees=None):
        if ratio:
            f = Fraction(ratio)
            c = (1200 * (math.log(f) / math.log(2)))
            return (int(round(c)))
        else:
            d = dict(zip(intervals, degrees))
            low = d[low]
            high = d[high]
            f = Fraction(self.get_spacing(low, high))
            c = Scale.get_cents(self, f)
            return (c)
