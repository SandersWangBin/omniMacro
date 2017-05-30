#!/usr/bin/env python

import sys, getopt
import re
from omniMacroCfg import loadStyle

STYLE_CPP = 'C++'
KEYWORD_VAR_DEFINE = 'VAR_DEFINE'
KEYWORD_VAR_REFER = 'VAR_REFER'
KEYWORD_VAR_PREFIX_NUM = 'VAR_PREFIX_NUM'
KEYWORD_MULTILINE_DEFINE = 'MULTILINE_DEFINE'
KEYWORD_MULTILINE_CONTINUE = 'MULTILINE_CONTINUE'
KEYWORD_MULTILINE_REFER_01 = 'MULTILINE_REFER_01'

def getStyle(): return loadStyle(STYLE_CPP)

def formatVar(var):
    prefixNum = getStyle()[KEYWORD_VAR_PREFIX_NUM]
    return var[prefixNum:-prefixNum]

def formatMultiName(multi):
    prefixNum = getStyle()[KEYWORD_VAR_PREFIX_NUM]
    return multi[prefixNum:-(prefixNum+2)].strip()

def formatMultiLines(multiLines, indent):
    newLine = ''
    for line in multiLines.split('\n'):
        newLine = newLine + indent + line + '\n'
    return newLine

def compileVar(line, macroDict):
    newLine = line
    reg = getStyle()[KEYWORD_VAR_REFER]
    while re.search(reg, newLine):
        s, e = [(m.start(), m.end()) for m in re.finditer(reg, newLine)][0]
        newLine = newLine[:s] + macroDict[formatVar(newLine[s:e])] + newLine[e:]
    return newLine

def compileLine(line, macroDict):
    newLine = line
    reg01 = getStyle()[KEYWORD_MULTILINE_REFER_01]
    if re.search(reg01, newLine):
        s, e = [(m.start(), m.end()) for m in re.finditer(reg01, newLine)][0]
        newLine = newLine[:s] + macroDict[formatMultiName(newLine[s:e])] + newLine[e:]
        newLine = formatMultiLines(newLine, ''*len(newLine[:s]))
    return compileVar(newLine, macroDict)

# COMPILE SOURCE FILE
def compileSource(sourceFile, macroDict):
    with open(sourceFile) as f: lines = [line.rstrip('\n') for line in f]
    for line in lines:
        print compileLine(line, macroDict)

def compileSources(sourceFiles, macroDict):
    for sourceFile in sourceFiles:
        compileSource(sourceFile, macroDict)

# READ MACRO FILES AND GENERATE THE MACRO DICTIONARY
def getVarValue(line, macroDict, multiLineFlag):
    mMltiDefine = re.match(getStyle()[KEYWORD_MULTILINE_DEFINE], line, re.M|re.I)
    if mMltiDefine:
        multiLineFlag = mMltiDefine.group(1)
        macroDict[multiLineFlag] = ''
        return macroDict, multiLineFlag

    mMultiCont = re.match(getStyle()[KEYWORD_MULTILINE_CONTINUE], line, re.M|re.I)
    if multiLineFlag != '' and mMultiCont:
        macroDict[multiLineFlag] = macroDict[multiLineFlag] + mMultiCont.group(1) + '\n'
        return macroDict, multiLineFlag

    m = re.match(getStyle()[KEYWORD_VAR_DEFINE], line, re.M|re.I)
    if m:
        macroDict[m.group(1)] = compileLine(m.group(2), macroDict)
        multiLineFlag = ''
        return macroDict, multiLineFlag
    return macroDict, multiLineFlag

def readMacro(macroFile, macroDict):
    with open(macroFile) as f: lines = [line.rstrip('\n') for line in f]
    multiLineFlag = ''
    for line in lines:
        macroDict, multiLineFlag = getVarValue(line, macroDict, multiLineFlag)
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

    for key, value in macroDict.iteritems():
        print key, ':\t', value