#!/usr/bin/python

import fractions
from scale import Scale
from interval import Interval



class EvenTempered(Scale):
    exponent = fractions.Fraction("1/12")
    semitone_factor = pow(2, exponent)

    def get_ratio(self, interval):
        return self.semitone_factor ** interval

    def get_frequency(self, interval):
        return self.base_frequency * self.get_ratio(interval)

    def get_chromatic_scale(self):
        frequency = self.base_frequency
        frequency_list = [frequency]
        for i in range(0, 12):
            frequency_list.append(self.get_frequency(i))
        return frequency_list

    # Return list of Interval objects for chromatic even tempered scale
    def get_intervals(self):
        notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", \
                 "G#/Ab", "A", "A#/Bb", "B", "C", ]
        intervals = ["1", "m2", "M2", "m3", "M3", "4", "b5", "5", \
                     "m6", "M6", "m7", "M7", "1", ]
        interval_list = []
        for i in range(0, 12):
            frequency = self.get_frequency(i)
            # frequency = interval_list[i].frequency * self.semitone_factor
            ratio = frequency / self.base_frequency
            interval = Interval(
                frequency,
                notes.pop(0),
                intervals.pop(0),
                ratio)
            interval_list.append(interval)
        return interval_list

