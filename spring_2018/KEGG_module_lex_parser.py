# This script uses an external parser to calculate MCS based on the definitions
# provided by get_module_defs.py. This script is called in
# calculate_module_completion.py.

import ply.lex as lex
import ply.yacc as yacc

# the number of spaces in the definition corresponds to the number of
# total reactions in the pathway
num_space = 1.0
nums_seen = 1.0

# name the different tokens we might encounter in a KEGG module definition
tokens = (
    'KOnum',
    'PLUS',
    'MINUS',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'SPACE'
)

# define what the different tokens look like
# KOnum is K followed by 5 integers
t_KOnum = r'K\d\d\d\d\d'
t_PLUS = r'\+'
t_MINUS = r'-'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SPACE = '\ '

# define an 'order of operations' for reading the definition
precedence = (
    ('left', 'SPACE'),
    ('left', 'RPAREN', 'LPAREN'),
    ('left', 'COMMA'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'KOnum'),
)

lexer = lex.lex()

# Get the token map from the lexer.  This is required.


# See section 6 (yacc) of this documentation
# https://www.dabeaz.com/ply/ply.html for an example of how the
# code below works
def p_expression_plus(p):
    'expression : expression PLUS expression'
    global nums_seen
    nums_seen += 1
    p[0] = (p[1] * (nums_seen - 1) + p[3]) / nums_seen


def p_expression_space(p):
    'expression : expression SPACE expression'
    global nums_seen
    global num_space
    nums_seen = 1.0
    p[0] = p[1] + p[3]
    num_space += 1


def p_expression_minus(p):
    'expression : expression MINUS expression'
    global nums_seen
    nums_seen = 1.0
    p[0] = p[1]


def p_expression_comma(p):
    'expression : expression COMMA expression'
    global nums_seen
    nums_seen = 1.0
    p[0] = max(p[1], p[3])


def p_expression_KOnum(p):
    'expression : KOnum'
    if p[1] in bin_set:
        p[0] = 1.0
    else:
        p[0] = 0.0


def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    global nums_seen
    nums_seen = 1.0
    p[0] = p[2]

# Error rule for syntax errors


def p_error(p):
    print("Syntax error in input!")


def MCR(module, bin):
    # Build the parser
    parser = yacc.yacc()
    global bin_set
    global num_space
    # reset these global variables each time the function is called
    num_space = 1.0
    nums_seen = 1.0
    bin_set = bin
    result = parser.parse(module)
    result = result / num_space
    return result
