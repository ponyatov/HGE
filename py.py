import os,sys ; print sys.argv ; print

try: SRC = sys.argv[1]
except IndexError: SRC = 'src.src'

############ neo4j connector #####

import neo4j.v1 as neo4j

BOLT = 'bolt://localhost:7687'
USER = 'neo4j'
PASS = "gjyznjd"
driver = neo4j.GraphDatabase.driver(BOLT, auth=neo4j.basic_auth(USER, PASS))
print 'neo4j driver',driver
session = driver.session()
print 'neo4j session',session
print

########## core objects ##########

class Sym:
    ' symbol '
    tag = 'sym'
    def __init__(self, V,super=None):
        self.val = V
        self.merge_class(super)
        session.run('''%s MERGE (:%s {tag:"%s" , val:"%s"}) -[:isa]-> (class)'''%(
            self.match_class(),self.tag,self.tag,self.val))
    def merge_class(self, super):
        if super:
            session.run('%s MERGE (%s:class {tag:"class",val:"%s"}) -[:ako]-> (class)' % (
                self.match_class(super),self.tag, self.tag))
        else:
            session.run('MERGE (%s:class {tag:"class",val:"%s"})' % (self.tag, self.tag))
    def match_class(self, super=None):
        if super: C = super.tag
        else: C = self.tag
        return 'MATCH (class:class) WHERE class.val="%s"' % C
    def __repr__(self): return '<%s:%s>' % (self.tag, self.val)
    
class Num(Sym):
    ' number '
    tag = 'num'
    def __init__(self,V):
        self.val = float(V)
        self.merge_class(Sym)
        session.run('''%s MERGE (:%s {tag:"%s" , val:%s}) -[:isa]-> (class)'''%(
            self.match_class(),self.tag,self.tag,self.val))
    
class Str(Sym):
    tag = 'str'
    def __init__(self,V): Sym.__init__(self, V, Sym)
    
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
yacc.yacc(debug=False,write_tables=False).parse(open(SRC).read())

session.close()
driver.close()
