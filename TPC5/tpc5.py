import json
import ply.lex as lex
from datetime import datetime

# stock do json
with open('stock.json', 'r') as json_file:
    produtos = json.load(json_file)["stock"]

tokens = (
    'OPERATION',
    'COIN',
    'ID',
    'COMMA',
    'POINT'
)

t_COMMA = r','
t_ignore = ' \t'

SALDO = 0.0
moedas = False
escolher_prod = False 

def processar_produto(id_prod):
    global SALDO
    produto = False

    # produto existe?
    for prod in produtos:
        if id_prod == prod['cod']:
            produto = prod
            break

    if produto is False:
        print("Produto não encontrado.")
        return

    #  há quantidade disponível?
    if produto['quant'] <= 0:
        print(f"Produto {produto['nome']} está fora de estoque.")
        return

    # saldo é suficiente?
    if SALDO < produto['preco']:
        print(f"Saldo insuficiente para satisfazer o seu pedido. Saldo = {SALDO:.2f}; Pedido = {produto['preco']:.2f}")
        return

    # Podemos comprar!
    print(f"Pode retirar o produto dispensado {produto['nome']}")
    produto['quant'] -= 1  # Tirar o produto do stock
    SALDO -= produto['preco']  # Atualizar o saldo
    print(f"Saldo = {SALDO:.2f}")  

    
def processar_moedas(coin_value):
    global SALDO
    if coin_value.endswith('e'):
        SALDO += float(coin_value[:-1])
    else:
        SALDO += float(coin_value[:-1]) * 0.01

def processar_pedido(operation):
    global moedas, escolher_prod

    if operation == 'LISTAR':
        print("cod | nome | quantidade | preço")
        print("---------------------------------")
        for produto in produtos:
            print(f"{produto['cod']} {produto['nome']} {produto['quant']} {produto['preco']:.2f}")  # Arredondamento para duas casas decimais
    
    if operation == 'MOEDA':
        moedas = True
        escolher_prod = False  

    if operation == 'SELECIONAR':
        escolher_prod = True
        moedas = False 

    if operation == 'SAIR':
        troco_mensagem = calcular_troco(SALDO)
        print(troco_mensagem)
        print("Obrigado por usar a Máquina de Venda!")

        # Salvar o estado atualizado do stock no arquivo JSON
        with open('stock.json', 'w') as json_file:
            json.dump({"stock": produtos}, json_file)
        exit()

def calcular_troco(saldo):
    troco_mensagem = "Pode retirar o troco: "
    
    moedas_troco = {
        "1e": 1.00,
        "50c": 0.50,
        "20c": 0.20,
        "10c": 0.10,
        "5c": 0.05,
        "2c": 0.02,
        "1c": 0.01
    }
    
    for moeda, valor in moedas_troco.items():
        quantidade_moedas = int(saldo // valor)
        saldo = round(saldo - quantidade_moedas * valor, 2)
        if quantidade_moedas > 0:
            troco_mensagem += f"{quantidade_moedas}x {moeda}, "
    
    return troco_mensagem.rstrip(", ")

def t_ID(t):
    r'[A-Z]\d+'
    if escolher_prod:
        processar_produto(t.value)
    return t

def t_OPERATION(t):
    r'\b[A-Z]+\b'
    processar_pedido(t.value)
    return t

def t_POINT(t):
    r'\.'
    print(f"Saldo = {SALDO:.2f}")  # Arredondamento para duas casas decimais
    return t

def t_COIN(t):
    r'\d+[ec]'
    if moedas:
        processar_moedas(t.value)
    return t

def t_error(t):
    print("Caractere inválido '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

def read_input(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break

#inicio
data_atual = datetime.now().strftime("%Y-%m-%d")
print(f"maq: {data_atual}, Stock carregado, Estado atualizado.")
print("Bom dia. Estou disponível para atender o seu pedido.")

while True:
    user_input = input()
    read_input(user_input)