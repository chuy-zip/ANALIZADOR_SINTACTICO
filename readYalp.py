# readYalp.py
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

    # Separadores y token único (incluye coma)
    punctuation = {':', '|', ';', ','}
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
            if chars[idx].isspace():
                idx += 1
                continue
            tk, idx = read_token(chars, idx)
            if tk is None:
                continue
            tokens.append(tk)
        print(tokens)

        # Manejar IGNORE: recopilar tokens a ignorar
        ignore_tokens = set()
        i = 0
        while i < len(tokens):
            if tokens[i] == 'IGNORE':
                j = i + 1
                # Tras IGNORE, leer nombres separados por comas
                count_coma = 0
                count_token = 0
                while j < len(tokens):
                    if tokens[j] == ',':
                        j += 1
                        count_coma += 1 
                        continue
                    if tokens[j] in {':', '|', ';'} or tokens[j] == 'IGNORE' or (count_coma + 1) == count_token:
                        break
                    # tokens[j] es nombre a ignorar
                    ignore_tokens.add(tokens[j])
                    count_token += 1
                    j += 1
                i = j
            else:
                i += 1

        # Guardar ignore_tokens en real_output/ignore_tokens.json
        os.makedirs('real_output', exist_ok=True)
        ignore_file = os.path.join('real_output', 'ignore_tokens.json')
        with open(ignore_file, 'w', encoding='utf-8') as f:
            json.dump(list(ignore_tokens), f, ensure_ascii=False, indent=2)

        # Construir producciones crudas, ignorando 'IGNORE' y ','
        productions = {}
        i = 0
        while i < len(tokens):
            if tokens[i] == 'IGNORE' or tokens[i] == ',':
                i += 1
                continue
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
                    elif tokens[i] == ',' or tokens[i] == 'IGNORE':
                        # omitir
                        pass
                    else:
                        current += tokens[i] + ' '
                    i += 1
                rules.append(current.strip())
                productions[name] = rules
            else:
                i += 1

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
        return simplified

    def augment(self, grammar):
        # grammar: dict de no terminal -> lista de cadenas
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
        # obtener gramática y tokens a ignorar
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

    def get_lexer_token_list(self):
        with open(self.tokens_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        lex_dict = {tok['nombre']: tok['lexema'] for tok in data['tokens']}
        return lex_dict
