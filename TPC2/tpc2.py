import sys
import re


csv = sys.stdin.read().splitlines()

compositores = set()
distribuicao_periodo = {}
obras_por_periodo = {}

# tratar das linhas
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

#ignor o cabeçalho
for linha in linhas_juntas[1:]:
    dados = re.split(r';\s*', linha)

    # eliminar linhas com ; diferente das colunas
    if len(dados) != 7:
        continue
    

    compositor = dados[4].strip()
    titulo = dados[0].strip()
    periodo = dados[3].strip()

#tarefa1
    compositores.add(compositor)
#tarefa2
    if periodo in distribuicao_periodo:
        distribuicao_periodo[periodo] += 1
    else:
        distribuicao_periodo[periodo] = 1
#tarefa3
    if periodo in obras_por_periodo:
        obras_por_periodo[periodo].append(titulo)
    else:
        obras_por_periodo[periodo] = [titulo]

#  alfabetica
compositores_ordenados = sorted(compositores)

for periodo in obras_por_periodo:
    obras_por_periodo[periodo].sort()

for compositor in compositores_ordenados:
    print(compositor)

print("---------------------------")
for periodo, quantidade in distribuicao_periodo.items():
    print(f"{periodo}: {quantidade} obras")

print("---------------------------")
for periodo, obras in obras_por_periodo.items():
    print(f"{periodo}: {obras}")

