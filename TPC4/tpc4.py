import re

def lexer(query):

    patterns = [
        (r'\s+', 'SPACE'),  
        (r'select', 'SELECT'),
        (r'where', 'WHERE'),
        (r'LIMIT', 'LIMIT'),
        (r'\?[a-zA-Z_]\w*', 'TIPO'),  # assumi ?qualquercoisa tanto '?nome' como '?s' eram TIPO
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'), # se não tiver '?' é um IDENTIFIER
        (r'"[^"]*"', 'STRING'),
        (r'\{', 'LBRACE'),  # Chave esquerda
        (r'\}', 'RBRACE'),  # Chave direita
        (r':', 'COLON'),  # Dois pontos
        (r'\.', 'DOT'),  # Ponto
        (r'\d+', 'INTEGER'), 
        ]

    # expressão regular 
    regex = '|'.join('(%s)' % pattern for pattern, _ in patterns)


    pos = 0


    for match in re.finditer(regex, query):
        for i, groupname in enumerate(pattern for pattern, _ in patterns):
            if match.group(i + 1):
                token_type = patterns[i][1]
                token_value = match.group(i + 1)

                #  espaços em branco
                if token_type != 'SPACE':
                    yield token_type, token_value

                # Atualizar posição atual
                pos = match.end()
                break

# Exemplo TPC4
query = '''
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
'''

for token in lexer(query):
    print(token)