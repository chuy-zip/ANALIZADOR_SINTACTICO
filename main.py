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
import subprocess

def main():
    print("Generador de analizador sintáctico")

    yalp_files = [
        "input/slr-1.yalp",
        "input/slr-2.yalp",
        "input/slr-3.yalp",
        "input/slr-4.yalp"
    ]

    print("Elige un archivo seleccinando el numero correspondiente:")
    for idx, name in enumerate(yalp_files, 1):
        print(f"{idx}. {name}")

    try:
        option = int(input("> "))
        filename = yalp_files[option - 1]
    except (ValueError, IndexError):
        print("Opción inválida.")
        return

    parser = YalpParser(filename, option)
    productions, au_grammar = parser.to_json()
    print(f"\nArchivo grammar.json generado en real_output/\n")
    #print(json.dumps(productions, ensure_ascii=False, indent=2))

    print(f"\nArchivo augmented_grammar.json generado en real_output/\n")
    #print(json.dumps(au_grammar, ensure_ascii=False, indent=2))

    aug_path = os.path.join('real_output', 'augmented_grammar.json')
    # invocar automataTable.py para construir la tabla
    subprocess.run(['python', 'automataTable.py', aug_path])
    print('automaton.json generado en real_output/')
    

if __name__ == '__main__':
    main()