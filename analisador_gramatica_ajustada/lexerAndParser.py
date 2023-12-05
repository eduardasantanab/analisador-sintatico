import lex, yacc

#Dupla: Maria Eduarda Santana e Gustavo Pereira 
# ANALISADOR LÉXICO 

# Definição palavras reservadas
reserved = {
   'int' : 'INT',
   'double' : 'DOUBLE',
   'switch' : 'SWITCH',
   'char' : 'CHAR',
   'boolean' : 'BOOLEAN',
   'float' : 'FLOAT',
   'char' : 'CHAR',
   'boolean' : 'BOOLEAN',
   'void' : 'VOID',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'scanf' : 'SCANF',
   'println' : 'PRINTLN',
   'main' : 'MAIN',
   'return' : 'RETURN',
   'default' : 'DEFAULT',
   'case' : 'CASE',
   'for' : 'FOR',
   'break' : 'BREAK',
   'continue' : 'CONTINUE',
   'struct' : 'STRUCT',
}

# Definição de tokens
tokens = ['ID',
          'NUMBER',
          'TEXTO',
          'COMMA',
          'NUM_DEC',
          'MINUS',
          'PLUS',
          'DIV',
          'MULT',
          'LPAREN',
          'RPAREN',
          'SEMICOLON',
          'EQUALS',
          'LBRACE',
          'RBRACE',
          'RBRACKET',
          'LBRACKET',
          'DOT',
          'COMMENTS',
          'COLON',
          'AND',
          'OR',
          'MOD',
          'NOT',
          'INCREMENT',
          'DECREMENT',
          'MAIOR_QUE',
          'MENOR_QUE',
          'MA_IGUAL',
          'ME_IGUAL',
          'DIF_DE',
          'COMPARA',
          'ARROW',] + list(reserved.values())

# Regras para tokens simples
t_NUM_DEC = r'\d+\.\d+'
t_MAIOR_QUE = r'\>'
t_MENOR_QUE = r'\<'
t_MA_IGUAL = r'\>\='
t_ME_IGUAL = r'\<\='
t_DIF_DE = r'\!\='
t_COMPARA = r'\=\='
t_COMMA = r'\,'
t_TEXTO = r'".*"'
t_MINUS = r'-'
t_PLUS = r'\+'
t_MULT = r'\*'
t_DIV = r'\/(?!\/)'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_DOT = r'\.'
t_COMMENTS = r'//.*'
t_COLON = r':'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_MOD = r'\%'
t_NOT = r'\!'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'
t_ARROW = r'\-\>'


# Regra para token NUMBER
def t_NUMBER(t):
 r'\d+'
 t.value = int(t.value)
 return t

# Ignora espaços em branco e tabulações
t_ignore = ' \t'

# Regra para token ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # Converte para minúsculas antes de verificar as palavras reservadas
    return t

#Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regras para erros
def t_error(t):
 print(f"Caractere inesperado: {t.value[0]}")
 t.lexer.skip(1)


code = '''
//testa comentário no código
int contador;
double x;
array[]

struct x{int cont = 0;};
return contador = x;
'''
# Contrução do analisador léxico
lexer = lex.lex()
lexer.input(code)

#for token in lexer:
    #print(token)

##############################################################################################################

# ANALISADROR SINTÁTICO


# Adiciona informações de precedência
precedence = (
    ('right', 'EQUALS'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'MAIOR_QUE', 'MENOR_QUE', 'MA_IGUAL', 'ME_IGUAL', 'DIF_DE', 'COMPARA'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('left', 'INCREMENT', 'DECREMENT'),
    ('left', 'ARROW'),
)

def p_program(p):
    'Programa : ListaDeclaracoes'
    p[0] = {'declaracoes': p[1]}
    

def p_lista_declaracoes(p):
    '''
    ListaDeclaracoes : Declaracao
                    | ListaDeclaracoes Declaracao
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracao(p):
    '''
    Declaracao : DeclaracaoVariavel
               | DeclaracaoFuncao
               | Comentario
               | Array
               | DeclaracaoEstrutura
               | EstruturaControle
    '''
    p[0] = p[1]

def p_array(p):
    '''
    Array : ID LBRACKET Expression RBRACKET
          | ID LBRACKET RBRACKET
    '''
    if len(p) == 5:
        # Array com tamanho especificado
        p[0] = {'id': p[1], 'tamanho': p[3]}
    else:
        # Array sem tamanho especificado
        p[0] = {'id': p[1], 'tamanho': None}


def p_ArrayInicializacao(p):
    'ArrayInicializacao : LBRACE ExpressaoLista RBRACE'
    p[0] = {'expressions': p[2]}

def p_ExpressaoLista(p):
    'ExpressaoLista : '

def p_ExpressaoLogica(p):
    '''
    ExpressaoLogica : ExpressaoRelacional
                   | ExpressaoLogica AND ExpressaoRelacional
                   | ExpressaoLogica OR ExpressaoRelacional
                   | NOT ExpressaoRelacional
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2].lower() == 'and':
        p[0] = {'op': 'and', 'left': p[1], 'right': p[3]}
    elif p[2].lower() == 'or':
        p[0] = {'op': 'or', 'left': p[1], 'right': p[3]}
    elif p[1].lower() == 'not':
        p[0] = {'op': 'not', 'expr': p[2]}

def p_ExpressaoRelacional(p):
    '''
    ExpressaoRelacional : ExpressaoAritmetica
                       | ExpressaoAritmetica MAIOR_QUE ExpressaoAritmetica
                       | ExpressaoAritmetica MA_IGUAL ExpressaoAritmetica
                       | ExpressaoAritmetica MENOR_QUE ExpressaoAritmetica
                       | ExpressaoAritmetica ME_IGUAL ExpressaoAritmetica
                       | ExpressaoAritmetica DIF_DE ExpressaoAritmetica
                       | ExpressaoAritmetica COMPARA ExpressaoAritmetica
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}


def p_ExpressaoAritmetica(p):
    '''
    ExpressaoAritmetica : ExpressaoMultiplicativa
                       | ExpressaoAritmetica PLUS ExpressaoMultiplicativa
                       | ExpressaoAritmetica MINUS ExpressaoMultiplicativa
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}


def p_ExpressaoMultiplicativa(p):
    '''
    ExpressaoMultiplicativa : ExpressaoUnaria
                          | ExpressaoMultiplicativa MULT ExpressaoUnaria
                          | ExpressaoMultiplicativa DIV ExpressaoUnaria
                          | ExpressaoMultiplicativa MOD ExpressaoUnaria
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}


def p_ExpressaoUnaria(p):
    '''
    ExpressaoUnaria : ExpressaoPostfix
                   | MINUS ExpressaoUnaria
                   | PLUS ExpressaoUnaria
                   | INCREMENT ExpressaoPostfix
                   | DECREMENT ExpressaoPostfix
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = {'op': p[1], 'operand': p[2]}


def p_ExpressaoPostfix(p):
    '''
    ExpressaoPostfix : Primaria
                    | Primaria LBRACKET Expression RBRACKET
                    | Primaria LPAREN Argumentos RPAREN
                    | Primaria DOT ID
                    | Primaria ARROW ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        if p[2] == '[':
            p[0] = {'op': 'INDEX', 'array': p[1], 'index': p[3]}
        elif p[2] == '(':
            p[0] = {'op': 'CALL', 'function': p[1], 'arguments': p[3]}
    elif len(p) == 4:
        if p[2] == '.':
            p[0] = {'op': 'MEMBER', 'struct': p[1], 'member': p[3]}
        elif p[2] == '->':
            p[0] = {'op': 'PTR_MEMBER', 'struct_ptr': p[1], 'member': p[3]}


def p_argumentos(p):
    '''
    Argumentos :  ExpressaoLista 
               |
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None  


def p_primaria(p):
    '''
    Primaria : ID
             | NUMBER
             | NUM_DEC
             | TEXTO
             | LPAREN Expression RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]


def p_declaracao_estrutura(p):
    'DeclaracaoEstrutura : STRUCT ID LBRACE DeclaracaoVariavel RBRACE SEMICOLON'
    p[0] = {'type': 'struct', 'name': p[2], 'declaracao_variavel': p[4]}


def p_atribuicao(p):
    '''
    Atribuicao : ID EQUALS Expression
               | ID PLUS EQUALS Expression
               | ID MINUS EQUALS Expression
               | ID MULT EQUALS Expression
               | ID DIV EQUALS Expression
               | ID MOD EQUALS Expression
               | ID AND AND EQUALS Expression
               | ID OR OR EQUALS Expression
               | ID EQUALS ID
               | ID PLUS EQUALS ID
               | ID MINUS EQUALS ID
               | ID MULT EQUALS ID
               | ID DIV EQUALS ID
               | ID MOD EQUALS ID
               | ID AND AND EQUALS ID
               | ID OR OR EQUALS ID
    '''
    if len(p) == 4:
        p[0] = {'type': 'atribuicao', 'left': p[1], 'operator': p[2], 'right': p[3]}
    else:
        p[0] = {'type': 'atribuicao', 'left': p[1], 'operator': p[2], 'right': p[4]}


def p_estrutura_controle(p):
    '''
    EstruturaControle : IF LPAREN Expression RPAREN Bloco
                     | IF LPAREN Expression RPAREN Bloco ELSE Bloco
                     | WHILE LPAREN Expression RPAREN Bloco
                     | FOR LPAREN Expression SEMICOLON Expression SEMICOLON Expression RPAREN Bloco
                     | SWITCH LPAREN Expression RPAREN CaseLista
                     | BREAK SEMICOLON
                     | CONTINUE SEMICOLON
                     | RETURN Expression SEMICOLON
    '''
    if p[1] == 'if':
        if len(p) == 6:
            p[0] = {'type': 'if', 'condition': p[3], 'body': p[5]}
        else:
            p[0] = {'type': 'if-else', 'condition': p[3], 'if_body': p[5], 'else_body': p[7]}
    elif p[1] == 'while':
        p[0] = {'type': 'while', 'condition': p[3], 'body': p[5]}
    elif p[1] == 'for':
        p[0] = {'type': 'for', 'init': p[3], 'condition': p[5], 'update': p[7], 'body': p[9]}
    elif p[1] == 'switch':
        p[0] = {'type': 'switch', 'expression': p[3], 'cases': p[5]}
    elif p[1] == 'break':
        p[0] = {'type': 'break'}
    elif p[1] == 'continue':
        p[0] = {'type': 'continue'}
    elif p[1] == 'return':
        p[0] = {'type': 'return', 'expression': p[2]}


def p_case_lista(p):
    '''
    CaseLista : CaseDecl
              | CaseDecl CaseLista
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_case_decl(p):
    '''
    CaseDecl : CASE Expression COLON Bloco
             | DEFAULT COLON Bloco
    '''
    if p[1] == 'case':
        p[0] = ('case', p[2], p[4])
    else:
        p[0] = ('default', p[3])



def p_DeclaracaoVariavel(p):
    '''
    DeclaracaoVariavel : Tipo ID SEMICOLON
                     | Tipo ID EQUALS Expression SEMICOLON
    '''
    if len(p) == 4:
        # A declaração sem uma expressão (Tipo ID SEMICOLON)
        p[0] = {'tipo': p[1], 'id': p[2]}
    else:
        # A declaração com uma expressão (Tipo ID EQUALS expression SEMICOLON)
        p[0] = {'tipo': p[1], 'id': p[2], 'expressao': p[4]}


def p_tipo(p):
    '''
    Tipo : INT
         | FLOAT
         | DOUBLE
         | CHAR
         | BOOLEAN
    '''
    p[0] = p[1]

def p_declaracao_funcao(p):
    'DeclaracaoFuncao : Tipo ID LPAREN Parametros RPAREN Bloco'
    p[0] = {'tipo': p[1], 'nome': p[2], 'parametros': p[4], 'bloco': p[6]}


def p_parametros(p):
    '''
    Parametros : Parametro
               | Parametros COMMA Parametro
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_parametro(p):
    '''
    Parametro : Tipo ID
             | Tipo ID LBRACKET RBRACKET
             | Tipo DOT DOT DOT ID
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])  # Representa um parâmetro sem dimensão ou elipse
    elif len(p) == 5:
        if p[3] == '...':
            p[0] = (p[1], '...')
        else:
            p[0] = (p[1], p[2], p[3], p[4])  # Representa um parâmetro com dimensão


def p_bloco(p):
    'Bloco : LBRACE Declaracao RBRACE'
    p[0] = p[2]

def p_comentario(p):
    'Comentario : COMMENTS'
    pass

def p_expression(p):
    '''
    Expression : Atribuicao
               | ExpressaoLogica
    '''
    p[0] = p[1]  


# Error rule for syntax errors
def p_error(p):
    print("Syntax error!")
    p.lexer.skip(1)
    
    
parser = yacc.yacc()
yacc.yacc(debug=True)

# Teste do analisador
result = parser.parse(code)
print(f"Resultado '{code}': {result}")
if(result != None):
 print("O código está correto!")
