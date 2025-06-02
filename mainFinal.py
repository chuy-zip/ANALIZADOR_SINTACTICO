"""
Diseño de Lengujes de Programacion

Autores:
    Nelson García Bravatti
    Joaquín Puente
    Ricardo Chuy

"""

from pprint import pprint
from readYalex import process_yalex_file, simplify_tokens, guardar_tokens_json, transform_let_regex_list
from lexer import load_dfa, process_file, load_token_names, build_dfa_nodes
from AFD_generator import generate_AFD_from_json
import os
import json
from readYalp import YalpParser
import subprocess
from AutomataLR import AutomataLR

print("Generador de analizador léxico")

yalex_files = ["yalex_prueba/slr-1.yal", "yalex_prueba/slr-2.yal",
               "yalex_prueba/slr-3.yal", "yalex_prueba/slr-4.yal"]
option = 0

print("Elige un archivo seleccinando el numero correspondiente:")

for index, item in enumerate(yalex_files):
    print(f"{index + 1}. {item}")

option = int(input("\nEleccion: "))

selected_yal = yalex_files[option-1]
print("Opcion seleccionada:", selected_yal)

# Definir el archivo yalex a procesar
# yalex_file = "yalex_prueba/slr-4.yal"

let_toks, let_re, rule_toks, rule_act = process_yalex_file(selected_yal)
print("Lista de tokens (sección let):")
print(let_toks)
print("\nLista de expresiones regulares (sección let):")
print(let_re)
print("\nLista de tokens (sección rule):")
print(rule_toks)
print("\nLista de acciones o return (sección rule):")
print(rule_act)

# Transformar las expresiones de la sección let que usan corchetes
let_re = transform_let_regex_list(let_re)
print("\nLista de expresiones regulares transformadas (sección let):")
print(let_re)

final_tokens, actions = simplify_tokens(let_toks, let_re, rule_toks, rule_act)
print("\nLista de tokens finales (expresiones expandidas):")
print(final_tokens)
print("\nLista de acciones finales:")
print(actions)

# Guardamos en un archivo JSON los tokens finales emparejados con sus acciones
guardar_tokens_json(final_tokens, actions, "expressions.json")
#print("\nArchivo 'tokens.json' generado exitosamente.")

# Creacion del AFD a partir del archivo expressions.json
# esta funcion guarda el AFD y tabla de transiciones en archivos pkl para hacer luego la parte del análsisi léxico.
transitions, acceptance = generate_AFD_from_json()

#transitions, acceptance = load_dfa("transition_table.pkl", "acceptance_states.pkl")
nodes, start_node = build_dfa_nodes(transitions, acceptance)
token_names = load_token_names('final_out_test.json')


## Aqui ahora se agrega la parte de la eleccion del yalp con la gramatica

"""
Autores:
- Nelson García Bravatti 
- Ricardo Chuy
- Joaquín Puente

Diseño de Lenguajes de Programación
"""



print("Generador de analizador sintáctico")

yalp_files = [
    "input/slr-1.yalp",
    "input/slr-2.yalp",
    "input/slr-3.yalp",
    "input/slr-4.yalp",
    "input/slr-1_2.yalp",
]

print("Elige un archivo seleccinando el numero correspondiente:")
for idx, name in enumerate(yalp_files, 1):
    print(f"{idx}. {name}")

try:
    option = int(input("> "))
    filename = yalp_files[option - 1]
except (ValueError, IndexError):
    print("Opción inválida.")


parser = YalpParser(filename, option)
lex_dict = parser.get_lexer_token_list()

productions, au_grammar = parser.to_json()
print(f"\nArchivo grammar.json generado en real_output/\n")
#print(json.dumps(productions, ensure_ascii=False, indent=2))

print(f"\nArchivo augmented_grammar.json generado en real_output/\n")
#print(json.dumps(au_grammar, ensure_ascii=False, indent=2))

aug_path = os.path.join('real_output', 'augmented_grammar.json')
# invocar automataTable.py para construir la tabla
subprocess.run(['python', 'automataTable.py', aug_path])
print('automaton.json generado en real_output/')
    
# despues de generar los archivos de los modulos para la construccion del automata
# ahora se crea el objeto automata

grammar = {}
transition_table = {}
#real_output/automaton.json
#real_output/grammar.json
with open('./real_output/grammar.json', 'r', encoding='utf-8') as file:
    grammar = json.load(file)
with open('./real_output/automaton.json', 'r') as file:
    transition_table = json.load(file)

#print(f'{grammar}')
#print(f'{transition_table}')
Automata = AutomataLR(transition_table, grammar)
# Generar en diferentes formatos
formats = ['png', 'pdf', 'svg']
for fmt in formats:
    Automata.visualize_automaton(
        filename=f"AUTOMATA_LR(0)/automata_lr0_{fmt}",
        format=fmt,
        view=False
    )
    print(f"Generado en formato {fmt}")

#print(Automata.action_goto_table.Action("0", "id"))
#print(Automata.action_goto_table.Goto("0",'E'))

files = [
    "input_to_parse/inputTest.txt",
    "input_to_parse/numbers_expressions.txt",
    "input_to_parse/variable_expressions.txt"
]

while True:
    menu_text = "\n=== MENÚ DE OPCIONES ===\n\n" + \
                f"1) Procesar archivo: {files[0]}\n" + \
                f"2) Procesar archivo: {files[1]}\n" + \
                f"3) Procesar archivo: {files[2]}\n" + \
                "4) Salir\n"

    print(menu_text)

    choice = input("Elige una opción: ")

    if choice in ['1', '2', '3']:
        index = int(choice) - 1
        file_path = files[index]

        if not os.path.exists(file_path):
            error_msg = f"\nEl archivo '{
                file_path}' no existe. Revisa la ruta.\n"
            print(error_msg)
            continue

        processing_msg = f"\nProcesando el archivo: {file_path}\n"
        print(processing_msg)

        # aqui queda la lista de tokens de 
        token_iterator = process_file(file_path, start_node, token_names, True)
        Automata.LR_parsing(token_iterator, lex_dict)

        # json_filename = f'tokens.json'
        # with open(json_filename, 'w') as json_file:
        #     json.dump(tokens, json_file, indent=4)

        # tokens_str = json.dumps(tokens, indent=4)

    elif choice == '4':
        exit_msg = "\nSaliendo del programa. ¡Hasta luego!\n"
        break

    else:
        invalid_msg = "\nOpción inválida. Inténtalo de nuevo.\n"
