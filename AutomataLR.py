from ActionGotoTable import ActionGotoTable
from first_follow import calculate_first, calculate_follow

class AutomataLR:
    def __init__(self, transition_table, original_grammar, augmented_start_symbol=None):
        self.automata_table: dict = transition_table
        self.original_grammar: dict = original_grammar
        self.non_terminals: set = set(original_grammar.keys())
        self.terminals: set = self.get_terminals()
        # Detección automática del símbolo aumentado si no se provee
        self.augmented_start = augmented_start_symbol or (next(iter(original_grammar))) + "'"
        self.first_follow_table: dict = self.compute_first_follow()
        self.production_numbers = self.number_productions()
        self.action_goto_table: ActionGotoTable = self.build_action_goto_table()
        
    def number_productions(self):
        productions_tuple = []

        for left, productions in self.original_grammar.items():
            for prod in productions:
                print(productions)
                productions_tuple.append((left, prod.split()))  # Ej: ("E", ["E", "+", "T"])

        print(f"producciones: {productions_tuple}")

        numbered_productions = {}
        for i, prod in enumerate(productions_tuple):

            numbered_productions[i + 1] = prod

        print(numbered_productions)

        return numbered_productions
    
    def get_terminals(self):
        terminals = set()

        for productions in self.original_grammar.values():
            for production in productions:

                # dividir por los espacios vacios
                symbols = production.split()
                for symbol in symbols:
                    # si no es un non_ter ni epsilon,es un terminal
                    if symbol not in self.non_terminals and symbol != 'ε':
                        terminals.add(symbol)
        return terminals
    
    def compute_first_follow(self):

        first_follow_table = {}

        # creating the table for the first and follow for each nonterminal
        for non_ter, value in self.original_grammar.items():

            first_follow_table[non_ter] = {'first': set(), 'follow': set()}

        print(self.terminals)
        print(self.non_terminals)

        calculate_first(self.original_grammar, self.terminals, first_follow_table)
        print(first_follow_table)
        calculate_follow(self.original_grammar, first_follow_table, self.non_terminals, self.terminals)
        
        print("\n first follow table result: \n", first_follow_table)

        return first_follow_table

    def build_action_goto_table(self):

        action_goto_table = {}
        # generando la tabla
        for state in self.automata_table.keys():
            state_number = state.replace("I","")
            action_goto_table[state_number] = { "action": {}, "goto": {}}

            for terminal in self.terminals:
                action_goto_table[state_number]["action"][terminal] = ""
            
            # el simbolo $ no es un no terminal original de la gramatica pero es necesario para el parsing
            action_goto_table[state_number]["action"]["$"] = ""
                
            for non_terminal in self.non_terminals:
                action_goto_table[state_number]["goto"][non_terminal] = ""
        
        
        # haciendo el goto

        #por cada estado
        for state in self.automata_table.keys():

            state_number = state.replace("I","")
            state_transitions = self.get_state_transitions(state)

            #ver todas las transiciones
            for transition_symbol, next_state in state_transitions.items():

                # si el simbolo de transicion es no terminal
                if transition_symbol in self.non_terminals:
                    next_state_number = next_state.replace("I","")

                    # la interseccion entre el no terminal y el estado (en goto) es el numero del siguiente estado
                    action_goto_table[state_number]["goto"][transition_symbol] = next_state_number
        

        # llenar las acciones (shift/accept/reduce) 
        for state_name, state_data in self.automata_table.items():
            state_num = state_name.replace("I", "")
            
            #SHIFT (para terminales)
            for terminal, target_state in state_data["transitions"].items():
                if terminal in self.terminals:  
                    target_num = target_state.replace("I", "")
                    action_goto_table[state_num]["action"][terminal] = f"s{target_num}"

           #ACCEPT (ítem E' → E·)
            for item in state_data["items"]:
                if item["left"] == self.augmented_start and item["dot"] == len(item["prod"]):  # E' → E·
                    action_goto_table[state_num]["action"]["$"] = "acc"
                    break  # Solo hay un ítem E' → E· por estado

            #REDUCE (para ítems con punto al final, excluyendo E')
            for item in state_data["items"]:
                if item["dot"] == len(item["prod"]) and item["left"] != self.augmented_start:
                    left_symbol = item["left"]
                    production = (left_symbol, item["prod"])
                    
                    # Buscar el numero de la producción
                    prod_num = next(
                        (num for num, prod in self.production_numbers.items() if prod == production),
                        None
                    )
                    if prod_num is not None:
                        for terminal in self.first_follow_table[left_symbol]["follow"]:
                            current_action = action_goto_table[state_num]["action"][terminal]
                            new_action = f"r{prod_num}"
                            
                            if current_action == "":
                                action_goto_table[state_num]["action"][terminal] = new_action
                            else:
                                # Detección del tipo de conflicto
                                if current_action.startswith('s') and new_action.startswith('r'):
                                    conflict_type = "Shift-Reduce"
                                elif current_action.startswith('r') and new_action.startswith('r'):
                                    conflict_type = "Reduce-Reduce"
                                else:
                                    conflict_type = "Conflicto desconocido"
                                
                                print(f"\n❌ {conflict_type} en state {state_num}, terminal '{terminal}':")
                                print(f" - Acción existente: {current_action}")
                                print(f" - Nueva acción: {new_action}")
                                print(f" - Producción en conflicto: {left_symbol} -> {' '.join(item['prod'])}")
        #print(action_goto_table)

        return ActionGotoTable(action_goto_table)
    
    #Modulo 5
    def LR_parsing(self, token_iterator, lex_dict):
        stack = [0]  # Pila de estados
        token_buffer = []
        
        # Función para obtener el siguiente token
        def get_next_token():
            if token_buffer:
                return token_buffer.pop(0)
            try:
                token = next(token_iterator)
                simple_token = lex_dict.get(token["TokenName"])
                return simple_token
            except StopIteration:
                return '$'  # Fin de entrada
        
        current_token = get_next_token()
        
        print(f"Iniciando parsing con primer token: {current_token}")
        print(f"Estado inicial de la pila: {stack}")
        
        while True:
            current_state = str(stack[-1])
            print(f"\nEstado actual: {current_state}, Token actual: {current_token}")
            print(f"Pila: {stack}")
            
            try:
                action = self.action_goto_table.Action(current_state, current_token)
                print(f"Acción encontrada: {action}")
                
                if action == "":
                    print(f"Error sintáctico: No hay acción definida para estado {current_state} y token '{current_token}'")
                    return False
                    
            except Exception as e:
                print(f"Error al buscar acción: {e}")
                return False
            
            if action == "acc":
                print("Parsing completado exitosamente (ACCEPT)")
                return True
                
            elif action.startswith('s'):
                new_state = int(action[1:])
                stack.append(new_state)
                current_token = get_next_token()
                print(f"SHIFT: Moviendo a estado {new_state}, avanzando token")
                
            elif action.startswith('r'):
                production_num = int(action[1:])
                
                if production_num not in self.production_numbers:
                    print(f"Error: Producción {production_num} no encontrada")
                    return False
                
                left_symbol, right_symbols = self.production_numbers[production_num]
                production_length = len(right_symbols)
                
                print(f"REDUCE: Aplicando producción {production_num}: {left_symbol} -> {' '.join(right_symbols)}")
                
                for _ in range(production_length):
                    if len(stack) <= 1:
                        print(f"Error: Intento de hacer pop en pila vacía")
                        return False
                    stack.pop()
                
                current_state_after_reduce = str(stack[-1])
                
                try:
                    goto_state = self.action_goto_table.Goto(current_state_after_reduce, left_symbol)
                    print(f"GOTO: Desde estado {current_state_after_reduce} con {left_symbol} -> estado {goto_state}")
                    
                    if goto_state == "":
                        print(f"Error sintáctico: No hay GOTO definido para estado {current_state_after_reduce} y no terminal '{left_symbol}'")
                        return False
                    
                    stack.append(int(goto_state))
                    
                except Exception as e:
                    print(f"Error al buscar GOTO: {e}")
                    return False
            
            else:
                print(f"Error: Acción desconocida '{action}'")
                return False

    #Obtiene las transiciones para un estado dado del autómata.
    def get_state_transitions(self, state):
        return self.automata_table[state]["transitions"]

    #Obtiene las producciones para un estado dado del autómata.
    def get_state_items(self, state):
        return self.automata_table[state]["items"]

    #Obtiene el conjunto FIRST para un simbolo gramatical.
    def get_first_set(self, symbol):
        return self.first_follow_table[symbol]["first"]

    #Obtiene el conjunto FOLLOW para un simbolo gramatical.
    def get_follow_set(self, symbol):
        return self.first_follow_table[symbol]["follow"]

    def visualize_automaton(self, filename="automata_lr0", format="png", view=True):
        try:
            from graphviz import Digraph
        except ImportError:
            print("Error: Graphviz no está instalado. Ejecuta: pip install graphviz")
            return None
        
        # Crear el grafo dirigido
        dot = Digraph(comment='Autómata LR(0)')
        dot.attr(rankdir='TB')  # Dirección de arriba hacia abajo
        dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightblue')
        dot.attr('edge', fontsize='10')
        
        # Agregar nodos (estados)
        for state_name, state_data in self.automata_table.items():
            # Crear etiqueta del estado con sus ítems
            label = self._create_state_label(state_name, state_data['items'])
            
            # Determinar el color del nodo según el tipo de estado
            node_color = self._get_node_color(state_data['items'])
            
            dot.node(state_name, label=label, fillcolor=node_color)
        
        # Agregar aristas (transiciones)
        for state_name, state_data in self.automata_table.items():
            for symbol, target_state in state_data['transitions'].items():
                # Determinar el color de la arista según el tipo de símbolo
                edge_color = 'blue' if symbol in self.non_terminals else 'red'
                edge_style = 'bold' if symbol in self.non_terminals else 'solid'
                
                dot.edge(state_name, target_state, 
                        label=symbol, 
                        color=edge_color,
                        style=edge_style)
        
        # Agregar nodo inicial invisible para mostrar el estado inicial
        dot.node('start', style='invisible')
        dot.edge('start', 'I0', style='bold', color='green')
        
        # Generar el archivo
        try:
            output_path = dot.render(filename, format=format, cleanup=True)
            print(f"✅ Autómata generado exitosamente: {output_path}")
            
            if view:
                dot.view()
                
            return output_path
            
        except Exception as e:
            print(f"Error al generar el archivo: {e}")
            return None
    
    def _create_state_label(self, state_name, items):
        # Comenzar la tabla HTML
        label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        
        # Encabezado del estado
        label += f'<TR><TD BGCOLOR="darkblue" COLSPAN="1">'
        label += f'<FONT COLOR="white"><B>{state_name}</B></FONT></TD></TR>'
        
        # Agregar cada ítem
        for item in items:
            item_str = self._format_item(item)
            label += f'<TR><TD ALIGN="LEFT">{item_str}</TD></TR>'
        
        label += '</TABLE>>'
        return label
    
    def _format_item(self, item):
        left = item['left']
        prod = item['prod'].copy()
        dot_pos = item['dot']
        
        # Insertar el punto en la posición correcta
        if dot_pos < len(prod):
            prod.insert(dot_pos, '•')
        else:
            prod.append('•')
        
        # Crear la cadena del ítem
        right_side = ' '.join(prod)
        return f"{left} → {right_side}"
    
    def _get_node_color(self, items):
        # Verificar si hay ítem de aceptación (E' → E•)
        for item in items:
            if item['left'] == "E'" and item['dot'] == len(item['prod']):
                return 'lightgreen'  # Estado de aceptación
        
        # Verificar si hay ítems de reducción (punto al final)
        has_reduce = any(item['dot'] == len(item['prod']) and item['left'] != "E'" 
                        for item in items)
        
        # Verificar si hay ítems de desplazamiento (punto no al final)
        has_shift = any(item['dot'] < len(item['prod']) for item in items)
        
        if has_reduce and has_shift:
            return 'orange'      # Estado con conflicto shift-reduce
        elif has_reduce:
            return 'lightcoral'  # Estado de reducción
        else:
            return 'lightblue'   # Estado de desplazamiento
    
    def print_automaton_info(self):
        """
        Imprime información detallada del autómata en la consola.
        """
        print("INFORMACIÓN DEL AUTÓMATA LR(0)")
        print("=" * 50)
        
        total_states = len(self.automata_table)
        total_transitions = sum(len(state['transitions']) for state in self.automata_table.values())
        
        print(f"Total de estados: {total_states}")
        print(f"Total de transiciones: {total_transitions}")
        print(f"No terminales: {self.non_terminals}")
        print(f"Terminales: {self.terminals}")
        
        print("\nESTADOS DETALLADOS:")
        for state_name, state_data in self.automata_table.items():
            print(f"\n🔹 {state_name}:")
            
            # Mostrar ítems
            print("  Ítems:")
            for item in state_data['items']:
                formatted_item = self._format_item(item)
                print(f"    {formatted_item}")
            
            # Mostrar transiciones
            if state_data['transitions']:
                print("  Transiciones:")
                for symbol, target in state_data['transitions'].items():
                    symbol_type = "NT" if symbol in self.non_terminals else "T"
                    print(f"    {symbol} ({symbol_type}) → {target}")
            else:
                print("  Sin transiciones")
