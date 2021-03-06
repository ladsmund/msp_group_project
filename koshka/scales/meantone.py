#!/usr/bin/python

from fractions import Fraction
from interval import Interval
from pythag_series import PythagDodecaphonic
import math


class Meantone(PythagDodecaphonic):
    '''This class builds a meantone scale based on the "reduced 5th" method,
    resulting in a quarter-comma meantone scale'''

    def _get_ratio(self, interval):
        interval_ratio_str = PythagDodecaphonic._get_ratio(self, interval)
        ratio = Fraction(interval_ratio_str)

        syntonic_comma = Fraction(81, 80)

        if interval < 0:
            adjusted_ratio = \
                ratio * math.pow(syntonic_comma, math.fabs(interval) / 4.)
        elif interval > 0:
            adjusted_ratio = \
                ratio * math.pow(math.pow(syntonic_comma, -1),
                                 math.fabs(interval) / 4.)
        else:
            adjusted_ratio = ratio

        return adjusted_ratio

    def get_intervals(self):
        scale = []
        notes = ["Gb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D",
                 "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
        intervals = ["b5 (+)", "m2 (+)", "m6 (+)", "m3 (+)", "m7 (+)",
                     "4", "1", "5", "2", "M6", "M3", "M7", "b5 (-)", "m2 (-)",
                     "m6 (-)", "m3 (-)", "m7 (-)"]
        for i in range(-6, 11):
            frequency = self._get_frequency(i)
            ratio = self._get_ratio(i)
            interval = Interval(frequency, notes.pop(0),
                                intervals.pop(0), ratio)
            scale.append(interval)
        scale.sort()
        return (scale)


class Meantone12Tone(Meantone):
    def get_intervals(self):
        scale = Meantone.get_intervals(self)

        result = []
        for et_ratio in [math.pow(2, i / 12.) for i in range(12)]:
            closest = scale[0]
            for mn_interval in scale[1:]:
                dist = abs(mn_interval.ratio - et_ratio)
                if dist < abs(closest.ratio - et_ratio):
                    closest = mn_interval

            result.append(closest)

        return result