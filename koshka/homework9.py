#!/usr/bin/python

from dac import DAC
from sequencers.sequencer import Sequencer
import instruments 

dac = DAC(bufferSize=2048, rate=44100)
dac.start()
try:
    sequencer = Sequencer(buffer_size=dac.bufferSize, sample_rate=dac.getSamplerate()) 
    dac.connect(sequencer.callback)
    
    # Format: instrument id, tone, on, wait time (in "ticks")
    score = [(0, 4, 1, 0),
             (0, 4, 0, 1),
             (0, 2, 1, 0),
             (0, 2, 0, 1),
             (0, 0, 1, 0),
             (0, 0, 0, 1),
             (0, 2, 1, 0),
             (0, 2, 0, 1),
             (0, 4, 1, 0),
             (0, 4, 0, 3),
             (0, 0, 0, 1),
             (0, 2, 1, 0),
             (0, 2, 0, 3),
             (0, 4, 1, 0),
             (0, 4, 0, 3),
            ]

    instrument = instruments.parse("ScaleSynth EvenTempered 1000".split(), 
                                   buffer_size=dac.bufferSize, 
                                   sample_rate=dac.getSamplerate()) 
    sequencer.add_instrument(instrument)
    sequencer.play(score=score, block=True)
finally:
    dac.stop()

