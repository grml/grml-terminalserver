#!/usr/bin/python2.4

import sys
import os

def getNicModules():
    """Get all NIC modules which discover is able to find"""
    f = open('/lib/discover/pci.lst', 'r')
    import re
    ethlinefilter = re.compile('ethernet')
    modlist = filter(ethlinefilter.search, f)
    new_modlist = set()
    for i in modlist:
        tmplist = i.split('\t', 4)
        try:
            type = tmplist[2]
            mod = tmplist[3]
        except:
            continue
        if type == 'ethernet' and mod != 'unknown':
            new_modlist.add(mod)
    f.close()
    return new_modlist

def basename(p):
    """Quite faster implementation of os.path.basename, submitted and accepted"""
    i = p.rfind('/') + 1
    return p[i:]

def generateModDep():
    """Generate an in-memory represenation of all module dependencies"""
    moddep = {}
    moddepfile = open(sys.argv[1], 'r')
    for i in moddepfile:
        tmplist = i.split()
        mainmod = tmplist.pop(0)
        mainmod = mainmod.rstrip(':')
        rawmod = mainmod.rstrip('.ko')
        rawmod = basename(rawmod)
        newlist = []
        newlist.append((rawmod, mainmod))
        for i in tmplist:
            a = i.rstrip('.ko')
            a = basename(a)
            newlist.append((a, i))
        moddep[rawmod] = newlist
    moddepfile.close()
    return moddep

def generateOutput(modlist, moddep):
    """Function to filter all keys from moddep not in modlist"""
    output = {}
    for i in modlist:
        try:
            for (j, k) in moddep[i]:
                output[j] = k
        except:
            continue
    return output

def calculateModuleDep():
    modlist = getNicModules()
    moddep = generateModDep()
    output = generateOutput(modlist, moddep)
    return output.values()

#############################################################################

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Error: you should give me the path to your modules.dep'
        sys.exit(1)

    for i in calculateModuleDep():
        print i
