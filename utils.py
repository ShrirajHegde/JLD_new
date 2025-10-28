import math


def printTime(value, timeBase):
    """Format time in milliseconds"""
    value_ms = value / (1000 / timeBase)
    return "%s ms" % (value_ms)


def hyperperiod(tasks):
    """Hyperperiod of the taskset"""
    periods = set([t.period for t in tasks])
    return math.lcm(*periods)
