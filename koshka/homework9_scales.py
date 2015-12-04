#!/usr/bin/python

import argparse
import scales

SCALE_NAME_LEN = 12
DEFAULT_BASE_FREQUENCY = 528

if __name__ == '__main__':
    scale_args = "The supported scales are: "+", ".join(map(lambda x: x.__name__,scales.SCALES))

    parser = argparse.ArgumentParser(description='MSP homework 9 scale interval comparison')
    parser.add_argument('scale0', type=str, help=scale_args)
    parser.add_argument('scale1', type=str, help="Same as scale0")
    parser.add_argument('-f', '--basefreq', type=int, default=DEFAULT_BASE_FREQUENCY)
    parser.add_argument('-i', '--intervals', type=str)
    namespace = parser.parse_args()

    scale0 = scales.parse([namespace.scale0, namespace.basefreq])
    scale1 = scales.parse([namespace.scale1, namespace.basefreq])

    if namespace.intervals:
        intervals = map(int, namespace.intervals.split())
    else:
        intervals = range(len(scale0) + 1)

    for interval in intervals:

        s0c = scale0.get_cents(interval)
        s0f = scale0.get_frequency(interval)
        s1c = scale1.get_cents(interval)
        s1f = scale1.get_frequency(interval)

        name0 = type(scale0).__name__
        if len(name0) > SCALE_NAME_LEN:
            name0 = name0[0:SCALE_NAME_LEN]
        name1 = type(scale1).__name__
        if len(name1) > SCALE_NAME_LEN:
            name1 = name1[0:SCALE_NAME_LEN]

        print "-" * 35
        print "Interval {:n}".format(interval)
        print ("{:<%i}: {:>7.1f} Hz {:>7.1f} cents" % SCALE_NAME_LEN).format(name0, s0f, s0c)
        print ("{:<%i}: {:>7.1f} Hz {:>7.1f} cents" % SCALE_NAME_LEN).format(name1, s1f, s1c)
        print ("{:<%i}: {:>7.1f} Hz {:>7.1f} cents" % SCALE_NAME_LEN).format("Difference", s1f - s0f, s1c - s0c)
