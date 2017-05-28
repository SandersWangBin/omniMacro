#!/usr/bin/env python

import sys, getopt
import re
from omniMacroCfg import loadStyle
STYLE_CPP = 'C++'

def getVarValue(line, macroDict):
    codeStyle = loadStyle(STYLE_CPP)
    m = re.match(codeStyle['MACRO_DEFINE'], line, re.M|re.I)
    if m: macroDict[m.group(1)] = m.group(2)
    return macroDict

def readMacro(macroFile, macroDict):
    with open(macroFile) as f: lines = [line.rstrip('\n') for line in f]
    for line in lines:
        macroDict = getVarValue(line, macroDict)
    return macroDict

def readMacros(macroFiles, macroDict):
    for macroFile in macroFiles:
        macroDict = readMacro(macroFile, macroDict)
    return macroDict



def parserOptions():
    optionsLong = ['help', 'macro', 'source']
    optionsShort = 'hm:s:'
    try:
        opts, args = getopt.getopt(sys.argv[1:], optionsShort, optionsLong)
    except getopt.GetoptError:
        showHelp()

    if len(args):
        sys.stderr.write("Extraneous arguments: %s\n" % args)
        sys.exit(3)

    macroFiles = list()
    sourceFiles = list()
    for o, a in opts:
        if o in ('-h', '--help'): showHelp()
        if o in ('-m', '--macro'): macroFiles = a.split(',')
        if o in ('-s', '--souce'): soueceFiles = a.split(',')

    return macroFiles, sourceFiles

def showHelp():
    helpMsg = 'Designed by Sanders Bin Wang\n'\
        'Usage: omniMacro [OPTION]...\n\n'\
        '    -h, --help        Show this help\n'\
        '    -m, --macro       Provide the macro files seperated by , \n'\
        '    -s, --source      Provide the source files seperated by , \n\n'
    sys.stdout.write(helpMsg)
    sys.exit(3)

if(__name__ == '__main__'):
    macroDict = dict()
    macroFiles, sourceFiles = parserOptions()
    macroDict = readMacros(macroFiles, macroDict)

    for key, value in macroDict.iteritems():
        print key, ': ', value, ' (', str(len(value)), ')'