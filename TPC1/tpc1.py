import sys
import ply.lex as lex

# Lista de tokens
tokens = (
    'ON',
    'OFF',
    'NUMBER',
    'EQUALS'
)

def t_ON(t):
    r'[Oo][Nn]'
    return t

def t_OFF(t):
    r'[Oo][Ff][Ff]'
    return t

def t_EQUALS(t):
    r'='
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espaços em branco e pontuação
t_ignore = ' \t\n.,;:!?"\'-'

# Função para tratar erros
def t_error(t):
    t.lexer.skip(1)


lexer = lex.lex()


def somar_on_off(data):
    lexer.input(data)
    sum_active = True  # Iniciar ON
    total_sum = 0

    for token in lexer:
        if token.type == 'ON':
            sum_active = True
        elif token.type == 'OFF':
            sum_active = False
        elif token.type == 'NUMBER' and sum_active:
            total_sum += token.value
        elif token.type == 'EQUALS':
            print(total_sum)

    print(total_sum) #imprimir no fim mesmo não tendo o '=' no final

# Ler input
data = sys.stdin.read()
somar_on_off(data)