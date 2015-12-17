# Koshka - Group project for MSP 2015

##Final Version
By Mads Lund and Aric Werner

This is the final version of our project Koshka for Music Software Project 2015.

###Excecution
Run Koshka using the executable file:
```
./koshka/koshka.py
```

A score can also be run without GUI using the command line:

```
usage: koshka.py [-h] [--no_gui [NO_GUI]] [-l [LOOP]] [score]

Koshka - MSP project

positional arguments:
  score

optional arguments:
  -h, --help            show this help message and exit
  --no_gui [NO_GUI]
  -l [LOOP], --loop [LOOP]
```

### Online Help
The online help can be found [here](koshka/help.md)

##Homework 9
By Mads Lund and Aric Werner

The homework solution is implemented with the two Python programs and the required deliverables and be executed with the command: ```./homework9.sh```.

#### Unit test / Harness test
The unit test for homework 9 can be executed using the command:
```
python -m unittest discover -p *meantone* koshka/
```

There is no explicit unit test for interval comparison since the correctness of the interval are already tested and the comparisons are only differences.

###Melody playback
```homework9.py``` is a program able to play a monophonic melody encoded with a simple file format. The melody *Mary had a little lamb* is encoded in this format in the file ```scores/mary.mscore```.

###Interval Comparison
```homework9_scale.py``` is a program for comparing frequencies and cents between different intervals and between tuning systems.

```
usage: homework9_scales.py [-h] [-f BASEFREQ] [-i INTERVALS0] [-i1 INTERVALS1]
                           scale0 scale1

MSP homework 9 scale interval comparison

positional arguments:
  scale0                The supported scales are: EvenTempered, PythagSeries,
                        PythagChromaticScale, PythagDodecaphonic,
                        PtolemyNaturalChromatic, Meantone, Meantone12Tone
  scale1                Same as scale0

optional arguments:
  -h, --help            show this help message and exit
  -f BASEFREQ, --basefreq BASEFREQ
  -i INTERVALS0, -i0 INTERVALS0, --intervals0 INTERVALS0
                        List of interval for scale0. Default: all interval in
                        an octave.
  -i1 INTERVALS1, --intervals1 INTERVALS1
                        List of interval for scale1. Default: the same as
                        intervals0
```


##Homework 8
By Mads Lund and Aric Werner

The current version of our project, Koshka, is able to play Ptolemy's scale and the Bembe Wheel described in score files located in the folder ./scores/

### Execution

The two parts of the homework and the harness test for Ptolemy's scale can be run using the shell script:
```
./homework8.sh
```

Alternatively, the parts can be runned seperatly using the commands:
```
./koshka/koshka.py scores/ptolemy_scale.txt --no_gui
./koshka/koshka.py scores/bembe_wheel.txt --no_gui --loop 1
```

And with GUI:
```
./koshka/koshka.py scores/ptolemy_scale.txt
./koshka/koshka.py scores/bembe_wheel.txt
```

#### Unit test / Harness test
The unit test for homework 8 can be executed using the command:
```
python -m unittest discover -p *ptolemy* koshka/
```

