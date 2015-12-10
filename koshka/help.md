Koshka sequencer overview
=========================

##Grid sequencer

* The grid sequencer contains the sequence of notes which will be looped when the sequencer is active. This sequence is modifiable by the user during runtime. There is one row for each synthesized tone or sample, and one column for each beat in the measure. Each note or sample is played from left to right depending on whether it is activated in the grid. 
* Stressed beats, of which there are a variable amount, are displayed in a distinct color so it is easy to see the time signature of the measure. 
* The live progression of audible notes or samples is also visible by a distinct color that moves from left to right, indicating which is the active column.

##Instrument panel

* This by default contains two ScaleSynths and a drum sampler, and some options for them.
* The drums samples can be changed on the fly by clicking on the name of the sample, and selecting a new .wav file in the file selection window that appears.
* The ScaleSynths have options to change their display names, their base frequency, and the type of scale construction that is used to create them. To change the scale, simply select another from the drop-down list. To change the base frequency, type in a new frequency and then press "Update". 

##Keyboard and scale plots

* This shows ScaleSynth objects, which represent various constructions of scales including Pythagorean variations
* To change the scale played by the keyboard, press the radio button next to the scale name
* Once the scale that you want to play is selected, you can then click on any piano key to activate the note associated with that key. Four rows of keys on the computer’s keyboard are also mapped to keys on the application’s keyboard and can be used to play notes. The [1-0] and [q-p] rows are mapped to the lower frequency keys and the [s-k] and [z-m] rows are mapped to the higher frequency keys (frequency increased from left to right on both the computer keyboard and the application’s keyboard, just as you would find on a standard piano). 
* The scale plots are in the area below the keyboard, and represent the spacing between the notes of the scale in an easy-to-see, graphical way. The horizontal lines are the notes of the scale arranged with accurate spacing. The shadows in the background represent the position of the notes in an even-tempered scale for easy comparison. 

##Main controls

* Most importantly, here are the Start and Stop buttons for starting and stopping the sequencer.
* The control frame provides functionality for changing the division of measures into beats. Both the total number of beats possible and the actual number are displayed and changeable. To change, you modify the number and then press the “update” button. The max number of beats, or measure resolution, must be divisible by the actual number of beats.
* There is a tempo slider that controls the speed at which the sequencer moves through the grid. 

##Volume mixer

* Allows for changing the master volume in addition to the volume of each instrument that is shown in the grid sequencer.
* If not all of the individual instruments appear on the left side of the mixer, you can change the window size and/or scroll to see them.

