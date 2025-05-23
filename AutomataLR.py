from ActionGotoTable import ActionGotoTable
from first_follow import calculate_first, calculate_follow

class AutomataLR:
    def __init__(self, transition_table, original_grammar):
        self.automata_table: dict = transition_table
        self.original_grammar: dict = original_grammar
        self.non_terminals: set = set(original_grammar.keys())
        self.terminals: set = self.get_terminals()
        self.first_follow_table: dict = self.compute_first_follow()
        self.action_goto_table: ActionGotoTable = self.build_action_goto_table()
    
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

        return
    
    #Modulo 5
    def LR_parsing(self, tokenlist):
        #usa la lista de tokens y la tablaActionGoto para hacer el parsing
        pass

    #Obtiene las transiciones para un estado dado del autómata.
    def get_state_transitions(self, state):
        return self.automata_table[state]["transitions"]

    #Obtiene las producciones para un estado dado del autómata.
    def get_state_items(self, state):
        return self.automata_table[state]["productions"]

    #Obtiene el conjunto FIRST para un simbolo gramatical.
    def get_first_set(self, symbol):
        return self.first_follow_table[symbol]["first"]

    #Obtiene el conjunto FOLLOW para un simbolo gramatical.
    def get_follow_set(self, symbol):
        return self.first_follow_table[symbol]["follow"]