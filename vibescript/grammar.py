"""
VibeScript Language Grammar and Token Definitions

This module defines the grammar rules and token types for the VibeScript language.
"""

# Token types
TOKEN_TYPES = {
    # Keywords
    'SPILL_THE_TEA': 'spill_the_tea',  # print
    'VIBE_CHECK': 'vibe_check',        # input
    'NO_CAP': 'no_cap',                # if
    'CAP': 'cap',                      # else
    'LOWKEY': 'lowkey',                # while
    'HIGHKEY': 'highkey',              # for
    'RIZZ_UP': 'rizz_up',              # function
    'SLAY': 'slay',                    # return
    'LETS_GO': 'lets_go',              # begin block
    'YEET': 'yeet',                    # end block
    'AND_I_OOP': 'and_i_oop',          # break
    'AS_IF': 'as_if',                  # continue
    'RENT_FREE': 'rent_free',          # global
    'MAIN_CHARACTER': 'main_character', # main function
    
    # Data types
    'LIT': 'lit',                      # int
    'TEA': 'tea',                      # string
    'MOOD': 'mood',                    # boolean
    'STAN': 'stan',                    # list/array
    'THIS_SLAPS': 'this_slaps',        # true
    'IM_DEAD': 'im_dead',              # false
    'GHOST': 'ghost',                  # null/none
    
    # Operators
    'PLUS': '+',
    'MINUS': '-',
    'MULTIPLY': '*',
    'DIVIDE': '/',
    'MODULO': '%',
    'ASSIGN': '=',
    'EQUALS': '==',
    'NOT_EQUALS': '!=',
    'LESS_THAN': '<',
    'GREATER_THAN': '>',
    'LESS_EQUALS': '<=',
    'GREATER_EQUALS': '>=',
    
    # Delimiters
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACKET': '[',
    'RBRACKET': ']',
    'COMMA': ',',
    'SEMICOLON': ';',
    'COLON': ':',
    
    # Other
    'IDENTIFIER': 'IDENTIFIER',
    'INTEGER': 'INTEGER',
    'STRING': 'STRING',
    'COMMENT': 'COMMENT',
    'EOF': 'EOF',
}

# Keywords dictionary for faster lookup
KEYWORDS = {
    'spill_the_tea': TOKEN_TYPES['SPILL_THE_TEA'],
    'vibe_check': TOKEN_TYPES['VIBE_CHECK'],
    'no_cap': TOKEN_TYPES['NO_CAP'],
    'cap': TOKEN_TYPES['CAP'],
    'lowkey': TOKEN_TYPES['LOWKEY'],
    'highkey': TOKEN_TYPES['HIGHKEY'],
    'rizz_up': TOKEN_TYPES['RIZZ_UP'],
    'slay': TOKEN_TYPES['SLAY'],
    'lets_go': TOKEN_TYPES['LETS_GO'],
    'yeet': TOKEN_TYPES['YEET'],
    'and_i_oop': TOKEN_TYPES['AND_I_OOP'],
    'as_if': TOKEN_TYPES['AS_IF'],
    'rent_free': TOKEN_TYPES['RENT_FREE'],
    'main_character': TOKEN_TYPES['MAIN_CHARACTER'],
    'lit': TOKEN_TYPES['LIT'],
    'tea': TOKEN_TYPES['TEA'],
    'mood': TOKEN_TYPES['MOOD'],
    'stan': TOKEN_TYPES['STAN'],
    'this_slaps': TOKEN_TYPES['THIS_SLAPS'],
    'im_dead': TOKEN_TYPES['IM_DEAD'],
    'ghost': TOKEN_TYPES['GHOST'],
}

# Mapping of VibeScript keywords to Python keywords/functions for interpreter
KEYWORD_MAPPING = {
    TOKEN_TYPES['SPILL_THE_TEA']: 'print',
    TOKEN_TYPES['VIBE_CHECK']: 'input',
    TOKEN_TYPES['NO_CAP']: 'if',
    TOKEN_TYPES['CAP']: 'else',
    TOKEN_TYPES['LOWKEY']: 'while',
    TOKEN_TYPES['HIGHKEY']: 'for',
    TOKEN_TYPES['RIZZ_UP']: 'def',
    TOKEN_TYPES['SLAY']: 'return',
    TOKEN_TYPES['AND_I_OOP']: 'break',
    TOKEN_TYPES['AS_IF']: 'continue',
    TOKEN_TYPES['RENT_FREE']: 'global',
    TOKEN_TYPES['MAIN_CHARACTER']: 'main',
    TOKEN_TYPES['THIS_SLAPS']: 'True',
    TOKEN_TYPES['IM_DEAD']: 'False',
    TOKEN_TYPES['GHOST']: 'None',
}
