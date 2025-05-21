"""
Autores:
- Nelson García Bravatti 
- Ricardo Chuy
- Joaquín Puente

Diseño de Lenguajes de Programación
"""

import json
import os

class ReadYalp:
    def __init__(self, yalp_file):
        self.yalp_file = yalp_file

    def read_file(self):
        with open(self.yalp_file, 'r', encoding='utf-8') as f:
            return list(f.read())


def read_token(chars, index):
    # Manejo de comentarios /* ... */
    if index + 1 < len(chars) and chars[index] == '/' and chars[index+1] == '*':
        idx = index + 2
        # Saltar hasta */
        while idx + 1 < len(chars) and not (chars[idx] == '*' and chars[idx+1] == '/'):
            idx += 1
        return None, idx + 2

    # Separadores y token único
    punctuation = {':', '|', ';'}
    ch = chars[index]
    if ch in punctuation:
        return ch, index + 1

    # Si es espacio, no debería llegar aquí (se ignora fuera)
    # Construir token hasta whitespace o puntuación
    start = index
    while index < len(chars):
        c = chars[index]
        if c.isspace() or c in punctuation or (index + 1 < len(chars) and c == '/' and chars[index+1] == '*'):
            break
        index += 1
    token = ''.join(chars[start:index])
    return token, index


class YalpParser:
    def __init__(self, yalp_file):
        self.yalp_file = yalp_file

    def process(self):
        chars = ReadYalp(self.yalp_file).read_file()
        tokens = []
        idx = 0
        while idx < len(chars):
            c = chars[idx]
            # Ignorar espacios
            if c.isspace():
                idx += 1
                continue
            tk, idx = read_token(chars, idx)
            if tk is None:
                continue
            tokens.append(tk)

        # Parseo de producciones
        productions = {}
        i = 0
        while i < len(tokens):
            # Nombre de producción seguido de ':'
            if i+1 < len(tokens) and tokens[i+1] == ':':
                name = tokens[i]
                i += 2
                rules = []
                current = ''
                while i < len(tokens) and tokens[i] != ';':
                    if tokens[i] == '|':
                        rules.append(current.strip())
                        current = ''
                    else:
                        current += tokens[i] + ' '
                    i += 1
                # última regla antes de ';'
                rules.append(current.strip())
                productions[name] = rules
            else:
                i += 1
        return productions

    def to_json(self, output_dir='output', out_name='grammar_example.json'):
        prods = self.process()
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, out_name)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(prods, f, ensure_ascii=False, indent=2)
        return path, prods