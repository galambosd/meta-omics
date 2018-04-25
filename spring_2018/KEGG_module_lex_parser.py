#!/usr/bin/env python
import ply.lex as lex
import ply.yacc as yacc


tokens = (
    'KOnum',
    'PLUS',
    'MINUS',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'SPACE'
)

t_KOnum = r'K\d\d\d\d\d'
t_PLUS = r'\+'
t_MINUS = r'-'
t_COMMA=r','
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_SPACE='\ '

lexer=lex.lex()

data = '(K00001,K00009) (K00002+K00003+K00004,K00005) (K00006-K00007,K00008)'
bin_set = ['K00001','K00004','K00008']
lexer.input(data)

for tok in lexer:
    print(tok)


# Get the token map from the lexer.  This is required.

def p_expression_plus(p):
    'expression : expression PLUS expression'
    p[0] = (p[1]+p[3])/2
    print('1',p[0])

def p_expression_space(p):
    'expression : expression SPACE expression'
    p[0] = (p[1]+p[3])/2
    print('2',p[0])


def p_expression_minus(p):
    'expression : expression MINUS expression'
    p[0] = p[1]
    print('3',p[0])


def p_expression_comma(p):
    'expression : expression COMMA expression'
    p[0] = max(p[1],p[3])
    print('4',p[0])


def p_expression_KOnum(p):
    'expression : KOnum'
    if p[1] in bin_set:
        p[0]=1.0
    else:
        p[0]=0.0
    print('5',p[0])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]
    print('6',p[0])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

precedence = (
  ('left', 'SPACE'),
  ('left', 'RPAREN', 'LPAREN'),
  ('left', 'COMMA'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'KOnum'),
)

# Build the parser
parser = yacc.yacc()

result = parser.parse(data, debug=True)
print(result)
