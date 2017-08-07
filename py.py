import os,sys ; print sys.argv ; print

########## core objects ##########

class Sym:
    ' symbol '
    tag = 'sym'
    def __init__(self, V): self.val = V
    def __repr__(self): return '<%s:%s>' % (self.tag, self.val)
    
class Num(Sym):
    ' number '
    tag = 'num'
    def __init__(self,V): Sym.__init__(self, V) ; self.val = float(V)
    
class Str(Sym):
    tag = 'str'
    
class Op(Sym):
    ' operator '
    tag = 'op'

########## parser ################

import ply.lex  as lex
import ply.yacc as yacc

tokens = ['SYM','NUM','STR']

t_ignore = ' \t\r{}[]'
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_NUM(t):
    r'[\-\+]?[0-9]+(\.[0-9]*)?([eE][\-\+]?[0-9]+)?'    
    t.value = Num(t.value) ; return t
    
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value) ; return t
    
def t_STR(t):
    r"'.*'"
    t.value = Str(t.value[1:-1]) ; return t
    
def p_REPL_none(p): ' REPL : '
def p_REPL(p):
    ' REPL : REPL ex '
    print p[2]
def p_ex_SYM(p):
    ' ex : SYM '
    p[0] = p[1]
def p_ex_NUM(p):
    ' ex : NUM '
    p[0] = p[1]
def p_ex_STR(p):
    ' ex : STR '
    p[0] = p[1]
    
def t_error(t): print 'lexer' ,t # raise BaseException('%s'%t)
def p_error(p): print 'parser',p # raise BaseException('%s'%p)

lex.lex()
yacc.yacc(debug=False,write_tables=False).parse(open(sys.argv[1]).read())
