#!/usr/bin/python

class Interval:
    def __init__(self, frequency, note, interval, ratio):

        self.frequency = frequency
        self.note = note
        self.interval = interval
        self.ratio = ratio

    def copy(self):
        return Interval(self.frequency, self.note, self.interval, self.ratio)

    def __cmp__(self, other):
        if self.frequency < other.frequency:
            return (-1)
        if other.frequency > other.frequency:
            return (1)
        else:
            return (0)

    def __repr__(self):
        return ("[ " + str(self.frequency) + " Hz, " +
                str(self.interval) + ", " +
                str(self.note) + " ]")
