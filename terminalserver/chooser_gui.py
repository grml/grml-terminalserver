#!/usr/bin/python2.4

import os
import sys
import snack
import types

class ChooserGui(object):
    def __init__(self, screen):
        #self.m_screen = screen
        helptext = """This dialog shows all installed plugins for the grml-terminalserver.
Just activate them as needed and proceed with <Run>!"""
        self.m_grid = snack.GridForm(screen, 'Grmlterminalserver Config', 1, 8)

        self.m_text = snack.TextboxReflowed(40, helptext)
        self.m_grid.add(self.m_text, 0, 0, (0, 0, 0, 1))

        self.m_plugins = snack.CheckboxTree(15)
        self.m_grid.add(self.m_plugins, 0, 2, (0, 0, 0, 1), growx=1)

        self.m_bb = snack.ButtonBar(screen, ((' Run ', 'run'), ('Quit', 'quit')))
        self.m_grid.add(self.m_bb, 0, 4)

    def run(self):
        result = self.m_grid.runOnce()
        if(type(result) == types.StringType and result == 'F12'):
            return 'run'
        else:
            return self.m_bb.buttonPressed(result)

    def getPlugins(self):
        return self.m_plugins.getSelection()

    def addPlugin(self, name, pluginid):
        self.m_plugins.append(name, pluginid)

def run(dir):
    dir = os.path.expanduser(dir.rstrip('\n'))
    try:
        files = os.listdir(dir)
    except OSError:
        print 'Error: no such file or directory, using current directory'
        files = os.listdir('.')
    dir = os.path.abspath(dir)
    files = [ f for f in files if os.path.isfile(os.path.join(dir, f)) ]

    screen = snack.SnackScreen()
    gui = ChooserGui(screen)
    for i in files:
        gui.addPlugin(i, i)
    result = gui.run()
    screen.finish()
    print 'ret =', result, 'selections =', gui.getPlugins()
    return result

if __name__ == '__main__':
    result = 'ok'
    while result != 'quit':
        print 'please input a directory: '
        dir = sys.stdin.readline()
        result = run(dir)
    print 'Bye!'
