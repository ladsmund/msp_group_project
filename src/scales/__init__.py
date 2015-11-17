from even_tempered import EvenTempered
from pythag_series import PythagSeries, PythagSeriesDodecaphonic, PythagSeriesSevenNoteScale
from harmonic_series import HarmonicSeries

from exceptions import Exception

def parse(args):
    name = args[0]
    base_frequency = int(args[1])

    if name == 'EvenTemp':
        return EvenTempered(base_frequency)
    elif name == 'Pythag':
        return PythagSeriesSevenNoteScale(base_frequency)
    elif name == 'PythagDodecaphonic':
        return PythagSeriesDodecaphpnic(base_frequency)

    raise Exception('Unknown scale: %s' % name)
