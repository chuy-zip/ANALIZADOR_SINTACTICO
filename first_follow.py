# Este codigo es obtenido de una implementacion propia realizada por el equipo para una tarea previa
# el enlace al repositorio anterior es el siguiente: https://github.com/chuy-zip/FIRST_FOLLOW_LAB

def is_terminal(symbol, terminals):
    return symbol in terminals

def first(symbol, grammar, terminals, first_sets, visited=None):
    if visited is None:
        visited = set()
    
    print(f"\nCalculando FIRST( {symbol} )...")
    print(f"Visitados: {visited}")

    # Caso base 1: Símbolo terminal
    if is_terminal(symbol, terminals):
        print(f"{symbol} es terminal entonces, FIRST( {symbol} ) = {{{symbol}}}")
        return {symbol}
    
    # Caso base 2: Épsilon
    if symbol == 'ε':
        print(f"ε encontrado → FIRST(ε) = {{ε}}")
        return {'ε'}
    
    # Evitar recursión infinita
    if symbol in visited:
        return set()
    visited.add(symbol)
    
    result = set()

    print(f"Producciones de {symbol}: {grammar.get(symbol, [])}")
    # Para cada producción del no terminal
    for production in grammar.get(symbol, []):
        symbols_in_prod = production.split()

        print(f"\nProcesando producción: {production}")
        print(f"Símbolos en producción: {symbols_in_prod}")
        
        # Caso: X -> ε 
        if not symbols_in_prod:
            result.add('ε')
            continue
            
        # Para cada símbolo en la producción X -> Y1, Y2...Yn
        for i, current_symbol in enumerate(symbols_in_prod):
            current_first = first(current_symbol, grammar, terminals, first_sets, visited.copy())
            print(f"FIRST( {current_symbol} ) = {current_first}")

            # Agregar todos los símbolos excepto ε, en este caso ya solo agregamos ε si llegamos al final
            # y vemos que el no terminal puede generar ε para todas sus producciones 
            result.update(current_first - {'ε'})
            
            # Si ε no está en current_first, no continuar ya que significa que hemos encontrado un terminal 
            # no es necesario seguir iterando en en los simbolos de la produccion. 
            if 'ε' not in current_first:
                print(f"ε ∉ FIRST( {current_symbol} ) → Terminando esta producción")
                break
                
            # Si llegamos al final y todos tienen ε, agregar ε
            if i == len(symbols_in_prod) - 1:
                print("Todos los símbolos pueden ser ε → Agregando ε al resultado")
                result.add('ε')
    
    print(f"\nFIRST( {symbol} ) final: {result}")
    return result

def calculate_first(grammar, terminals, first_follow_table):
    first_sets = {nt: set() for nt in grammar}
    
    for non_terminal in grammar:
        print(f"\nCALCULANDO EL FIRST DEL NO TERMINAL {non_terminal}")
        new_first = first(non_terminal, grammar, terminals, first_sets)
        first_sets[non_terminal].update(new_first)
        
        first_follow_table[non_terminal]["first"] = new_first


def first_of_string(symbols, first_follow_table, terminals):

    result = set()
    # Si la secuencia está vacía, se retorna {ε}
    if not symbols:
        result.add("ε")
        return result

    # Se procesa cada símbolo de la secuencia
    for symbol in symbols:
        if symbol in terminals:
            # Si es terminal, se agrega directamente y se detiene el proceso
            result.add(symbol)
            return result
        else:
            # Si es un no terminal, se agregan los símbolos de su FIRST exceptuando ε
            first_set = first_follow_table[symbol]["first"]
            result.update(first_set - {"ε"})
            # Si no se puede derivar ε, se detiene aquí
            if "ε" not in first_set:
                return result
    # Si todos los símbolos podían derivar ε, se agrega ε al resultado
    result.add("ε")
    return result

def calculate_follow(grammar, first_follow_table, non_terminals, terminals):

    # Se asume que el primer no terminal de la gramática es el símbolo inicial.
    start_symbol = list(grammar.keys())[0]
    print(f"\nCalculando Follow de {start_symbol}")
    first_follow_table[start_symbol]["follow"].add("$")
    print(f"Caso 1: FOLLOW( {start_symbol} ) = { {'$'} }")

    changed = True
    while changed:
        changed = False
        for A in grammar:
            for production in grammar[A]:
                symbols = production.split()

                # Iterar sobre cada símbolo en la producción
                for i in range(len(symbols)):
                    B = symbols[i]
                    if B not in non_terminals:
                        continue  # Ignorar terminales

                    # Caso 1: A -> αBβ (β no vacío)
                    if i < len(symbols) - 1:
                        beta = symbols[i + 1:]
                        first_beta = first_of_string(beta, first_follow_table, terminals)

                        # Agregar FIRST(β) - {ε} a FOLLOW(B)
                        before = len(first_follow_table[B]["follow"])
                        first_follow_table[B]["follow"].update(first_beta - {"ε"})
                        if len(first_follow_table[B]["follow"]) > before:
                            changed = True

                        # Si ε ∈ FIRST(β), agregar FOLLOW(A) a FOLLOW(B)
                        if "ε" in first_beta:
                            before = len(first_follow_table[B]["follow"])
                            first_follow_table[B]["follow"].update(first_follow_table[A]["follow"])
                            if len(first_follow_table[B]["follow"]) > before:
                                changed = True

                    # Caso 2: A -> αB (β vacío)
                    else:
                        before = len(first_follow_table[B]["follow"])
                        first_follow_table[B]["follow"].update(first_follow_table[A]["follow"])
                        if len(first_follow_table[B]["follow"]) > before:
                            changed = True
            
    return first_follow_table