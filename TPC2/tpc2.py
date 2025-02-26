import sys
import re

# Ler o arquivo CSV da entrada padrão
csv = sys.stdin.read().splitlines()

# Inicializar variáveis
compositores = set()
distribuicao_periodo = {}
obras_por_periodo = {}

# Juntar linhas quebradas
linhas_juntas = []
linha_atual = ""

for linha in csv:
    if linha.startswith(" ") or linha.startswith("\t"):
        linha_atual += " " + linha.strip()
    else:
        if linha_atual:
            linhas_juntas.append(linha_atual)
        linha_atual = linha.strip()

if linha_atual:
    linhas_juntas.append(linha_atual)

#Processar cada linha do CSV (ignorando o cabeçalho)
for linha in linhas_juntas[1:]:
    dados = re.split(r';\s*', linha)

    # Verificar se a linha tem o número correto de colunas
    if len(dados) != 7:
        continue
    

    compositor = dados[4].strip()
    titulo = dados[0].strip()
    periodo = dados[3].strip()

    # Adicionar compositor à lista de compositores
    compositores.add(compositor)

    # Atualizar a distribuição das obras por período
    if periodo in distribuicao_periodo:
        distribuicao_periodo[periodo] += 1
    else:
        distribuicao_periodo[periodo] = 1

    # Atualizar o dicionário de obras por período
    if periodo in obras_por_periodo:
        obras_por_periodo[periodo].append(titulo)
    else:
        obras_por_periodo[periodo] = [titulo]

# Ordenar compositores alfabeticamente
compositores_ordenados = sorted(compositores)

# Ordenar títulos das obras por período
for periodo in obras_por_periodo:
    obras_por_periodo[periodo].sort()

# Imprimir os resultados
for compositor in compositores_ordenados:
    print(compositor)

print("---------------------------")
for periodo, quantidade in distribuicao_periodo.items():
    print(f"{periodo}: {quantidade} obras")

print("---------------------------")
for periodo, obras in obras_por_periodo.items():
    print(f"{periodo}: {obras}")

# Exemplo de uso
# Para testar o script, você pode redirecionar a entrada de um arquivo CSV:
# python tpc2.py < obras.csv