'''
MiaLang Rules:
start--> `<mia>` <stmt> 
<stmt> --> <while_stmt>|<if_stmt>|<block>|<varOp>
<block> --> `{` <stmt> `;` `}`
<while_stmt> --> `whilst` <boolexpr> <block> [ `elsey` <block> ]
<if_stmt> --> `iffy` <boolexpr> <block>
<varOp> --> `id` (<declare>|<assign>)
<declare> --> `intOne`|`intTwo`|`intThree`|`intFour`
<assign> --> `=` <expr>
<expr> --> <term> {(`*`|`/`|`%`) <term>}
<term> --> <factor> {(`+`|`-`) <factor>}
<factor> --> `id`|`int_lit`|`(` <expr> `)`
<boolexpr> --> <boo>{`and` <boo>}
<boo> --> <equalityOp> {`or` <equalityOp>}
<equalityOp> --> <relationOp> {(`!=`|`==`) <relationOp>}
<relationOp> --> <booExpr> {(`<=`|`>=`|`<`|`<`) <booExpr>}
<booExpr> --> <booTerm> {(`*`|`/`|`%`) <booTerm>}
<booTerm> --> <booFactor> {(`+`|`-`) <booFactor>}
<booFactor>--> `id`|`int_lit`|`bool_lit`
'''
import re

class RDA:
  def __init__(self, tokens) :
    self.tokens = tokens
    self.current = 0
    self.currentToken = tokens[self.current]

  def getNextToken(self):
    if self.current < len(self.tokens):
      self.current += 1
    self.currentToken = self.tokens[self.current]

  def stmt(self):
    #<stmt> --> <while_stmt>|<if_stmt>|<block>|<varOp>
    match self.currentToken:
      case 'whilst':
        self.while_stmt()
      case 'iffy':
        self.if_stmt()
      case 'id':
        self.varOp()
      case '{':
        self.block()
      case _:
        self.error()
    
  def start(self):
    if self.currentToken == 'start':
      self.getNextToken()
      self.stmt()
    else:
      self.error()

  def block(self):
    #<block> --> `{` <stmt> `;` `}`
    if self.currentToken == '{':
      self.getNextToken()
      while self.currentToken == 'whilst' or self.currentToken == 'iffy' or self.currentToken == 'id' or self.currentToken == '{':
        self.stmt()
        if self.currentToken == ';':
          self.getNextToken()
          self.stmt()
        else:
          self.error()
      if self.currentToken == '}':
        self.getNextToken()
      else:
        self.error()
    else:
      self.error()
    

  def if_stmt(self):
    #<if_stmt> --> `iffy` <boolexpr> <block>
    if self.currentToken == 'iffy':
      self.getNextToken()
      if self.currentToken == '(':
        self.getNextToken()
        self.boolexpr()
        if self.currentToken == ')':
          self.getNextToken()
          self.block()
        else:
          self.error()
      elif self.currentToken == 'int_lit':
        self.getNextToken()
        self.block()
      else:
        self.error()
      pass
    else:
      self.error()
    
  def while_stmt(self):
    #<while_stmt> --> `whilst` `(` <boolexpr> `)` <block>
    if self.currentToken == 'whilst':
      self.getNextToken()
      if self.currentToken == '(':
        self.getNextToken()
        self.boolexpr()
        if self.currentToken == ')':
          self.getNextToken()
          self.block()
          if self.currentToken == 'elsey':
            self.getNextToken()
            self.block()
        else:
          self.error()
      else:
        self.error()
    else:
      self.error()
  '''
  <boolexpr> --> <boo>{`and` <boo>}
  <boo> --> <equalityOp> {`OR` <equalityOp>}
  <equalityOp> --> <relationOp> {(`!=`|`==`) <relationOp>}
  <relationOp> --> <booExpr> {(`<=`|`>=`|`<`|`<`) <booExpr>}
  <booExpr> --> <booTerm> {(`*`|`/`|`%`) <booTerm>}
  <booTerm> --> <negateOp> {(`+`|`-`) <negateOp>}
  <negateOp> --> `!`<booFactor>
  <booFactor>--> `id`|`int_lit`|`bool_lit`
  ''' 
  def boolexpr(self):
    #<boolexpr> --> <boo>{`and` <boo>}
    self.boo()
    while self.currentToken == '&&':
      self.getNextToken()
      self.boo()
  def boo(self):
    #<boo> --> <equalityOp> {`OR` <equalityOp>}
    self.equalityOp()
    while self.currentToken == '||':
      self.getNextToken()
      self.equalityOp()
  def equalityOp(self):
    #<equalityOp> --> <relationOp> {(`!=`|`==`) <relationOp>}
    self.relationOp()
    while self.currentToken == '!=' or self.currentToken == '==':
      self.getNextToken()
      self.relationOp()
  def relationOp(self):
    #<relationOp> --> <booExpr> {(`<=`|`>=`|`<`|`<`) <booExpr>}
    self.booExpr()
    while self.currentToken == '<=' or self.currentToken == '>=' or self.currentToken == '>' or self.currentToken == '<':
      self.getNextToken()
      self.booExpr()
  def booExpr(self):
    #<booExpr> --> <booTerm> {(`*`|`/`|`%`) <booTerm>}
    self.booTerm()
    while self.currentToken == '*' or self.currentToken == '/' or self.currentToken == '%':
      self.getNextToken()
      self.booTerm()
  def booTerm(self):
    #<booTerm> --> <negateOp> {(`+`|`-`) <negateOp>}
    self.booFactor()
    while self.currentToken == '+' or self.currentToken == '-' :
      self.getNextToken()
      self.booFactor()
  def booFactor(self):
    #<booFactor>--> `id`|`int_lit`|`bool_lit`
    if self.currentToken == 'id' or self.currentToken == 'int_lit':
      self.getNextToken()
    elif self.currentToken == '(':
      self.getNextToken()
      self.booExpr()
      if self.currentToken == ')':
        self.getNextToken()
      else:
        self.error()
    else:
      self.error()
    
  '''
 <varOp> --> `id` (<declare>|<assign>)
 <declare> --> `intOne`|`intTwo`|`intThree`|`intFour`
 <assign> --> `=` <expr>
 <expr> --> <term> {(`*`|`/`|`%`) <term>}
 <term> --> <factor> {(`+`|`-`) <factor>}
 <factor> --> `id`|`int_lit`|`(` <expr> `)`
  '''
  def varOp(self):
    #<varOp> --> `id` (<declare>|<assign>)
    if self.currentToken == 'id':
      self.getNextToken()
      # <declare> --> `intOne`|`intTwo`|`intThree`|`intFour`
      if self.currentToken == 'intOne'or self.currentToken =='intTwo'or self.currentToken =='intThree'or self.currentToken =='intFour':
        self.getNextToken()
        #<assign> --> `=` <expr>
      elif self.currentToken == '=':
        self.getNextToken()
        self.expr()
      else:
        self.error()
  
  def expr(self):
    #<expr> --> <term> {(`*`|`/`|`%`) <term>}
    self.term()
    while self.currentToken == '*' or self.currentToken == '/'or self.currentToken == '%':
      self.getNextToken()
      self.term()

  def term(self):
    #<term> --> <factor> {(`+`|`-`) <factor>}
    self.factor()
    #<factor> --> `id`|`int_lit`|`(` <expr> `)`
    while self.currentToken == '+' or self.currentToken == '-' :
      self.getNextToken()
      self.factor()

  def error(self):
    print("syntax error")
    StopIteration

  def factor(self):
    #<factor> --> 'id' | 'int_lit' | '('<expr>')'
    if self.currentToken == 'id' or self.currentToken == 'int_lit':
      self.getNextToken()
    elif self.currentToken == '(':
      self.getNextToken()
      self.expr()
      if self.currentToken == ')':
        self.getNextToken()
      else:
        self.error()
    else:
      self.error()

def isVariable(string):
  return re.search("[a-zA-Z]{6,8}|_", string)

class Lexer:
  def __init__(self, string):
    self.string = string
  def error(self):
    print("Error!")
    exit()
  def checkLex(self):
    tokenList = []
    for lex in self.string:
      if lex == "<mia>":
        tokenList.append('start')
      elif lex == "</mia>":
        tokenList.append('END')
      elif lex == "iffy":
        tokenList.append('iffy')
      elif lex == "elsey":
        tokenList.append('elsey')
      elif lex == "whilst":
        tokenList.append('whilst')
      elif lex == "intOne":
        tokenList.append('intOne')
      elif lex == "intTwo":
        tokenList.append('intTwo')
      elif lex == "intThree":
        tokenList.append('intThree')
      elif lex == "intFour":
        tokenList.append('intFour')
      elif lex == "+":
        tokenList.append('+')
      elif lex == "-":
        tokenList.append('-')
      elif lex == "*":
        tokenList.append('*')
      elif lex == "/":
        tokenList.append('/')
      elif lex == "%":
        tokenList.append('%')
      elif lex == ">":
        tokenList.append('>')
      elif lex == ">=":
        tokenList.append('>=')
      elif lex == "<":
        tokenList.append('<')
      elif lex == "<=":
        tokenList.append('<=')
      elif lex == "==":
        tokenList.append('==')
      elif lex == "!=":
        tokenList.append('!=')
      elif lex == "{":
        tokenList.append('{')
      elif lex == "}":
        tokenList.append('}')
      elif lex == "(":
        tokenList.append('(')
      elif lex == ")":
        tokenList.append(')')
      elif lex == "=":
        tokenList.append('=')
      elif lex == ";":
        tokenList.append(';')
      elif lex == "&&":
        tokenList.append('&&')
      elif lex == "||":
        tokenList.append('||')
      elif lex.isnumeric():
        tokenList.append('int_lit')
      elif isVariable(lex):
        tokenList.append('id')
      else:
        print(lex)
        self.error()
        
    return tokenList


#Enter name of test file to test
testFile = open("test1.txt", "rt")
data = testFile.read()
lexemes = data.split()
tokenString = Lexer(lexemes)
token = tokenString.checkLex()
print(token)
test = RDA(token)
test.start()
