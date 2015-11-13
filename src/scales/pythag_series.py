#!/usr/bin/python

import math
from fractions import Fraction
from scale import Scale
from interval import Interval


class PythagSeries(Scale):
    def __init__(self, base_frequency):
        Scale.__init__(self, base_frequency)
        self.intervals = self.get_dodecaphonic_intervals()

    base = Fraction(3, 2)

    def get_interval_frequency(self, interval):
        interval = int(interval)
        interval_adjusted = interval % 13
        interval_octave = interval / 13
        return self.intervals[interval_adjusted].frequency * 2 ** interval_octave

    # Returns the frequncy of the given interval
    def get_frequency(self, interval):
        base_ratio = PythagSeries.base
        factor = math.pow(base_ratio, interval)
        interval_freq = factor * self.base_frequency
        octave = (interval_freq // self.base_frequency) - 1
        octave_denom = math.pow(2, octave)
        factor_adjusted = factor / octave_denom
        while factor_adjusted < 1:
            # Make sure that the factor is greater than 1
            factor_adjusted = factor_adjusted * 2
        frequency = self.base_frequency * factor_adjusted
        return frequency

    # Returns the fractional ratio of the given interval
    def get_interval_ratio(self, interval):
        base_ratio = PythagSeries.base
        if interval < 0:
            # If the interval is negative, treat it as positive
            # and then return the reciprocal
            inverted_fraction = Fraction(math.pow(base_ratio, -interval))
            fraction = Fraction(inverted_fraction.denominator, \
                                inverted_fraction.numerator)
        else:
            fraction = Fraction(math.pow(base_ratio, interval))
        return str(fraction)

    # Returns the fractional ratio of the given interval, adjusted to
    # the first octave
    def get_adjusted_interval_ratio(self, interval):
        ratio = Fraction(self.get_interval_ratio(interval))
        while ratio < 1:
            ratio = ratio * 2
        while ratio > 2:
            ratio = ratio / 2
        return str(ratio)

    # Returns a list of frequencies for the natural pythagorean scale
    def get_natural_scale(self):
        scale_tones = []
        for i in range(-1, 6):
            scale_tones.append(self.get_frequency(i))
        scale_tones.sort()
        scale_tones.append(scale_tones[0] * 2)
        return scale_tones

    # Returns a list of Interval objects for the natural pythagorean scale
    def get_natural_intervals(self):
        scale = []
        notes = ["F", "C", "G", "D", "A", "E", "B", "C"]
        intervals = ["4", "1", "5", "M2", "M6", "M3", "M7", "1"]
        for i in range(-1, 6):
            interval = Interval(self.get_frequency(i), notes.pop(0), intervals.pop(0))
            scale.append(interval)
        scale.sort()
        scale.append( \
            Interval(scale[0].frequency * 2, notes.pop(0), intervals.pop(0)))
        return (scale)

    # Returns a list of frequencies for the chromatic pythagorean scale
    def get_chromatic_scale(self):
        scale_tones = []
        for i in range(-1, 13):
            scale_tones.append(self.get_frequency(i))
        scale_tones.sort()
        return scale_tones

    def get_dodecaphonic_intervals(self):
        scale = []
        notes = ["Gb/F+", "Db/C#", "Ab/G#", "Eb/D#", "Bb/A#", \
                 "F", "C", "G", "D", "A", "E", "B", "Gb/F#"]
        intervals = ["b5 (-)", "m2", "m6", "m3", "m7", \
                     "4", "1", "5", "M2", "M6", "M3", "M7", "b5 (+)"]
        for i in range(-6, 7):
            interval = Interval(self.get_frequency(i), notes.pop(0), intervals.pop(0))
            scale.append(interval)
        scale.sort()
        return (scale)

    # Returns the spacing between two given pythagorean natural intervals
    # as a fraction
    def get_spacing(self, low, high):
        scale = []
        for i in range(-1, 6):
            frequency = self.get_frequency(i)
            ratio = Fraction(self.get_adjusted_interval_ratio(i))
            scale.append([frequency, ratio])
        scale.sort()
        scale.append([scale[0][0] * 2, Fraction(2)])
        numerator = (scale[high - 1][1].numerator * scale[low - 1][1].denominator)
        denominator = (scale[high - 1][1].denominator * scale[low - 1][1].numerator)
        spacing = Fraction(numerator, denominator)
        return str(spacing)

    # Return integer value in cents when given a ratio or two pythagorean natural
    # intervals (use ratio=ratio_var, low=low_var, etc)
    def get_cents(self, ratio=None, low=None, high=None):
        if ratio:
            return (Scale.get_cents(self, ratio))
        else:
            intervals = ["1", "M2", "M3", "4", "5", "M6", "M7", "1o"]
            degrees = [1, 2, 3, 4, 5, 6, 7, 8]
            return (Scale.get_cents(self, low=low, high=high, \
                                    intervals=intervals, degrees=degrees))

    def print_spacings(self):
        for i in range(1, 8):
            print(self.get_spacing(i, i + 1))
