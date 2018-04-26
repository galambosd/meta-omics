#!/usr/bin/env python
import ply.lex as lex
import ply.yacc as yacc

num_space = 1.0
nums_seen = 1.0
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
# Get the token map from the lexer.  This is required.

def p_expression_plus(p):
    'expression : expression PLUS expression'
    global nums_seen
    nums_seen+=1
    p[0]=(p[1]*(nums_seen-1)+p[3])/nums_seen

def p_expression_space(p):
    'expression : expression SPACE expression'
    global nums_seen
    global num_space
    nums_seen = 1.0
    p[0] = p[1]+p[3]
    num_space+=1

def p_expression_minus(p):
    'expression : expression MINUS expression'
    global nums_seen
    nums_seen = 1.0
    p[0] = p[1]

def p_expression_comma(p):
    'expression : expression COMMA expression'
    global nums_seen
    nums_seen = 1.0
    p[0] = max(p[1],p[3])


def p_expression_KOnum(p):
    'expression : KOnum'
    if p[1] in bin_set:
        p[0]=1.0
    else:
        p[0]=0.0

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    global nums_seen
    nums_seen = 1.0
    p[0] = p[2]

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

def calc_MCR(module, bin):
    # Build the parser
    parser = yacc.yacc()
    global bin_set
    global num_space
    bin_set = bin
    result = parser.parse(module)
    return result/num_space

if __name__ == "__main__":
    module = input("Module definition\n>")
    # some hardcoded set of KOs for the bin
    bin = ['K11780','K00003','K00006']
    print(calc_MCR(module, bin))
