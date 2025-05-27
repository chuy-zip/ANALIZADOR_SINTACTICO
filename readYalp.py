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
        # Leer archivo carácter a carácter
        with open(self.yalp_file, 'r', encoding='utf-8') as f:
            return list(f.read())


def read_token(chars, index):
    # Saltar comentarios /* ... */
    if index + 1 < len(chars) and chars[index] == '/' and chars[index+1] == '*':
        idx = index + 2
        while idx + 1 < len(chars) and not (chars[idx] == '*' and chars[idx+1] == '/'):
            idx += 1
        return None, idx + 2

    # Tokens únicos
    punctuation = {':', '|', ';'}
    ch = chars[index]
    if ch in punctuation:
        return ch, index + 1

    # Construir token hasta espacio, puntuación o comentario
    start = index
    while index < len(chars):
        c = chars[index]
        if c.isspace() or c in punctuation or (index + 1 < len(chars) and c == '/' and chars[index+1] == '*'):
            break
        index += 1
    token = ''.join(chars[start:index])
    return token, index

class YalpParser:
    def __init__(self, yalp_file, option):
        self.yalp_file = yalp_file
        self.option = option
        # Selecciona el archivo tokens_yaln.json según la opción
        self.tokens_file = f'proyecto1/listas_regex/tokens_yal{option}.json'

    def process(self):
        chars = ReadYalp(self.yalp_file).read_file()
        tokens = []
        idx = 0
        while idx < len(chars):
            c = chars[idx]
            if c.isspace():
                idx += 1
                continue
            tk, idx = read_token(chars, idx)
            if tk is None:
                continue
            tokens.append(tk)

        # Construir producciones crudas
        productions = {}
        i = 0
        while i < len(tokens):
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
                rules.append(current.strip())
                productions[name] = rules
            else:
                i += 1
        #print(productions)
        return productions

    def simplify(self, productions):
        # Carga lexemas de tokens
        with open(self.tokens_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        lex_dict = {tok['nombre']: tok['lexema'] for tok in data['tokens']}

        simplified = {}
        for name, rules in productions.items():
            # Simplifica nombre de producción
            new_name = lex_dict.get(name, name[0].upper())
            new_rules = []
            for rule in rules:
                symbols = rule.split()
                new_syms = []
                for sym in symbols:
                    new_syms.append(lex_dict.get(sym.upper(), sym[0].upper()))
                new_rules.append(' '.join(new_syms))
            simplified[new_name] = new_rules
        #print(simplified)
        return simplified

    def augment(self, grammar):
        # grammar: dict of nonterminal -> list of prod strings
        prods = {nt: [r.split() for r in rules] for nt, rules in grammar.items()}
        start = next(iter(grammar))
        aug_start = start + "'"

        items = []
        # producción aumentada
        items.append({'left': aug_start, 'prod': [start]})
        # producciones originales
        for nt, rules in prods.items():
            for prod in rules:
                items.append({'left': nt, 'prod': prod})
        return items

    

    def to_json(self, output_dir='real_output'):
        # obtener gramática
        raw = self.process()
        simple = self.simplify(raw)
        os.makedirs(output_dir, exist_ok=True)
        gfile = os.path.join(output_dir, 'grammar.json')
        with open(gfile, 'w', encoding='utf-8') as f:
            json.dump(simple, f, ensure_ascii=False, indent=2)
            
        # generar gramática aumentada
        aug_items = self.augment(simple)
        aug_file = os.path.join(output_dir, 'augmented_grammar.json')
        with open(aug_file, 'w', encoding='utf-8') as f:
            json.dump(aug_items, f, ensure_ascii=False, indent=2)

        return simple, aug_items