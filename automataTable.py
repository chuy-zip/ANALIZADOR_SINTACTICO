import json
import os
from copy import deepcopy


def closure(items, productions):
    '''
    items: set of tuples (left, tuple(prod), dot)
    productions: dict left -> list of prod lists
    '''
    closure_set = set(items)
    added = True
    while added:
        added = False
        for (A, prod, dot) in list(closure_set):
            # if dot before a nonterminal B
            if dot < len(prod):
                B = prod[dot]
                if B in productions:
                    for gamma in productions[B]:
                        item = (B, tuple(gamma), 0)
                        if item not in closure_set:
                            closure_set.add(item)
                            added = True
    return closure_set


def goto(items, X, productions):
    '''Compute GOTO on item set'''
    moved = set()
    for (A, prod, dot) in items:
        if dot < len(prod) and prod[dot] == X:
            moved.add((A, prod, dot+1))
    return closure(moved, productions) if moved else set()


def items_collection(augmented_items, productions):
    '''Build canonical collection of LR(0) item sets.'''
    # productions: dict left -> list of prod lists
    C = []
    C_map = {}
    # initial item: the augmented production is first in list
    start_item = augmented_items[0]
    I0 = closure({(start_item['left'], tuple(start_item['prod']), 0)}, productions)
    C.append(I0)
    C_map[frozenset(I0)] = 'I0'

    transitions = {}
    idx = 0
    while idx < len(C):
        I = C[idx]
        state_name = C_map[frozenset(I)]
        transitions[state_name] = {}
        # consider all grammar symbols appearing after dot
        symbols = set()
        for (A, prod, dot) in I:
            if dot < len(prod):
                symbols.add(prod[dot])
        for X in symbols:
            J = goto(I, X, productions)
            if J:
                key = frozenset(J)
                if key not in C_map:
                    C_map[key] = f'I{len(C)}'
                    C.append(J)
                transitions[state_name][X] = C_map[key]
        idx += 1
    # format output
    result = {}
    for key, state in C_map.items():
        items = []
        for (A, prod, dot) in key:
            items.append({'left': A, 'prod': list(prod), 'dot': dot})
        result[state] = {
            'items': sorted(items, key=lambda x: (x['left'], x['dot'], x['prod'])),
            'transitions': transitions.get(state, {})
        }
    return result

if __name__ == '__main__':
    # expects argument: path to augmented_grammar.json
    import sys
    if len(sys.argv) != 2:
        print('Usage: python automataTable.py real_output/augmented_grammar.json')
        sys.exit(1)
    aug_path = sys.argv[1]
    with open(aug_path, 'r', encoding='utf-8') as f:
        augmented = json.load(f)
    # build productions dict
    productions = {}
    for item in augmented:
        left = item['left']
        prod = item['prod']
        productions.setdefault(left, []).append(prod)
    # build automaton
    C = items_collection(augmented, productions)
    # write to real_output/automaton.json
    out_dir = os.path.dirname(aug_path)
    out_file = os.path.join(out_dir, 'automaton.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(C, f, ensure_ascii=False, indent=2)
    print(f'Automaton written to {out_file}')