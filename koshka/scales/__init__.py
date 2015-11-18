from even_tempered import EvenTempered
from pythag_series import PythagSeries, PythagSeriesDodecaphonic, PythagChromaticScale
from harmonic_series import HarmonicSeries

from exceptions import Exception


def parse(args):
    name = args[0]
    base_frequency = int(args[1])

    if name == 'EvenTemp':
        return EvenTempered(base_frequency)
    elif name == 'Pythag':
        return PythagSeries(base_frequency)
    elif name == 'PythagChromaticScale':
        return PythagChromaticScale(base_frequency)
    elif name == 'PythagDodecaphonic':
        return PythagSeriesDodecaphonic(base_frequency)

    raise Exception('Unknown scale: %s' % name)
