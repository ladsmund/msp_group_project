#!/usr/bin/python

class Interval:
    def __init__(self, frequency, note, interval):

        self.frequency = frequency
        self.note = note
        self.interval = interval

        # interval = None
        # note = None

        # if degree == 1:
        #  interval = "1"
        #  note = "C"
        # elif degree == 2:
        #  interval = "m2"
        #  note = "C#/Db"
        # elif degree == 3:
        #  interval = "M2"
        #  note = "D"
        # elif degree == 4:
        #  interval = "m3"
        #  note = "D#/Eb"
        # elif degree == 5:
        #  interval = "M3"
        #  note = "E"
        # elif degree == 6:
        #  interval = "4"
        #  note = "F"
        # elif degree == 7:
        #  interval = "b5"
        #  note = "F#/Gb"
        # elif degree == 8:
        #  interval = "5"
        #  note = "G"
        # elif degree == 9:
        #  interval = "m6"
        #  note = "G#/Ab"
        # elif degree == 10:
        #  interval = "M6"
        #  note = "A"
        # elif degree == 11:
        #  interval = "m7"
        #  note = "A#/Bb"
        # elif degree == 12:
        #  interval = "M7"
        #  note = "B"
        # elif degree == 13:
        #  interval = "1"
        #  note = "C"

        # self.interval = interval
        # self.note = note

    def __cmp__(self, other):
        if self.frequency < other.frequency:
            return (-1)
        if other.frequency > other.frequency:
            return (1)
        else:
            return (0)

    def __repr__(self):
        return ("[ " + str(self.frequency) + " Hz, " + \
                str(self.interval) + ", " + \
                str(self.note) + " ]")
