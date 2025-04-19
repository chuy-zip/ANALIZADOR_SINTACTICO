class ActionGotoTable():
    def __init__(self, table_dict):
        self.table = table_dict

    def Action(self, State: int, Terminal: str) -> str:
        table = self.table
        
        print(f"\nSearching Action on table with state '{State}' for Terminal '{Terminal}'")

        result = table[State]["action"][Terminal]
        res1 = f"There is no action with the pair ({State},{Terminal})" if result == "" else f"The corresponding value to the pair ({State},{Terminal}) is {result}"
        
        print(res1)

        return result
    
    def Goto(self, State: int, NonTerminal: str) -> int:

        table = self.table

        print(f"\nSearching Action on table with state '{State}' for NonTerminal '{NonTerminal}'")

        result = table[State]["goto"][NonTerminal]
        res1 = f"There is no goto with the pair ({State},{NonTerminal})" if result == "" else f"The corresponding value to the pair ({State},{NonTerminal}) is {result}"
        
        print(res1)

        return result