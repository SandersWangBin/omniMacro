#!/usr/bin/env python

import sys, getopt
import re
from omniMacroCfg import loadStyle

STYLE_CPP = 'C++'
KEYWORD_MACRO_DEFINE = 'MACRO_DEFINE'
KEYWORD_VAR_REFER = 'VAR_REFER'
KEYWORD_VAR_PREFIX_NUM = 'VAR_PREFIX_NUM'

def getStyle(): return loadStyle(STYLE_CPP)

def formatVar(var):
    prefixNum = getStyle()[KEYWORD_VAR_PREFIX_NUM]
    return var[prefixNum:-prefixNum]

def compileLine(line, macroDict):
    newLine = line
    reg = getStyle()[KEYWORD_VAR_REFER]
    while re.search(reg, newLine):
        s, e = [(m.start(), m.end()) for m in re.finditer(reg, newLine)][0]
        newLine = newLine[:s] + macroDict[formatVar(newLine[s:e])] + newLine[e:]
    return newLine

# COMPILE SOURCE FILE
def compileSource(sourceFile, macroDict):
    with open(sourceFile) as f: lines = [line.rstrip('\n') for line in f]
    for line in lines:
        print compileLine(line, macroDict)

def compileSources(sourceFiles, macroDict):
    for sourceFile in sourceFiles:
        compileSource(sourceFile, macroDict)

# READ MACRO FILES AND GENERATE THE MACRO DICTIONARY
def getVarValue(line, macroDict):
    m = re.match(getStyle()[KEYWORD_MACRO_DEFINE], line, re.M|re.I)
    if m: macroDict[m.group(1)] = compileLine(m.group(2), macroDict)
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

# PARSER ARGUMENTS
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

    macroFiles = None
    sourceFiles = None
    for o, a in opts:
        if o in ('-h', '--help'): showHelp()
        if o in ('-m', '--macro'): macroFiles = a.split(',')
        if o in ('-s', '--souce'): sourceFiles = a.split(',')

    return macroFiles, sourceFiles

def showHelp():
    helpMsg = 'Designed by Sanders Bin Wang\n'\
        'Usage: omniMacro [OPTION]...\n\n'\
        '    -h, --help        Show this help\n'\
        '    -m, --macro       Provide the macro files seperated by , \n'\
        '    -s, --source      Provide the source files seperated by , \n\n'
    sys.stdout.write(helpMsg)
    sys.exit(3)

# MAIN ENTRY
if(__name__ == '__main__'):
    macroDict = dict()
    macroFiles, sourceFiles = parserOptions()
    macroDict = readMacros(macroFiles, macroDict)

    compileSources(sourceFiles, macroDict)