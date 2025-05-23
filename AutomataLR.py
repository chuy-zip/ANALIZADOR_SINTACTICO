from ActionGotoTable import ActionGotoTable
from first_follow import calculate_first, calculate_follow

class AutomataLR:
    def __init__(self, transition_table, original_grammar):
        self.automata_table: dict = transition_table
        self.original_grammar: dict = original_grammar
        self.non_terminals: set = set(original_grammar.keys())
        self.terminals: set = self.get_terminals()
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
        print("WIP")

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
        print(action_goto_table)

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
                if item["left"] == "E'" and item["dot"] == len(item["prod"]):  # E' → E·
                    action_goto_table[state_num]["action"]["$"] = "acc"
                    break  # Solo hay un ítem E' → E· por estado

            #REDUCE (para ítems con punto al final, excluyendo E')
            for item in state_data["items"]:
                if item["dot"] == len(item["prod"]) and item["left"] != "E'":
                    left_symbol = item["left"]
                    production = (left_symbol, item["prod"])
                    
                    # Buscar el numero de la prod
                    prod_num = next(
                        (num for num, prod in self.production_numbers.items() if prod == production),
                        None
                    )
                    if prod_num is not None:
                        for terminal in self.first_follow_table[left_symbol]["follow"]:
                            if action_goto_table[state_num]["action"][terminal] == "":
                                action_goto_table[state_num]["action"][terminal] = f"r{prod_num}"
                            else:
                                print(f"Conflicto en state {state_num}, terminal {terminal}: {action_goto_table[state_num]['action'][terminal]} vs r{prod_num}")
            print("Tabla ACTION/GOTO completada:")
            print(action_goto_table)

        return action_goto_table
    
    #Modulo 5
    def LR_parsing(self, tokenlist):
        #usa la lista de tokens y la tablaActionGoto para hacer el parsing
        pass

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