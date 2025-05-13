### grammar_example.json 

Debe de ser el output del modulo 1, el que toma los yalp y los convierte en un json.

Prácticamente es un diccionario donde la llave es el no terminal a la izquierda y las producciones son una lista. EL ejemplo representa el yalp 1.

E → E + T | T 
T → T ∗ F | F 
F → ( E ) | id

output:
{
  "E": ["E + T", "T"],
  "T": ["T * F", "F"],
  "F": ["( E )", "id"]
}


Este archivo debe ser usado por el modulo 1.5 y el 4.

### augmented_grammar.json
Es el output del algoritmo 1.5 opara au,emtar la gramática.

"left", indica el no terminal a la izquierda de la producción

El número 0 en cada producción representa la posición inicial del punto (ej: E → ·E + T)

dot indica a la izquierda de que caracter de la producción se encuentra. 

si es 2 en "dot" con "left": "E" y "prod": ["E", "+", "T"], entonces la producción es el item:

E → E + .T (dot = 2, se traduce como "el punto está a la izquierda del simbolo en la posicion 2")

si es 3 en dot con "prod": ["E", "+", "T"], sería E → E + T. (el indice es mayor a los indices de los elementos entonces quiere decir que el punto está hasta el final)

Importante notar que los simbolos gramaticales de la producción son una lista para que dot represente la posición exacta del punto a la izquierda del i-ésimo símbolo gramátical en la predicción.

Estructura:
[
  { "left": "E'", "prod": ["E"], "dot": 0 },     // E' → ·E
  { "left": "E", "prod": ["E", "+", "T"], "dot": 0 },  // E → ·E + T
  { "left": "E", "prod": ["T"], "dot": 0 },      // E → ·T
  { "left": "T", "prod": ["T", "*", "F"], "dot": 0 },  // T → ·T * F
  { "left": "T", "prod": ["F"], "dot": 0 },      // T → ·F
  { "left": "F", "prod": ["(", "E", ")"], "dot": 0 },  // F → ·( E )
  { "left": "F", "prod": ["id"], "dot": 0 }      // F → ·id
]

Para todos los items, el punto comienza a la izquierda.

Este archivo debe ser usado por el modulo 2.

### automata_table_Example.json
Es el output del modulo 2.

Un formato similar al de la gramática aumentada. Con la diferencia de que esta será la tabla de transición del automata LR0. Casa estado I_n tiene su diccionario de items canonicos. Manteniendo la estructura de antes ya que acceder a la posición será útil para la construcción de la tabla. Y también su diccionario de transiciones. Left es el no terminal a la izquierda, prod la producción y dot la posición del punto a la izquierda de un indice.

{
  "I0": {
    "items": [
      { "left": "E'", "prod": ["E"], "dot": 0 },
      { "left": "E", "prod": ["E", "+", "T"], "dot": 0 },
      { "left": "E", "prod": ["T"], "dot": 0 },
      { "left": "T", "prod": ["T", "*", "F"], "dot": 0 },
      { "left": "T", "prod": ["F"], "dot": 0 },
      { "left": "F", "prod": ["(", "E", ")"], "dot": 0 },
      { "left": "F", "prod": ["id"], "dot": 0 }
    ],
    "transitions": { "E": "I1", "T": "I2", "F": "I3", "(": "I4", "id": "I5" }
  },
  "I1": {
    "items": [
      { "left": "E'", "prod": ["E"], "dot": 1 },
      { "left": "E", "prod": ["E", "+", "T"], "dot": 1 }
    ],
    "transitions": { "+": "I6" }
  },
  "I2": {
    "items": [
      { "left": "E", "prod": ["T"], "dot": 1 },
      { "left": "T", "prod": ["T", "*", "F"], "dot": 1 }
    ],
    "transitions": { "*": "I7" }
  },
  ...
}


Este archivo debe ser usado por el modulo 3.

### ActionGotoTableExample.json
Este es el output del modulo 4 La tabla de análisis sintáctico LR(0) resultante es un diccionario donde cada clave representa un estado del autómata (ej: "0", "1", etc.). Cada estado contiene dos secciones clave:

{
    "0": {
        "action":{
            "id":"s5",
            "+":"",
            "*":"",
            "(":"s4",
            ")":"",
            "$":""
        },
        "goto":{
            "E":"1",
            "T":"2",
            "F":"3"
        }
    },
    "1": {
        "action":{
            "id":"",
            "+":"s6",
            "*":"",
            "(":"",
            ")":"",
            "$":"acc"
        },
        "goto":{
            "E":"",
            "T":"",
            "F":""
        }
    },
    "2": {
        "action":{
            "id":"",
            "+":"r2",
            "*":"s7",
            "(":"",
            ")":"r2",
            "$":"r2"
        },
        "goto":{
            "E":"",
            "T":"",
            "F":""
        }
    },
}

Esta tabla será parte del objeto ActionGotoTable:

```
class ActionGotoTable():
    def __init__(self, table_dict):
        self.table = table_dict
    def Action(self, State: str, Terminal: str) -> str:
    
    def Goto(self, State: str, NonTerminal: str) -> int:
```

La método tendrá su función Actio ny Goto para Obtener los valores. Por fines de simplicidad el estado es un string y el contenido de la tabla también. Estoe es por que los elementos dentro de la tabla son operaciones de reducción y desplasamiento que se escriben de la isguiente forma:

1. action: Define las acciones para terminales (tokens de entrada).
    * sN: Shift (desplazar) al estado N.
    * rM: Reduce (reducir) usando la producción M (numerada según la gramática).
    * acc: Aceptación (si el token es $ y se completó la gramática).
    * "": Error (celda vacía indica conflicto o situación inválida).

2. goto: Indica transiciones para no terminales después de una reducción.
    * "N": Saltar al estado N tras reducir a ese no terminal.
    * "": No aplicable (ej: si no hay transición posible).

Este archivo debe ser usado por el modulo 5.