#!/usr/bin/python2.4

import sys
import os
import fileinput


def modulesFromSubprocess():
    import subprocess
    return subprocess.Popen('awk "/ethernet/{print \$3}" /lib/discover/pci.lst |sort |uniq',
            stdout=subprocess.PIPE, shell=True).communicate()[0].splitlines()

def modulesFromOwnFileinput():
    modlist = []
    for i in fileinput.input('/lib/discover/pci.lst'):
        #i = i.lstrip(' \t')
        tmplist = i.split('\t', 3)
        try:
            type = tmplist[2]
            mod = tmplist[3]
        except:
            continue
        if type == 'ethernet' and mod != 'unknown':
            modlist.append(mod)
    fileinput.close()
    return modlist

def modulesFromOwn():
    modlist = set()
    f = open('/lib/discover/pci.lst', 'r')
    for i in f:
        #i = i.lstrip(' \t')
        tmplist = i.split('\t', 4)
        try:
            type = tmplist[2]
            mod = tmplist[3]
        except:
            continue
        if type == 'ethernet' and mod != 'unknown':
            modlist.add(mod)
    f.close()
    return modlist

def modulesFromOwn2():
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
    i = p.rfind('/') + 1
    return p[i:]

def osbasename(p):
    return os.path.split(p)[1]

def generateModDep_basename():
    moddep = {}
    moddepfile = open(sys.argv[1], 'r')
    for i in moddepfile:
        tmplist = i.split()
        mainmod = tmplist.pop(0)
        mainmod = mainmod.rstrip(':')
        rawmod = mainmod.rstrip('.ko')
        rawmod = osbasename(rawmod)
        newlist = []
        newlist.append((rawmod, mainmod))
        for i in tmplist:
            a = i.rstrip('.ko')
            a = osbasename(a)
            newlist.append((a, i))
        moddep[rawmod] = newlist
    moddepfile.close()
    return moddep

def generateModDep_mybasename():
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

def ossplit(p):
    i = p.rfind('/') + 1
    head, tail = p[:i], p[i:]
    if head and head != '/'*len(head):
        head = head.rstrip('/')
    return head, tail

def split(p):
    i = p.rfind('/') + 1
    head, tail = p[:i], p[i:]
    head = head.rstrip('/')
    if not head:
        head = '/'
    return head, tail

def generateModDep_split():
    moddep = {}
    moddepfile = open(sys.argv[1], 'r')
    for i in moddepfile:
        tmplist = i.split()
        mainmod = tmplist.pop(0)
        mainmod = mainmod.rstrip(':')
        rawmod = mainmod.rstrip('.ko')
        (a, rawmod) = ossplit(rawmod)
        newlist = []
        newlist.append((rawmod, mainmod))
        for i in tmplist:
            a = i.rstrip('.ko')
            (x, a) = ossplit(a)
            newlist.append((a, i))
        moddep[rawmod] = newlist
    moddepfile.close()
    return moddep

def generateModDep_mysplit():
    moddep = {}
    moddepfile = open(sys.argv[1], 'r')
    for i in moddepfile:
        tmplist = i.split()
        mainmod = tmplist.pop(0)
        mainmod = mainmod.rstrip(':')
        rawmod = mainmod.rstrip('.ko')
        (a, rawmod) = split(rawmod)
        newlist = []
        newlist.append((rawmod, mainmod))
        for i in tmplist:
            a = i.rstrip('.ko')
            (x, a) = split(a)
            newlist.append((a, i))
        moddep[rawmod] = newlist
    moddepfile.close()
    return moddep

def generateOutput(modlist, moddep):
    output = {}
    for i in modlist:
        try:
            for (j, k) in moddep[i]:
                output[j] = k
        except:
            continue
    return output

def calculateModuleDep():
    #modlist = modulesFromSubprocess()
    #modlist = modulesFromOwnFileinput()
    #modlist = modulesFromOwn()
    modlist = modulesFromOwn2()

    #moddep = generateModDep_basename()
    #moddep = generateModDep_split()
    #moddep = generateModDep_mysplit()
    moddep = generateModDep_mybasename()
    
    output = generateOutput(modlist, moddep)
    return output.values()

#############################################################################

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Error: you should give me the path to your modules.dep'
        sys.exit(1)

    for i in calculateModuleDep():
        print i
