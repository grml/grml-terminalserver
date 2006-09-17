#!/usr/bin/python2.4

import timeit

from_subprocess = timeit.Timer('modcalc.modulesFromSubprocess()', 'import modcalc')

from_own = timeit.Timer('modcalc.modulesFromOwn()', 'import modcalc')
from_own_fileinput = timeit.Timer('modcalc.modulesFromOwnFileinput()', 'import modcalc')

def printTime(name, timelist):
    mintime = min(timelist)
    print name + ':', mintime, mintime/5

time_sub = from_subprocess.repeat(10, 5)
printTime('modulesFromSubprocess()', time_sub)

time_own = from_own.repeat(10, 5)
printTime('modulesFromOwn()', time_own)

time_own_fileinput = from_own_fileinput.repeat(10, 5)
printTime('modulesFromOwnFileinput()', time_own_fileinput)
