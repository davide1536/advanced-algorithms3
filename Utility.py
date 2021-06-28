import numpy as np
from Nodo import *
from Grafo import *
from tabulate import tabulate
import math




def getPesoTaglio(g):
    matrix = np.array(g.adj_matrix)
    c_matrix = matrix[1:,1:]
    indices = np.nonzero(c_matrix)
    #print ("numero di elementi diversi da zero: ",np.count_nonzero(c_matrix))
    #print("i nodi rimasti sono:", indices[0][0]+1, "e ", indices[0][1]+1)
    #print(c_matrix [indices[0][0], indices[0][1]])
    return c_matrix [indices[0][0], indices[0][1]]



def binarySearch(c, low, high, element, avg):
    if high >= low:
        mid = (high + low) // 2
        # print("indice medio:", mid)
        # print("elemento medio:", c[mid])
        # print("elemento dopo:", c[mid+1])
        # print("\n")

        if (element < c[low] and c[low] != 0):
            #print("il primo!")
            return low
        
        # if element == c[high]:
        #     return high

        if mid < len(c)-1:
            if ((c[mid] <= element and c[mid+1] > element) or (c[mid] < element and c[mid+1] >= element)):
                #print("elementi trovati binary:", c[mid], c[mid+1])
                return mid + 1 
        
            elif c[mid] > element:
                #print("elemento maggiore o uguale")
                return binarySearch(c, low, mid-1, element, avg)

            elif c[mid]< element:

                #print("elemento minore ")
                return binarySearch(c, mid+1, high, element, avg)
            
            elif c[mid] == element:
                #print("MEDIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                if element < avg:
                    return binarySearch(c, mid+1, high, element, avg)
                else:
                    return binarySearch(c, low, mid-1, element, avg)

        else:
            return mid

    else:
        return -1



def print_m(matrix_old):
    matrix = []
    matrix[:] = matrix_old
    for i in range(len(matrix)):
        matrix[i][0] = i
    tabella = []
    for i in range(1, len(matrix)):
        tabella.append(matrix[i])

    print()
    print(tabulate(tabella, headers= [str(i) for i in range(1, len(matrix))], tablefmt='grid'))




################################## Funzioni di Test ##################################


def checkWeight(ksWeights, swWeights, lista_grafi):
    for i in range(len(ksWeights)):
        ksPeso = ksWeights[i]
        swPeso = swWeights[i]
        for nodo in lista_grafi[i].getListaNodi():
           
            if ((ksPeso > nodo.d) or (swPeso > nodo.d)):
                print("peso karger and stein", ksPeso, "peso stoer and wagner", swPeso)
                print(lista_grafi[i].n_nodi)
                print(nodo.d)
                exit("il peso trovato ha un valore maggiore rispetto ad uno dei gradi pesati")
    
    return 1



def test_tot_pesi(prim, kruskal, kruskal_naive):
    i = 0
    while i < len(prim):
        res = prim[i].totPeso == kruskal[i].totPeso == kruskal_naive[i].totPeso
        if not res:
            return False
        i+=1
    print("Tutti i grafi risultanti hanno peso uguale")
    return True



def measureProbability(graphs_groupped, kargerAndStein):
    dimensions = []
    realValue = [3056,1526, 2137,1282, 969, 341,951, 484,346, 1137, 676, 508, 400, 43]
    data = [0]*len(realValue)

    for key in graphs_groupped.keys():
        dimensions.append(key)

    j = 0
    while j < 500:
        for i,graphs in enumerate(graphs_groupped):
            k = round(math.log(graphs[0].n_nodi)**2)
            res = kargerAndStein(graphs[0],k)
            if res[0] != realValue[i]:
                data[i] += 1
        j += 1
    
    return data, dimensions

################################## Funzioni Risultati ##################################
    

#funzione di output
def tot_risultati(lista_grafi, res_stoer_wagner, res_karger_stain):
    
    #calcolo l'errore
    errore = []
    for i in range(len(lista_grafi)-40):
        #(soluzione_trovata - soluzione_ottima)/soluzione_ottima
        errore.append(round((res_karger_stain[i] - res_stoer_wagner[i])/res_stoer_wagner[i],3))
    
    table = []
    table.append([grafo.nome for grafo in lista_grafi])         #table[0]
    table.append(res_stoer_wagner)                              #table[1]
    table.append(res_karger_stain)                              #table[2]
    table.append(errore)


    res_table = []
    for i in range(len(lista_grafi)):
        res_table.append([table[0][i], table[1][i], table[2][i], table[3][i]])

    print()
    print(tabulate(res_table, headers= ["nome grafo", "stoer_wagner", "karger_stain", "errore"], tablefmt='pretty'))

 
    








