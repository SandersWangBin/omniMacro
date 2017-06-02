#!/usr/bin/env python

import sys, getopt
import re
from omniMacroCfg import *

def getStyle(): return loadStyle(STYLE_CPP)

def genArgsDict(args):
    argsDict = dict()
    for arg in args.strip().split(','):
        argsDict[arg.split('=')[0].strip()] = arg.split('=')[1].strip()
    return argsDict

def formatMultiLines(multiLines, indent):
    newLine = ''
    lineNum = 0
    for line in multiLines.split('\n'):
        lineNum = lineNum + 1
        if lineNum == 1: newLine = newLine + line + '\n'
        else: newLine = newLine + indent + line + '\n'
    return newLine

def lookupDict(var, dict1, dict2):
    return dict1[var] if dict1.get(var, None) != None else dict2[var]

def compileVar(line, macroDict, argsDict):
    newLine = line
    reg = getStyle()[KEYWORD_VAR_REFER]
    match = re.search(reg, newLine)
    while match:
        s, e = match.start(), match.end()
        newLine = newLine[:s] + lookupDict(match.group(1), argsDict, macroDict) + newLine[e:]
        match = re.search(reg, newLine)
    return newLine

def compileLine(line, macroDict):
    newLine = line
    argsDict = dict()
    match01 = re.search(getStyle()[KEYWORD_MULTILINE_REFER_01], newLine)
    if match01:
        s, e = match01.start(), match01.end()
        newLine = newLine[:s] + macroDict[match01.group(1)] + newLine[e:]
        newLine = formatMultiLines(newLine, ' '*len(newLine[:s]))
    else:
        match02 = re.search(getStyle()[KEYWORD_MULTILINE_REFER_02], newLine)
        if match02:
            s, e = match02.start(), match02.end()
            func, argsDict = match02.group(1), genArgsDict(match02.group(2))
            newLine = newLine[:s] + macroDict[func] + newLine[e:]
            newLine = formatMultiLines(newLine, ' '*len(newLine[:s]))
    return compileVar(newLine, macroDict, argsDict)

# COMPILE SOURCE FILE
def compileSource(sourceFile, outputFile, macroDict):
    with open(sourceFile) as f: lines = [line.rstrip('\n') for line in f]
    fOutput = open(outputFile, 'w')
    for line in lines:
        fOutput.write(compileLine(line, macroDict) + '\n')
    fOutput.close()

def compileSources(sourceFiles, outputFiles, macroDict):
    index = 0
    for sourceFile in sourceFiles:
        compileSource(sourceFile, outputFiles[index], macroDict)
        index = index + 1

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
    optionsLong = ['help', 'macro', 'source', 'output']
    optionsShort = 'hm:s:o:'
    try:
        opts, args = getopt.getopt(sys.argv[1:], optionsShort, optionsLong)
    except getopt.GetoptError:
        showHelp()

    if len(opts) <= 0:
        showHelp()

    macroFiles = None
    sourceFiles = None
    outputFiles = None
    for o, a in opts:
        if o in ('-h', '--help'): showHelp()
        if o in ('-m', '--macro'): macroFiles = a.split(',')
        if o in ('-s', '--souce'): sourceFiles = a.split(',')
        if o in ('-o', '--output'): outputFiles = a.split(',')

    return macroFiles, sourceFiles, outputFiles

def showHelp():
    helpMsg = 'Designed by Sanders Bin Wang\n'\
        'Usage: omniMacro [OPTION]...\n\n'\
        '    -h, --help        Show this help\n'\
        '    -m, --macro       Provide the macro files seperated by , \n'\
        '    -s, --source      Provide the source files seperated by , \n'\
        '    -o, --output      Provide the output files seperated by , \n\n'
    sys.stdout.write(helpMsg)
    sys.exit(3)

# MAIN ENTRY
if(__name__ == '__main__'):
    macroDict = dict()
    macroFiles, sourceFiles, outputFiles = parserOptions()
    macroDict = readMacros(macroFiles, macroDict)

    compileSources(sourceFiles, outputFiles, macroDict)