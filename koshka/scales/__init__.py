from even_tempered import EvenTempered
from pythag_series import PythagSeries, PythagDodecaphonic, PythagChromaticScale
from ptolemy_natural_chromatic import PtolemyNaturalChromatic
from harmonic_series import HarmonicSeries
from meantone import Meantone, Meantone12Tone

from exceptions import Exception

SCALES = [EvenTempered, PythagSeries, PythagChromaticScale, PythagDodecaphonic, PtolemyNaturalChromatic, Meantone, Meantone12Tone]

def parse(args):
    name = args[0]
    base_frequency = int(args[1])

    if name == 'EvenTemp':
        return EvenTempered(base_frequency)
    elif name == 'EvenTempered':
        return EvenTempered(base_frequency)
    elif name == 'Pythag':
        return PythagSeries(base_frequency)
    elif name == 'PythagChromaticScale':
        return PythagChromaticScale(base_frequency)
    elif name == 'PythagDodecaphonic':
        return PythagDodecaphonic(base_frequency)
    elif name == 'PtolemyNaturalChromatic':
        return PtolemyNaturalChromatic(base_frequency)
    elif name == 'Meantone':
        return Meantone(base_frequency)
    elif name == 'Meantone12Tone':
        return Meantone12Tone(base_frequency)


    raise Exception('Unknown scale: %s' % name)
