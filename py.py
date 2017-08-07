import os,sys ; print sys.argv ; print

########## core objects ##########

class Sym:
    tag = 'sym'
    def __init__(self, V): self.val = V
    def __repr__(self): return '<%s:%s>' % (self.tag, self.val)

########## parser ################

import ply.lex  as lex
import ply.yacc as yacc

tokens = ['SYM']

t_ignore = ' \t\r'
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value) ; return t
    
def p_REPL_none(p): ' REPL : '
def p_REPL(p):
    ' REPL : REPL SYM '
    print p[2]
    
def t_error(t): print 'lexer' ,t # raise BaseException('%s'%t)
def p_error(t): print 'parser',p # raise BaseException('%s'%p)

lex.lex()
yacc.yacc(debug=False,write_tables=False).parse(open('src.src').read())
