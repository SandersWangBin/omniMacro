#!/usr/bin/env python

CODE_STYLE = {
    'C++': {'VAR_DEFINE': r'#define\s+(\w*)\s*(.*)',
            'VAR_REFER':   r'<<(\w*)>>',
            'VAR_PREFIX_NUM': 2,
            'VAR_POSTFIX_NUM': 2,
            'MULTILINE_DEFINE': r'#define\s+(\w*)\s*\(\)\s*\\',
            'MULTILINE_CONTINUE': r'(.*)\\',
            'MULTILINE_REFER_01': r'<<(\w*)\s*\(\)>>',
            'MULTILINE_PREFIX_NUM': 2,
            'MULTILINE_POSTFIX_NUM': 4}}

def loadStyle(style): return CODE_STYLE[style]