#!/usr/bin/python

import math


class Scale:
    def __init__(self, base_frequency):
        self.base_frequency = base_frequency
        self.intervals = self.get_intervals()
        self.scale_size = len(self.intervals)

    # This function should be overridden by the sub-classes
    def get_intervals(self):
        return []

    def get_interval(self, index):
        index = int(index)
        index_adjusted = index % self.scale_size
        octave = index / self.scale_size

        interval = self.intervals[index_adjusted]
        interval.frequency *= 2 ** octave
        interval.ratio *= 2 ** octave
        return interval

    def get_frequency(self, interval):
        return self.get_interval(interval).frequency

    def get_ratio(self, interval):
        '''Returns the spacing between two given intervals as a fraction'''
        return self.get_interval(interval).ratio

    def get_spacing(self, low, high):
        return self.get_ratio(high) / self.get_ratio(low)

    def get_cents(self, interval):
        ratio = self.get_ratio(interval)
        return 1200 * math.log(ratio, 2)
