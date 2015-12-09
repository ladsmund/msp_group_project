from exceptions import Exception

from scalesynth import ScaleSynth
from perfect_triads import PerfectTriads
from sampler import SingleSoundSampler, Sampler
from drumset import Drumset
import scales

scale_synth_cnt = 0
drumset_cnt = 0
sampler_cnt = 0


def parse(args, sample_rate, buffer_size):
    name = args[0]

    if name == ScaleSynth.__name__:
        scale = scales.parse(args[1:])
        instrument = ScaleSynth(sample_rate, buffer_size, scale)
        global scale_synth_cnt
        instrument.name_id = instrument.name_id + str(scale_synth_cnt)
        scale_synth_cnt += 1
        return instrument

    elif name == SingleSoundSampler.__name__:
        instrument = SingleSoundSampler(args[1])
        return instrument

    elif name == Sampler.__name__:
        instrument = Sampler(args[1:])
        global sampler_cnt
        instrument.name_id = instrument.name_id + str(sampler_cnt)
        sampler_cnt += 1
        return instrument

    elif name == PerfectTriads.__name__:
        scale = scales.parse(args[1:])
        instrument = PerfectTriads(sample_rate, buffer_size, scale)
        return instrument

    elif name == Drumset.__name__:
        kick = Drumset.KICK
        snare = Drumset.SNARE
        hihat = Drumset.HIHAT
        crash = Drumset.CRASH
        tom1 = Drumset.TOM1
        tom2 = Drumset.TOM2
        ride = Drumset.RIDE
        i = 0
        while i < len(args):
            if args[i] == 'kick':
                kick = args[i + 1]
                i += 1
            elif args[i] == 'snare':
                snare = args[i + 1]
                i += 1
            elif args[i] == 'hihat':
                hihat = args[i + 1]
                i += 1
            elif args[i] == 'crash':
                crash = args[i + 1]
                i += 1
            elif args[i] == 'tom1':
                tom1 = args[i + 1]
                i += 1
            elif args[i] == 'tom2':
                tom2 = args[i + 1]
                i += 1
            elif args[i] == 'ride':
                ride = args[i + 1]
                i += 1
            i += 1
            instrument = Drumset(kick=kick,
                                 snare=snare,
                                 tom1=tom1,
                                 tom2=tom2,
                                 hihat=hihat,
                                 crash=crash,
                                 ride=ride)
            global drumset_cnt
            instrument.name_id = instrument.name_id + str(drumset_cnt)
            drumset_cnt += 1
            return instrument


    raise Exception('Unknown instrument: %s' % name)
