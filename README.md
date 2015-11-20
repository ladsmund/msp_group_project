# Koshka - Group project for MPS 2015
##Homework 8
By Mads Lund and Aric Werner

The current version of our project, Koshka, is able to play Ptolemy's scale and the Bembe Wheel described in score files located in teh folder ./scores/

### Excecution

The two parts of the homework and the harness test for ptolemy's scale can be runned using the shell script:
```
./homework8.sh
```

Alternatively, the pars can be runned seperatly using the commands:
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

