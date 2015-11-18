#!/usr/bin/python

from fractions import Fraction
from pythag_series import PythagChromaticScale


class PtolemyNaturalChromatic(PythagChromaticScale):

    def _get_ratio(self, interval):
        # First get the pythagorean intervals
        interval_ratio_str = PythagChromaticScale._get_ratio(self, interval)
        ratio = Fraction(interval_ratio_str)

        # We will be adjusting by using these
        syntonic_comma = Fraction("81/80")
        dim_fifth = Fraction("64/45")

        if interval == -5:
            ratio = ratio * syntonic_comma
        elif interval == -3:
            ratio = ratio * syntonic_comma
        elif interval == 4:
            ratio = ratio / syntonic_comma
        elif interval == -4:
            ratio = ratio * syntonic_comma
        elif interval == 3:
            ratio = ratio / syntonic_comma
        elif interval == 5:
            ratio = ratio / syntonic_comma
        elif interval == 6:
            ratio = dim_fifth

        return ratio

