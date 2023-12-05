import lex, yacc

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

# Ignorar espaços em branco e tabulações
t_ignore = ' \t'

# Regra para token ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # Converta para minúsculas antes de verificar as palavras reservadas
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
int x = 2;
void fun(int a, double b, char c[]) {
    int result;
    result = x + 2;
    if (result > 0) {
        println(result);
    } else {
        println(0);
    }
}
'''
# Contrução do analisador léxico
lexer = lex.lex()
lexer.input(code)

for token in lexer:
    print(token)

##############################################################################################################

# Regras de produção para o analisador sintático


# Adiciona informações de precedência
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
)

def p_program(p):
    'Programa : Declaracao'

def p_declaracao(p):
    '''
    Declaracao : DeclaracaoVariavel
               | DeclaracaoFuncao
               | Comentario
               | DeclaracaoEstrutura
               | EstruturaControle
               | expression
               | array
               |
    '''

def p_array(p):
    '''
    array : ID LBRACKET expression RBRACKET
          | ID LBRACKET RBRACKET
    '''

def p_array_inicializacao(p):
    'ArrayInicializacao : LBRACE ExpressaoLista RBRACE'

def p_expressao_logica(p):
    '''
    ExpressaoLogica : ExpressaoRelacional
                   | ExpressaoLogica AND ExpressaoRelacional
                   | ExpressaoLogica OR ExpressaoRelacional
                   | NOT ExpressaoRelacional
    '''

def p_expressao_relacional(p):
    '''
    ExpressaoRelacional : ExpressaoAritmetica
                       | ExpressaoAritmetica MAIOR_QUE ExpressaoAritmetica
                       | ExpressaoAritmetica MA_IGUAL ExpressaoAritmetica
                       | ExpressaoAritmetica MENOR_QUE ExpressaoAritmetica
                       | ExpressaoAritmetica ME_IGUAL ExpressaoAritmetica
                       | ExpressaoAritmetica DIF_DE ExpressaoAritmetica
                       | ExpressaoAritmetica COMPARA ExpressaoAritmetica
    '''

def p_expressao_aritmetica(p):
    '''
    ExpressaoAritmetica : ExpressaoMultiplicativa
                       | ExpressaoAritmetica PLUS ExpressaoMultiplicativa
                       | ExpressaoAritmetica MINUS ExpressaoMultiplicativa
    '''

def p_expressao_multiplicativa(p):
    '''
    ExpressaoMultiplicativa : ExpressaoUnaria
                          | ExpressaoMultiplicativa MULT ExpressaoUnaria
                          | ExpressaoMultiplicativa DIV ExpressaoUnaria
                          | ExpressaoMultiplicativa MOD ExpressaoUnaria
    '''

def p_expressao_unaria(p):
    '''
    ExpressaoUnaria : ExpressaoPostfix
                   | MINUS ExpressaoUnaria
                   | PLUS ExpressaoUnaria
                   | INCREMENT ExpressaoPostfix
                   | DECREMENT ExpressaoPostfix
    '''

def p_expressao_postfix(p):
    '''
    ExpressaoPostfix : Primaria
                    | Primaria LBRACKET expression RBRACKET
                    | Primaria LPAREN argumentos RPAREN
                    | Primaria DOT ID
                    | Primaria ARROW ID
    '''
    # Adicione ações semânticas se necessário

def p_argumentos(p):
    '''
    argumentos :  ExpressaoLista 
               |
    '''

def p_primaria(p):
    '''
    Primaria : ID
            | NUMBER
            | NUM_DEC
            | TEXTO
            | LPAREN expression RPAREN
    '''


def p_declaracao_estrutura(p):
    'DeclaracaoEstrutura : STRUCT ID LBRACE DeclaracaoVariavel RBRACE SEMICOLON'


def p_atribuicao(p):
    '''
    atribuicao : ID EQUALS expression
               | ID PLUS EQUALS expression
               | ID MINUS EQUALS expression
               | ID MULT EQUALS expression
               | ID DIV EQUALS expression
               | ID MOD EQUALS expression
               | ID AND AND EQUALS expression
               | ID OR OR EQUALS expression
               | ID EQUALS ID
               | ID PLUS EQUALS ID
               | ID MINUS EQUALS ID
               | ID MULT EQUALS ID
               | ID DIV EQUALS ID
               | ID MOD EQUALS ID
               | ID AND AND EQUALS ID
               | ID OR OR EQUALS ID
    '''

def p_estrutura_controle(p):
    '''
    EstruturaControle : IF LPAREN expression RPAREN Bloco
                     | IF LPAREN expression RPAREN Bloco ELSE Bloco
                     | WHILE LPAREN expression RPAREN Bloco
                     | FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN Bloco
                     | SWITCH LPAREN expression RPAREN CaseLista
                     | BREAK SEMICOLON
                     | CONTINUE SEMICOLON
                     | RETURN expression SEMICOLON
    '''

def p_case_lista(p):
    '''
    CaseLista : CaseDecl
              | CaseDecl CaseLista
    '''

def p_case_decl(p):
    '''
    CaseDecl : CASE expression COLON Bloco
             | DEFAULT COLON Bloco
    '''


def p_declaracao_variavel(p):
    '''
    DeclaracaoVariavel : Tipo ID SEMICOLON
                      | Tipo ID EQUALS expression SEMICOLON
    '''

def p_tipo(p):
    '''
    Tipo : INT
         | FLOAT
         | DOUBLE
         | CHAR
         | BOOLEAN
    '''

def p_declaracao_funcao(p):
    'DeclaracaoFuncao : Tipo ID LPAREN Parametros RPAREN Bloco'

def p_parametros(p):
    '''
    Parametros : Parametro
               | Parametro COMMA Parametro
    '''

def p_parametro(p):
    '''
    Parametro : Tipo ID
             | Tipo ID LBRACKET RBRACKET
             | Tipo DOT DOT DOT ID
    '''

def p_bloco(p):
    'Bloco : LBRACE Declaracao RBRACE'

def p_comentario(p):
    'Comentario : COMMENTS'

def p_expression(p):
 '''
 expression : expression PLUS term
 | expression MINUS term
 | term
 | atribuicao
 | ExpressaoLogica
 '''
 if len(p) == 2:
        p[0] = p[1]
 else:
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_times(p):
    'term : term MULT factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIV factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

#Error handling rule
def p_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Construção do analisador sintático
parser = yacc.yacc()
yacc.yacc(debug=True)

# Teste do analisador
result = parser.parse(code)
print(f"Resultado '{code}': {result}")