#!/usr/bin/python

import math
import fractions
from scale import Scale
from interval import Interval

def frequency_to_cents(base_frequency, frequency):
    ratio = 1. * frequency / base_frequency
    return 1200 * math.log(ratio,2)

class EvenTempered(Scale):

    exponent = fractions.Fraction("1/12")
    semitone_factor = pow(2, exponent)

    def get_scaletone_frequency(self, interval):
        frequency = self.base_frequency
        frequency *= self.semitone_factor ** interval
        return frequency

    def get_chromatic_scale(self):
        frequency = self.base_frequency
        frequency_list = [frequency]
        for i in range(0, 12):
            frequency_list.append(self.get_scaletone_frequency(i))
        return frequency_list

    # Return list of Interval objects for chromatic even tempered scale
    def get_chromatic_intervals(self):
        notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", \
                 "G#/Ab", "A", "A#/Bb", "B", "C", ]
        intervals = ["1", "m2", "M2", "m3", "M3", "4", "b5", "5", \
                     "m6", "M6", "m7", "M7", "1", ]
        interval_list = [ \
            Interval(self.base_frequency, notes.pop(0), intervals.pop(0))]
        for i in range(0, 12):
            interval_list.append \
                (Interval \
                     (interval_list[i].frequency * self.semitone_factor, \
                      notes.pop(0), \
                      intervals.pop(0) \
                      ))
        return interval_list

    def get_spacing(self, low, high):
        low_frequency = self.get_scaletone_frequency(low)
        high_frequency = self.get_scaletone_frequency(high)
        spacing = high_frequency - low_frequency
        return str(spacing)

    def get_cents(self, ratio=None, low=None, high=None):
        if ratio:
            return (Scale.get_cents(self, ratio))
        else:
            intervals = ["1", "m2", "M2", "m3", "M3", "4", "b5", "5", "m6", \
                         "M6", "m7", "M7", "1o"]
            degrees = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            d = dict(zip(intervals, degrees))
            low = d[low]
            high = d[high]
            return (100 * (high - low))


class EvenTemperedScale(EvenTempered):

    def __init__(self, base_frequency):
        Scale.__init__(self, base_frequency)
        self.intervals = self.get_chromatic_intervals()

    def get_interval_frequency(self, interval):
        interval = int(interval)
        interval_adjusted = interval % 12
        interval_octave = interval / 12
        return self.intervals[interval_adjusted].frequency \
               * 2 ** interval_octave