# Koshka - Group project for MPS 2015

##Homework 8
### Excecution
The current version of Koshka is able to play Ptolemy's scale and the Bembe Wheel described in score files located in teh folder ./scores/

The two parts of the homework can be played with the two commands:

```
./koshka/koshka.py scores/ptolemy_scale.txt --no_gui
./koshka/koshka.py scores/bembe_wheel.txt --no_gui --loop 1
```

Alternatively the solutions can also be played using the GUI:

```
./koshka/koshka.py scores/ptolemy_scale.txt
./koshka/koshka.py scores/bembe_wheel.txt
```

### Unit test
The unit test for homework 8 can be executed uing 

```
python -m unittest discover TestPtolemy 
```
TODO: Or something similar
