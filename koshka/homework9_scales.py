#!/usr/bin/python

import argparse
import scales

SCALE_NAME_LEN = 12
DEFAULT_BASE_FREQUENCY = 528

if __name__ == '__main__':
    scale_args = "The supported scales are: " + ", ".join(map(lambda x: x.__name__, scales.SCALES))

    parser = argparse.ArgumentParser(description='MSP homework 9 scale interval comparison')
    parser.add_argument('scale0', type=str, help=scale_args)
    parser.add_argument('scale1', type=str, help="Same as scale0")
    parser.add_argument('-f', '--basefreq', type=int, default=DEFAULT_BASE_FREQUENCY)
    parser.add_argument('-i', '-i0', '--intervals0', type=str,
                        help='List of interval for scale0. Default: all interval in an octave.')
    parser.add_argument('-i1', '--intervals1', type=str,
                        help='List of interval for scale1. Default: the same as intervals0')
    namespace = parser.parse_args()

    scale0 = scales.parse([namespace.scale0, namespace.basefreq])
    scale1 = scales.parse([namespace.scale1, namespace.basefreq])

    if namespace.intervals0:
        intervals0 = map(int, namespace.intervals0.split())
    else:
        intervals0 = range(len(scale0) + 1)

    if namespace.intervals1:
        intervals1 = map(int, namespace.intervals1.split())
        assert (len(intervals0) == len(intervals1))
    else:
        intervals1 = intervals0

    intervals = zip(intervals0, intervals1)

    for (interval0, interval1) in intervals:

        s0c = scale0.get_cents(interval0)
        s0f = scale0.get_frequency(interval0)
        s1c = scale1.get_cents(interval1)
        s1f = scale1.get_frequency(interval1)

        name0 = type(scale0).__name__
        if len(name0) > SCALE_NAME_LEN:
            name0 = name0[0:SCALE_NAME_LEN]
        name1 = type(scale1).__name__
        if len(name1) > SCALE_NAME_LEN:
            name1 = name1[0:SCALE_NAME_LEN]

        print "-" * 35
        print ("{:<%i} {:2n}: {:>7.1f} Hz {:>7.1f} cents" % SCALE_NAME_LEN).format(name0, interval0, s0f, s0c)
        print ("{:<%i} {:2n}: {:>7.1f} Hz {:>7.1f} cents" % SCALE_NAME_LEN).format(name1, interval1, s1f, s1c)
        print ("{:<%i}     {:>7.1f} Hz {:>7.1f} cents" % SCALE_NAME_LEN).format("Difference:", s1f - s0f, s1c - s0c)
