#!/usr/bin/env python

STYLE_CPP = 'C++'
KEYWORD_VAR_DEFINE = 'VAR_DEFINE'
KEYWORD_VAR_REFER = 'VAR_REFER'
KEYWORD_MULTILINE_DEFINE = 'MULTILINE_DEFINE'
KEYWORD_MULTILINE_CONTINUE = 'MULTILINE_CONTINUE'
KEYWORD_MULTILINE_REFER_01 = 'MULTILINE_REFER_01'
KEYWORD_MULTILINE_REFER_02 = 'MULTILINE_REFER_02'

CODE_STYLE = {
    STYLE_CPP: {KEYWORD_VAR_DEFINE:         r'#define\s+(\w*)\s*(.*)',
                KEYWORD_VAR_REFER:          r'<<(\w*)>>',
                KEYWORD_MULTILINE_DEFINE:   r'#define\s+(\w*)\s*\(\)\s*\\',
                KEYWORD_MULTILINE_CONTINUE: r'(.*)\\',
                KEYWORD_MULTILINE_REFER_01: r'<<(\w*)\s*\(\)>>',
                KEYWORD_MULTILINE_REFER_02: r'<<(\w*)\s*\((.*)\)>>'}}

def loadStyle(style): return CODE_STYLE[style]