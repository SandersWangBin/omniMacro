#!/usr/bin/env python

CODE_STYLE = {
    'C++': {'MACRO_DEFINE': r'#define\s+(\w*)\s*(.*)',
            'VAR_REFER':   r'$$$(\w*)$$$'}}

def loadStyle(style): return CODE_STYLE[style]