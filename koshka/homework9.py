#!/usr/bin/python

from dac import DAC
from sequencers.sequencer import Sequencer
import instruments

import argparse

DEFAULT_INSTRUMENT = "ScaleSynth EvenTempered 528"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='MSP homework 9')
    parser.add_argument('score', type=str)
    parser.add_argument('-i', '--instrument', type=str, default=DEFAULT_INSTRUMENT)
    namespace = parser.parse_args()

    dac = DAC(bufferSize=2 ** 10, rate=44100)
    dac.start()

    try:

        sequencer = Sequencer(buffer_size=dac.bufferSize, sample_rate=dac.getSamplerate())
        dac.connect(sequencer.callback)

        instrument = instruments.parse(namespace.instrument.split(),
                                       buffer_size=dac.bufferSize,
                                       sample_rate=dac.getSamplerate())

        sequencer.add_instrument(instrument)

        file = open(namespace.score, 'r')
        score_string = file.read()
        file.close()
        score = Sequencer.parse_mono_score(score_string)

        sequencer.play(score=score)

    finally:
        dac.stop()
