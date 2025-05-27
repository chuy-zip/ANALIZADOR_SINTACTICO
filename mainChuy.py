from AutomataLR import AutomataLR
import json
grammar = {}
transition_table = {}
with open('./output/grammar_example.json', 'r', encoding='utf-8') as file:
    grammar = json.load(file)
with open('./output/automata_table_Example.json', 'r') as file:
    transition_table = json.load(file)

print(f'{grammar=}')
print(f'{transition_table=}')
Automata = AutomataLR(transition_table, grammar)

print(Automata.action_goto_table.Action("0", "id"))
print(Automata.action_goto_table.Goto("0",'E'))

def run_tests():
    print("🧪 INICIANDO PRUEBAS DEL PARSER LR")
    print("=" * 50)
    
    # Casos válidos esperados
    valid_test_cases = [
        (['id'], "Expresión simple"),
        (['id', '+', 'id'], "Suma simple"),
        (['id', '*', 'id'], "Multiplicación simple"),
        (['id', '+', 'id', '*', 'id'], "Suma y multiplicación"),
        (['(', 'id', ')'], "Paréntesis simples"),
        (['(', 'id', '+', 'id', ')', '*', 'id'], "Expresión compleja"),
        (['id', '+', 'id', '+', 'id'], "Múltiples sumas"),
        (['id', '*', 'id', '*', 'id'], "Múltiples multiplicaciones"),
    ]
    
    # Casos inválidos esperados
    invalid_test_cases = [
        (['id', '+'], "Operador sin operando derecho"),
        (['+', 'id'], "Operador sin operando izquierdo"),
        (['id', '+', '*', 'id'], "Dos operadores consecutivos"),
        (['(', 'id', '+', 'id'], "Paréntesis sin cerrar"),
        (['id', '+', 'id', ')'], "Paréntesis sin abrir"),
        (['(', ')'], "Paréntesis vacíos"),
        (['id', 'id'], "Dos identificadores consecutivos"),
        ([], "Cadena vacía"),
    ]
    
    # Ejecutar casos válidos
    print("\n✅ CASOS VÁLIDOS:")
    valid_passed = 0
    for tokens, description in valid_test_cases:
        result = Automata.LR_parsing(tokens.copy())
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {description}: {tokens}")
        if result:
            valid_passed += 1
    
    # Ejecutar casos inválidos
    print("\n❌ CASOS INVÁLIDOS:")
    invalid_passed = 0
    for tokens, description in invalid_test_cases:
        result = Automata.LR_parsing(tokens.copy())
        status = "✅ PASS" if not result else "❌ FAIL"
        print(f"{status} - {description}: {tokens}")
        if not result:
            invalid_passed += 1
    
    # Resumen
    total_valid = len(valid_test_cases)
    total_invalid = len(invalid_test_cases)
    total_tests = total_valid + total_invalid
    total_passed = valid_passed + invalid_passed
    
    print(f"\n📊 RESUMEN:")
    print(f"Casos válidos: {valid_passed}/{total_valid}")
    print(f"Casos inválidos: {invalid_passed}/{total_invalid}")
    print(f"Total: {total_passed}/{total_tests}")
    print(f"Porcentaje de éxito: {(total_passed/total_tests)*100:.1f}%")

# Ejecutar todas las pruebas
run_tests()

print("Generando visualización completa...")
Automata.visualize_automaton(
    filename="automata_lr0_completo",
    format="png",
    view=True
)

# Información en consola
Automata.print_automaton_info()

# Generar en diferentes formatos
formats = ['png', 'pdf', 'svg']
for fmt in formats:
    Automata.visualize_automaton(
        filename=f"automata_lr0_{fmt}",
        format=fmt,
        view=False
    )
    print(f"Generado en formato {fmt}")

