from AutomataLR import AutomataLR
import json
grammar = {}
transition_table = {}
with open('./output/grammar_example.json', 'r', encoding='utf-8') as file:
    grammar = json.load(file)
with open('./output/automata_table_Example.json', 'r') as file:
    transition_table = json.load(file)

print(grammar)
print(transition_table)
Automata = AutomataLR(transition_table, grammar)

