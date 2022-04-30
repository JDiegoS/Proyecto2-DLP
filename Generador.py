# Juan Diego Solorzano 18151
# Proyecto 1 Automatas

from PySimpleAutomata import automata_IO
import os
import json
from Node import Node
from AFN import AFN
from Subconjuntos import Subconjuntos

from Node import Node
class Generador(object):
    # Clase para construir AFN

    def __init__(self, tokens, keywords, characters):
        self.tokens = tokens
        self.keywords = keywords
        self.characters = characters
        self.operaciones = ['(', ')', '|', '{', '}']
        self.expressions = []

        os.environ["PATH"] += os.pathsep + 'C:/Program Files/graphviz/bin'

        print("Analizando la gramatica...")
        self.analizeGrammar()

        # Verificar que se cierren los parentesis y kleene
        for i in self.expressions:
            arr = list(i)
            if arr.count('(') != arr.count(')') or arr.count('{') != arr.count('}'):
                print('Esa expresion no es valida')
                quit()

        # Construir AFN
        alphabetfinal = []
        graph = {
            "alphabet": alphabetfinal,
            "states": [],
            "initial_states": "0",
            "accepting_states": [],
            "transitions": [],
        }
        print(self.expressions)
        for i in self.expressions:
            currentAlphabet = []
            for j in i:
                if j not in self.operaciones:
                    currentAlphabet.append(j)
                    if j not in alphabetfinal:
                        alphabetfinal.append(j)
            self.generateAFN(list(i), currentAlphabet, graph)

        print("Generando AFN (Thompson)...")
        self.graphAFN(graph)
        afd = self.generateAFD(graph, alphabetfinal)

        self.simulateA(afd)


    def analizeGrammar(self):
        # En cada token, convertir ids de caracteres a sus alfabetos
        finalExpression = []
        for i in self.tokens:
            currentToken = i.value
            currentToken = currentToken.replace('"', '')
            nextIndex = 0
            for j in self.characters:
                nextIndex +=1
                goNext = False
                # Buscar si el id del caracter se encuentra en el token
                character = currentToken.find(j.id)
                if character != -1:
                    for c in self.characters[nextIndex:]:
                        # Verificar que se este usando el caracter correcto (problemas como digito y digitoHex)
                        if currentToken.find(c.id) == character:
                            goNext = True
                    if goNext:
                        goNext = False
                        continue
                    currentAlphabet = '('
                    if len(j.alphabet) == 1:
                        currentAlphabet = j.alphabet[0]
                    else:
                        currentAlphabet = (currentAlphabet * (len(j.alphabet)-1)) + j.alphabet[0]
                        for a in j.alphabet[1:]:
                            # Agregar OR para cada valor del alfabeto
                            currentAlphabet += '|' + a + ')'
                    # Reemplazar el id del caracter por su alfabeto
                    currentToken = currentToken.replace(j.id, currentAlphabet)
                
            # Agregar expresion al arreglo final
            finalExpression.append(currentToken)
        self.expressions = finalExpression
        print(self.expressions)
            

    def generateAFN(self, arr, alphabet, graph):
        # Crear AFN en base al alfabeto
        afn = AFN(arr, alphabet)
        afn_nodes = afn.generateAFN()

        if graph['states'] == []:
            nextIndex = 1
        else:
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
        # Crear grafica del AFN
        with open('digraph.json', 'w') as outfile:
            json.dump(graph, outfile)
        dfa_example = automata_IO.nfa_json_importer('./digraph.json')
        automata_IO.nfa_to_dot(dfa_example, 'thompsonAFN', './')

    def generateAFD(self, graph, alphabet):
        # Crear y graficar AFD
        print("Generando AFD (Construccion de subconjuntos)...")
        afd_sub = Subconjuntos(graph['states'], graph['transitions'], alphabet, graph['accepting_states'])
        print('pol')
        afd_snodes = afd_sub.generateAFD()
        graph2 = {
            "alphabet": alphabet,
            "states": [],
            "initial_state": "s0",
            "accepting_states": [],
            "transitions": [],
        }
        print('pol2')

        for i in afd_snodes:
            if i.state not in graph2['states']:
                graph2['states'].append(str(i.state))
                if i.accepted == True:
                    graph2['accepting_states'].append(str(i.state))
                for t in i.transitions:
                    graph2['transitions'].append([str(t[0]), t[1], str(i.state)])

        # Graficar tarda mucho
        '''
        with open('digraph2.json', 'w') as outfile:
            json.dump(graph2, outfile)
        dfa_example = automata_IO.dfa_json_importer('./digraph2.json')
        automata_IO.dfa_to_dot(dfa_example, 'subconjuntosAFD', './')
        '''
        return graph2

    def simulateA(self, graph):
        # Simular AFD
        opc = input('\nIngrese una cadena para evaluar (q para salir): ')
        while opc != 'q':
            
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
            

