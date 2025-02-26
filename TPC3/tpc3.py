import re

def markdown_to_html(markdown):
    # Headers
    markdown = re.sub(r'# (.+)', r'<h1>\1</h1>', markdown)
    markdown = re.sub(r'## (.+)', r'<h2>\1</h2>', markdown)
    markdown = re.sub(r'### (.+)', r'<h3>\1</h3>', markdown)

    # Bold
    markdown = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', markdown)

    # Italic
    markdown = re.sub(r'\*(.+?)\*', r'<i>\1</i>', markdown)

    # Numbered List
    markdown = re.sub(r'(\d+\.\s+.*\n?)+', r'<ol>\n\g<0></ol>\n', markdown)
    markdown = re.sub(r'(\d+\. (.+)\n)', r'<li>\g<2></li>\n', markdown)

    # Image
    markdown = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1"/>', markdown)
    
    # Link
    markdown = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', markdown)

    return markdown

# Lê o conteúdo do arquivo de entrada (teste.md)
input_file_path = 'teste.md'
with open(input_file_path, 'r', encoding='utf-8') as file:
    markdown_text = file.read()

# Exemplo de uso
html_output = markdown_to_html(markdown_text)

# Remove o conteúdo anterior do arquivo HTML
output_file_path = 'output.html'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(html_output)

print(f'A saída HTML foi salva em {output_file_path}')