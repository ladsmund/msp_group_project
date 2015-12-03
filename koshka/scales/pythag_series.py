#!/usr/bin/python

import math
from fractions import Fraction
from scale import Scale
from interval import Interval


class PythagSeries(Scale):
    base = Fraction(3, 2)

    # Returns the frequncy of the given interval
    def _get_frequency(self, interval):
        ratio = self._get_ratio(interval)
        return float(self.base_frequency) * ratio

    # Returns the fractional ratio of the given interval
    @staticmethod
    def _get_interval_ratio(interval):
        base_ratio = PythagSeries.base
        if interval < 0:
            # If the interval is negative, treat it as positive
            # and then return the reciprocal
            inverted_fraction = Fraction(math.pow(base_ratio, -interval))
            fraction = Fraction(inverted_fraction.denominator,
                                inverted_fraction.numerator)
        else:
            fraction = Fraction(math.pow(base_ratio, interval))
        return str(fraction)

    # Returns the fractional ratio of the given interval, adjusted to
    # the first octave
    def _get_ratio(self, interval):
        ratio = Fraction(self._get_interval_ratio(interval))
        while ratio < 1:
            ratio *= 2
        while ratio > 2:
            ratio /= 2
        return ratio

    # Returns a list of Interval objects for the natural pythagorean scale
    def get_intervals(self):
        scale = []
        notes = ["F", "C", "G", "D", "A", "E", "B", "C"]
        intervals = ["4", "1", "5", "M2", "M6", "M3", "M7", "1"]
        for i in range(-1, 6):
            frequency = self._get_frequency(i)
            ratio = self._get_ratio(i)
            interval = Interval(frequency, notes.pop(0),
                                intervals.pop(0), ratio)
            scale.append(interval)
        scale.sort()
        return (scale)

    def print_spacings(self):
        for i in range(1, 8):
            print(self.get_spacing(i, i + 1))


class PythagChromaticScale(PythagSeries):
    def get_intervals(self):
        scale = []
        notes = ["Db/C#", "Ab/G#", "Eb/D#", "Bb/A#", \
                 "F", "C", "G", "D", "A", "E", "B", "Gb/F#"]
        intervals = ["m2", "m6", "m3", "m7", \
                     "4", "1", "5", "M2", "M6", "M3", "M7", "b5"]
        for i in range(-5, 7):
            frequency = self._get_frequency(i)
            ratio = self._get_ratio(i)
            interval = Interval(frequency, notes.pop(0),
                                intervals.pop(0), ratio)
            scale.append(interval)
        scale.sort()
        return (scale)


class PythagDodecaphonic(PythagSeries):
    def get_intervals(self):
        scale = []
        notes = ["Gb/F+", "Db/C#", "Ab/G#", "Eb/D#", "Bb/A#", \
                 "F", "C", "G", "D", "A", "E", "B", "Gb/F#"]
        intervals = ["b5 (-)", "m2", "m6", "m3", "m7", \
                     "4", "1", "5", "M2", "M6", "M3", "M7", "b5 (+)"]
        for i in range(-6, 7):
            frequency = self._get_frequency(i)
            ratio = self._get_ratio(i)
            interval = Interval(frequency, notes.pop(0),
                                intervals.pop(0), ratio)
            scale.append(interval)
        scale.sort()
        return (scale)

