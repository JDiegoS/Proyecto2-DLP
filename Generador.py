# Juan Diego Solorzano 18151
# Proyecto 1 Automatas

from PySimpleAutomata import automata_IO
import os
import json
from Node import Node
from AFN import AFN
from Subconjuntos import Subconjuntos

from Node import Node
class AFN(object):
    # Clase para construir AFN

    def __init__(self, tokens, keywords, characters):
        self.tokens = tokens
        self.keywords = keywords
        self.characters = characters
        self.operaciones = ['(', ')', '|', '{', '}']

        os.environ["PATH"] += os.pathsep + 'C:/Program Files/graphviz/bin'

        expresion = input("\nIngrese la expresion regular: ")
        expresion2 = input("\nIngrese la expresion regular: ")
        print("Analizando expresion...")

        arr = list(expresion)
        if arr.count('(') != arr.count(')') or arr.count('{') != arr.count('}'):
            print('Esa expresion no es valida')
            quit()
        alphabet = []
        for i in arr:
            if i not in self.operaciones and i not in alphabet:
                alphabet.append(i)

        arr2 = list(expresion2)
        if arr2.count('(') != arr2.count(')') or arr2.count('{') != arr2.count('}'):
            print('Esa expresion no es valida')
            quit()
        alphabet2 = []
        for i in arr2:
            if i not in self.operaciones and i not in alphabet2:
                alphabet2.append(i)

        # Construir AFN
        print("Generando AFN (Thompson)...")

        alphabetfinal = alphabet + alphabet2
        graph = {
            "alphabet": alphabetfinal,
            "states": [],
            "initial_states": "0",
            "accepting_states": [],
            "transitions": [],
        }

        self.generateAFN(arr, alphabet, graph)
        self.generateAFN(arr2, alphabet2, graph)
        self.graphAFN(graph)
        self.generateAFD(alphabetfinal, graph)

    def generateAFN(self, arr, alphabet, graph):
        afn = AFN(arr, alphabet)
        afn_nodes = afn.generateAFN()

        nextIndex = int(graph['states'][-1]) + 1
        graph['transitions'].append(['0', 'epsilon', str(int(afn_nodes[0].state) + nextIndex)])
        for i in afn_nodes:
            if str(int(i.state) + nextIndex) not in graph['states']:
                graph['states'].append(str(int(i.state) + nextIndex))
                if i.accepted == True:
                    graph['accepting_states'].append(str(int(i.state) + nextIndex))
                for t in i.transitions:
                    graph['transitions'].append([str(int(t[0]) + nextIndex), t[1], str(int(i.state) + nextIndex)])

    
    def graphAFN(self, graph):
        with open('digraph.json', 'w') as outfile:
            json.dump(graph, outfile)
        dfa_example = automata_IO.nfa_json_importer('./digraph.json')
        automata_IO.nfa_to_dot(dfa_example, 'thompsonAFN', './')

    def generateAFD(self, graph, alphabet):
        print("Generando AFD (Construccion de subconjuntos)...")
        afd_sub = Subconjuntos(graph['states'], graph['transitions'], alphabet, graph['accepting_states'])
        afd_snodes = afd_sub.generateAFD()
        graph2 = {
            "alphabet": alphabet,
            "states": [],
            "initial_state": "s0",
            "accepting_states": [],
            "transitions": [],
        }
        for i in afd_snodes:
            if i.state not in graph2['states']:
                graph2['states'].append(str(i.state))
                if i.accepted == True:
                    graph2['accepting_states'].append(str(i.state))
                for t in i.transitions:
                    graph2['transitions'].append([str(t[0]), t[1], str(i.state)])

        with open('digraph2.json', 'w') as outfile:
            json.dump(graph2, outfile)
        dfa_example = automata_IO.dfa_json_importer('./digraph2.json')
        automata_IO.dfa_to_dot(dfa_example, 'subconjuntosAFD', './')

    def simulateA(self, graph):
        opc = input('\nIngrese una cadena para evaluar (0 para salir): ')
        while opc != '0':
            
            cadena = list(opc)
            if len(cadena) == 0:
                if 's0' in graph['accepting_states']:
                    print('SI CON SUBCONJUNTOS')
                else:
                    print("NO CON SUBCONJUNTOS")
            else:
                s = 's0'
                c = cadena[0]
                i = 0
                cadena.append('eof')
                while (c != 'eof'):
                    cambio = False
                    # Mover(s,c)
                    for j in graph['transitions']:
                        if j[0] == s and j[1] == c:
                            s = j[2]
                            cambio = True
                            print(s)
                            break
                    if cambio == False:
                        break
                    # Siguiente caracter
                    i+=1
                    c = cadena[i]
                if (s in graph['accepting_states'] and cambio):
                    print('SI CON SUBCONJUNTOS')
                else:
                    print("NO CON SUBCONJUNTOS")
            
            opc = input('\nIngrese una cadena para evaluar (0 para salir): ')
            

