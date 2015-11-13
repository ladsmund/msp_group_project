#!/usr/bin/python

import math
from fractions import Fraction
from scale import Scale
from interval import Interval

class HarmonicSeries(Scale):
  
  def __init__(self, base_frequency):
    self.base_frequency = base_frequency
    
  def get_frequency(self, harmonic_degree):
    frequency = self.base_frequency * harmonic_degree
    return frequency

  def get_ratio(self, harmonic_degree):
    ratio = "{0}/1".format(harmonic_degree)
    return ratio

  def get_octave(self, harmonic_degree):
    octave_intermediate = math.log(harmonic_degree + 1) / math.log(2)
    octave = math.ceil(octave_intermediate)
    return int(octave)

  def get_denom(self, harmonic_degree):
    octave = self.get_octave(harmonic_degree)
    denom = math.pow(2, octave - 1)
    return int(denom)

  def get_adj_ratio(self, harmonic_degree):
    denom = self.get_denom(harmonic_degree)
    ratio = "{0}/{1}".format(harmonic_degree, denom)
    return ratio

  def get_reduced_ratio(self, harmonic_degree):
    adj_ratio = self.get_adj_ratio(harmonic_degree)
    ratio = Fraction(adj_ratio)
    if ratio == 1:
      ratio = "1/1"
    return ratio

  def get_decimal(self, harmonic_degree):
    denom = self.get_denom(harmonic_degree)
    decimal = float(harmonic_degree) / float(denom)
    return decimal

  def get_low_freq(self, harmonic_degree):
    denom = self.get_denom(harmonic_degree)
    frequency = self.get_frequency(harmonic_degree)
    lowest_octave_frequency = float(frequency) / float(denom)
    return lowest_octave_frequency

  def show(self):
    for d in range(1, 33):
      line = [self.get_ratio(d), \
              self.get_frequency(d), \
              self.get_octave(d), \
              self.get_denom(d), \
              self.get_adj_ratio(d), \
              self.get_reduced_ratio(d), \
              self.get_decimal(d), \
              self.get_low_freq(d)]
      print(d),
      for item in line:
        print("\t" + str(item)),
      print("")

  def get_fifth_octave_intervals(self):
    interval_list = []
    notes = [ "C", "C#-", "D", "Eb-", "E", "F-", "F#b", "F#+", "G", "Ab-", \
              "Ab#", "A+", "Bb", "Bb+", "B", "B#" ]
    intervals = [ "1", "m2", "M2", "m3", "M3", "4", "b5", "b5", "5", "m6", \
                  "M6", "M6", "m7", "m7", "M7", "M7" ]
    for d in range(16, 32):
      interval_list.append(Interval(self.get_low_freq(d), \
                                    notes.pop(0), \
                                    intervals.pop(0)))
    return(interval_list)

  def get_spacing(self, low, high):
    low_ratio = Fraction(self.get_reduced_ratio(low))
    high_ratio = Fraction(self.get_reduced_ratio(high))
    #print(low_ratio)
    #print(high_ratio)
    numerator = high_ratio.numerator * low_ratio.denominator
    denominator = high_ratio.denominator * low_ratio.numerator
    spacing = Fraction(numerator, denominator)
    return str(spacing)

  # Return integer value in cents when given a ratio or two harmonic degree
  # intervals (use keywords; e.g. ratio=ratio_var, low=low_var, etc)
  def get_cents(self, ratio=None, low=None, high=None):
    if ratio:
      return(Scale.get_cents(self, ratio))
    else:
      intervals = [ "1", "M2", "M3", "4", "5", "M6", "M7", "1o" ]
      degrees = [ 1, 18, 20, 21, 3, 27, 30, 2 ]
      return(Scale.get_cents(self, low=low, high=high, \
             intervals=intervals, degrees=degrees))


