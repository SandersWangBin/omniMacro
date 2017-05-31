#!/usr/bin/env python

import sys, getopt
import re
from omniMacroCfg import loadStyle

STYLE_CPP = 'C++'
KEYWORD_VAR_DEFINE = 'VAR_DEFINE'
KEYWORD_VAR_REFER = 'VAR_REFER'
KEYWORD_VAR_PREFIX_NUM = 'VAR_PREFIX_NUM'
KEYWORD_VAR_POSTFIX_NUM = 'VAR_POSTFIX_NUM'
KEYWORD_MULTILINE_DEFINE = 'MULTILINE_DEFINE'
KEYWORD_MULTILINE_CONTINUE = 'MULTILINE_CONTINUE'
KEYWORD_MULTILINE_REFER_01 = 'MULTILINE_REFER_01'
KEYWORD_MULTILINE_PREFIX_NUM = 'MULTILINE_PREFIX_NUM'
KEYWORD_MULTILINE_POSTFIX_NUM = 'MULTILINE_POSTFIX_NUM'

def getStyle(): return loadStyle(STYLE_CPP)

def formatVar(var):
    prefixNum = getStyle()[KEYWORD_VAR_PREFIX_NUM]
    postfixNum = getStyle()[KEYWORD_VAR_POSTFIX_NUM]
    return var[prefixNum:-postfixNum]

def formatMultiName(multi):
    prefixNum = getStyle()[KEYWORD_MULTILINE_PREFIX_NUM]
    postfixNum = getStyle()[KEYWORD_MULTILINE_POSTFIX_NUM]
    return multi[prefixNum:-postfixNum].strip()

def formatMultiLines(multiLines, indent):
    newLine = ''
    lineNum = 0
    for line in multiLines.split('\n'):
        lineNum = lineNum + 1
        if lineNum == 1: newLine = newLine + line + '\n'
        else: newLine = newLine + indent + line + '\n'
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
        newLine = formatMultiLines(newLine, ' '*len(newLine[:s]))
    return compileVar(newLine, macroDict)

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

    if len(args):
        sys.stderr.write("Extraneous arguments: %s\n" % args)
        sys.exit(3)

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