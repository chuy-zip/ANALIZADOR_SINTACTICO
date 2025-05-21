"""
Autores:
- Nelson García Bravatti 
- Ricardo Chuy
- Joaquín Puente

Diseño de Lenguajes de Programación
"""

import os
import json
from readYalp import YalpParser


def main():
    print("Generador de analizador sintáctico")

    yalp_files = ["input/slr-1.yalp", "input/slr-2.yalp", "input/slr-3.yalp", "input/slr-4.yalp"]

    option = 0

    print("Elige un archivo seleccinando el numero correspondiente:")

    for idx, name in enumerate(yalp_files, 1):
            print(f"{idx}. {name}")

    try:
        option = int(input("> "))
        filename = yalp_files[option - 1]
    except (ValueError, IndexError):
        print("Opción inválida.")
        return

    parser = YalpParser(filename)
    json_file, productions = parser.to_json(output_dir='output', out_name='grammar_example.json')
    print(f"Archivo JSON generado: {json_file}")
    print(json.dumps(productions, ensure_ascii=False, indent=2))



if __name__ == '__main__':
    main()


# from ActionGotoTable import ActionGotoTable
# import json

# data = {}

# with open('ActionGotoTableExample.json', 'r') as file:
#     data = json.load(file)

# action_goto_table = ActionGotoTable(data)

# state = "5"
# terminal = "*"
# nonTerminal = "E"

# value1 = action_goto_table.Action(state, terminal)
# value2 = action_goto_table.Goto(state, nonTerminal)