from numpy import insert, square
from numpy.lib.polynomial import roots
from Grafo import Grafo
from Nodo import Nodo
from Arco import Arco
import random
import os
import math
from random import seed
from random import randint
import gc
from time import perf_counter_ns
from collections import defaultdict
import collections
import matplotlib.pyplot as plt
import copy
import time
from Utility import *
from Heap import *
from datetime import datetime

#lista di grafi stoer wagner
res_stoer_wagner = []
#lista grafi karger stain
res_karger_stain = []


#lista dei tempi di stoer wagner
time_stoer_wagner = [] 
#lista dei tempi di karger stain
time_karger_stain = []
discovery_times = []
discovery_iterations = []


directory = "dataset/"
lista_grafi = []



def parsing(directory):
    for file in os.listdir(directory):
            crea_grafi(file)



#funzione che dato un path, aggiunge un oggetto grafo 
#alla lista lista_grafi
def crea_grafi(path):

    global lista_grafi
    g = Grafo()
    id2Node = {}
    lista_nodi = set()
    lista_nodi_obj = []
    lista_archi = []
    lista_adiacenza = {}
    
    
    f = open("dataset/" + path, "r")

    #assegno i valori numero nodi e numero archi
    prima_riga = f.readline().split(" ")
    g.n_nodi = int(prima_riga[0]) 
    g.n_archi = int(prima_riga[1])
    
    #creo lista di stringhe "nodo1, nodo2, peso"
    righe = f.read().splitlines()
    
    #divido le stringhe in liste di 3 valori [nodo1, nodo2, peso]
    lista_valori = []
    for riga in righe:
        lista_valori.append(riga.split())
    f.close()
    
    #inizializzo matrice di adiacenza
    adj_matrix = [[0]*(g.n_nodi+1) for i in range(g.n_nodi+1)]

    #creo il set di nodi e lista archi
    for i in range(0, len(lista_valori)):
        #valori estratti dal file
        nodo_1 = int(lista_valori[i][0])
        nodo_2 = int(lista_valori[i][1])
        peso = int(lista_valori[i][2])
        
        adj_matrix[nodo_1][nodo_2] = peso
        adj_matrix[nodo_2][nodo_1] = peso

        #set di nodi, per evitare i duplicati
        lista_nodi.add(nodo_1)
        lista_nodi.add(nodo_2)
        lista_adiacenza.setdefault(nodo_1, [])    #inzializzo ogni chiave nodo a un valore list
        lista_adiacenza.setdefault(nodo_2, [])    
        
        arco_1 = Arco(nodo_1, nodo_2, peso)
        lista_archi.append(arco_1)

    
    #creo gli oggetti nodo e il dizionario id2Node
    for nodo in lista_nodi:
        obj_nodo = Nodo(nodo)
        id2Node[obj_nodo.id] = obj_nodo
        lista_nodi_obj.append(obj_nodo)

    #riempio le liste di adicenza create in precedenza
    for i in range(0, len(lista_valori)):
        nodo_1 = int(lista_valori[i][0])
        nodo_2 = int(lista_valori[i][1])
        peso = int(lista_valori[i][2])
        lista_adiacenza[nodo_1].append(Arco(nodo_1, nodo_2, peso))      #arco(u,v)
        lista_adiacenza[nodo_2].append(Arco(nodo_2, nodo_1, peso))      #arco(v,u)


    #setto gli attributi dell'arco
    g.nome = path[:-4]
    g.lista_nodi_updated = []
    g.lista_merged = []
    g.merged_matrix = [row[:] for row in adj_matrix]
    g.id2Node = id2Node
    g.lista_archi = lista_archi
    g.lista_nodi_obj = sorted(lista_nodi_obj, key=lambda nodo: (nodo.id))
    g.lista_nodi_id = [n for n in range(1, g.n_nodi+1)]     
    g.adj_matrix = adj_matrix
    g.lista_adiacenza = lista_adiacenza
    g.merged_n_nodi = g.n_nodi
    g.lista_nodi_updated[:] = lista_nodi_obj
    g.lista_merged
    lista_grafi.append(g)




def measure_run_time(n_instances, graphs, algorithm):
    sum_times = 0

    if graphs[0].n_nodi <=20:         #per avere valori più precisi le istanze con un basso numero di nodi vengono ripetute più volte
        iterations = 30
    else:
        iterations = 1
    #liste per confrontare gli algoritmi                          
    # global p_g
    # global k_g
    # global kn_g
    # global sw_t 
    # global ks_t 


    print("testing graph size: ", graphs[0].n_nodi)
    for i in range(n_instances):
        print("istanza numbero: ",i)
        if algorithm == "kargerAndStein":
            gc.disable()
            #nodo_casuale = next(iter(graphs[i].lista_nodi))    #casuale perchè il set lista_nodi cambia ordine ad ogni parsing
            
            start_time = perf_counter_ns()
            m = 0
            while m < iterations:
                #prim(graphs[i],graphs[i].getNodo(nodo_casuale))
                k = round(math.log(graphs[i].n_nodi)**2)
                res = kargerAndStein(graphs[i], k)
                m+=1

            end_time = perf_counter_ns()
            #p_g.append(prim(graphs[i],graphs[i].getNodo(nodo_casuale)).getGrafoPrim())
            discovery_time = res[3]
            discovery_iteration = res[2]

            discovery_times.append(discovery_time)
            discovery_iterations.append(discovery_iteration)
            time_karger_stain.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "storeAndWagner":            
            gc.disable()
            j = 0
            newGrafi = []
            
            for k in range(iterations):
                newGrafi.append(copy.deepcopy(graphs[i]))

            start_time = perf_counter_ns()
            while j < iterations:
                globalMinCut(newGrafi[j])
                j+=1
            end_time = perf_counter_ns()
            #kn_g.append(naiveKruskal(graphs[i]))
            time_stoer_wagner.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        # if algorithm == "Kruskal":
        #     gc.disable()
        #     start_time = perf_counter_ns()
        #     k = 0
        #     while k < iterations:
        #         #kruskal(graphs[i])     
        #         k += 1
        #     end_time = perf_counter_ns()
        #     #k_g.append(kruskal(graphs[i]))
        #     k_t.append(round((end_time - start_time)/iterations//1000, 3))
        #     gc.enable()

        sum_times += (end_time - start_time)/iterations


    avg_time = round((sum_times / n_instances)//1000, 3) #millisecondi

    return avg_time



def measurePerformance():
    graphs_groupped = defaultdict(list)
    
    #raggruppo i grafi in base alla dimensione dei loro nodi con un dizionario key:n_nodi, value: grafi con quel numero di nodi        
    for i in range (len(lista_grafi)):
        graphs_groupped[int(lista_grafi[i].n_nodi)].append(lista_grafi[i])

    #  ghhhh il dizionario in base alla key (numero di nodi)
    graphs_groupped = collections.OrderedDict(sorted(graphs_groupped.items()))
    

    #per calcolare la costante considero ElgV quindi per ogni dimensione di grafo prendo il numero di nodi e la media del numero degli archi
    sizes = []
    arches = 0
    for key in graphs_groupped.keys():
        for g in graphs_groupped[key]:
            arches += g.n_archi
            nodes = g.n_nodi
        avg_arches = arches / len(graphs_groupped[key])
        sizes.append([nodes, avg_arches])
        arches = 0
        nodes = 0

    #algorithmsToTest = ["kargerAndStein","storeAndWagner"]
    algorithmsToTest = ["kargerAndStein","storeAndWagner"]
    totTimes = []
    totRatios = []
    totConstant = []
    for algorithm in algorithmsToTest:
        print("sto testando", algorithm)
        times = [measure_run_time(len(graphs_groupped[key]), graphs_groupped[key], algorithm) for key in graphs_groupped]
        totTimes.append(times)
        ratios = [None] + [round(times[i+1]/times[i],3) for i in range(len(sizes)-1)] 
        totRatios.append(ratios)

        if algorithm == "kargerAndStein":
            totConstant.append([round(times[i]/((sizes[i][0]**2) * math.log(sizes[i][0])**3),3) for i in range(len(sizes))])

        else:
            totConstant.append([round(times[i]/(sizes[i][1] * sizes[i][0] * math.log(sizes[i][0])),3) for i in range(len(sizes))])

    return totTimes, totRatios, totConstant, sizes, graphs_groupped
    


def plot_graph():
    
    #misuro le performance per ogni algoritmo, i valori times, ratios, constant sono matrici di dimensione 4*n n sono il numero di dimensioni dei grafi
    [times, ratios, constant, sizes, graphs_groupped] = measurePerformance()
    algorithmsToTest = ["kargerAndStein","storeAndWagner"]

    for i in range(len(algorithmsToTest)):
        print ("Algoritmo:", algorithmsToTest[i])
        print("Size\t\ttTime(ms)\t\tCostant\t\tRatio")

        print(65*"-")
        for j in range(len(sizes)):
            if j < 10:
                print(sizes[j][0], '' , times[i][j], '', '', constant[i][j], '', ratios[i][j] ,sep="\t")
            else:
                print(sizes[j][0], '', times[i][j], '', constant[i][j], '', ratios[i][j], sep="\t")
        print(65*"-")


    #grafico dei tempi
        reference = []
        print("costante utilizzata per calcolare la reference :", algorithmsToTest[i], " ",constant[i][len(constant[0]) - 1] )
        print("ratio finale per",algorithmsToTest[i],": ", times[i][len(sizes) -1] / times[i][len(sizes) - 3])

        if algorithmsToTest[i] == "kargerAndStein":
            for j in range (len(sizes)):
                reference.append (constant[i][len(constant[0]) - 1] * (sizes[j][0]**2) * math.log(sizes[j][0])**3)
        else:
            for j in range (len(sizes)):
                reference.append (constant[i][len(constant[0]) - 1] * sizes[j][1] * sizes[j][0] * math.log(sizes[j][0]))

        plt.plot(graphs_groupped.keys(), times[i], label = algorithmsToTest[i])
        plt.plot(graphs_groupped.keys(), reference, label="reference")
        plt.legend()
        plt.title("performance " + algorithmsToTest[i])
        plt.ylabel('run time(ns)')
        plt.xlabel('size')
        plt.show()


    plt.plot(graphs_groupped.keys(), times[0], label = 'kargerAndStein')
    plt.plot(graphs_groupped.keys(), times[1],label = 'storeAndWagner')
    plt.legend()
    plt.title("grafici in relazione")
    plt.ylabel('run time(ns)')
    plt.xlabel('size')
    plt.show()

    return graphs_groupped, times


#---------------------------------------------------------------Karger & Stein---------------------------------------------------------------

            

def gradoPesato(g, nodi):
    for u in nodi:
        for peso in g.adj_matrix[u.id][1:]:
            u.d = u.d + peso


def randomSelect(g,c):
    
    r = random.randint(0, c[len(c)-1])

    
    r = random.randint(0, c[len(c)-1])
    avg = sum(c) / len(c)
   
    index = binarySearch(c, 0, len(c)-1, r, avg)
    
    vertex = g.getListaNodi()[index]
    
    return vertex


def edgeSelect(g):
    pesiComulativi = []
    tot = 0

    for u in g.getListaNodi():
        tot = tot + u.d
        pesiComulativi.append(tot)

    u = randomSelect(g,pesiComulativi)
    
    pesiComulativi = []
    tot = 0
    for v in g.getListaNodi():
        tot += g.adj_matrix[u.id][v.id]
        pesiComulativi.append(tot)
        
    v = randomSelect(g,pesiComulativi)


    return u,v, pesiComulativi


def contractEdge(g, edge, c):
    u = edge[0]
    v = edge[1]
    if  g.adj_matrix[u.id][v.id] == 0:
        print("nodo gia selezionato ")
        exit(0)

    u.d = u.d + v.d - (2*g.adj_matrix[u.id][v.id])
    v.d = 0
    g.adj_matrix[u.id][v.id] = 0
    g.adj_matrix[v.id][u.id] = 0
    for i in range(1,len(g.adj_matrix)):
        if (i != u.id and i != v.id):

            g.adj_matrix[u.id][i] = g.adj_matrix[u.id][i] + g.adj_matrix[v.id][i]
            g.adj_matrix[i][u.id] = g.adj_matrix[i][u.id] + g.adj_matrix[i][v.id]
            g.adj_matrix[v.id][i] = 0
            g.adj_matrix[i][v.id] = 0 
    
    g.merged_n_nodi -= 1


def contract(g, k):
    n = g.merged_n_nodi
    for i in range(n-k):
        u,v,c = edgeSelect(g)
        edge = [u,v]
        contractEdge(g, edge, c)
    return g


#funzione che consente di trovare un taglio
def recursiveContract(g):
    w = []
    n = g.merged_n_nodi
    if n <= 6:
        gPrime = contract(g, 2)
        peso = getPesoTaglio(gPrime)
        return peso
        
    t = round(g.merged_n_nodi/math.sqrt(2) + 1)
    
    g1 = contract(g, t)
    g2 = contract(g,t)
    return min(recursiveContract(g1), recursiveContract(g2))


def kargerAndStein(g, k):
    gradoPesato(g, g.getListaNodi())
    minCut = float('inf')
    gMin = Grafo()
    start_time = perf_counter_ns()

    for i in range(k):
        random.seed(datetime.now())
        g2 = copy.deepcopy(g)

        cut = recursiveContract(g2)
        if cut < minCut:
            discoveredIteration = i
            discoveredTime = perf_counter_ns()
            gMin = g2
            minCut = cut

    discoveredTime = discoveredTime - start_time

    return minCut, gMin, discoveredIteration, discoveredTime



#---------------------------------------------------------------Stoer & Wagner---------------------------------------------------------------

#ci riprovo

dict_pesi = {}


#funzione che salva i pesi dei tagli di s_w in un dizionario
def crea_dict(lista_grafi):
    for g in lista_grafi:
        dict_pesi[g.nome] = [0,0]



#funzione utile a calcolare il peso del global min_cut
def calcola_peso_taglio(grafo):
    nodo_merge = grafo.lista_nodi_updated[0]
    sum = 0
    for peso in grafo.adj_matrix[nodo_merge.id]:
        sum += peso
    return sum


def globalMinCut(g):
    
    if g.merged_n_nodi == 2:
        peso_taglio = calcola_peso_taglio(g)
        dict_pesi[g.nome][1] = peso_taglio

        return g

    else:
        g1, s, t = stMinCut(g)
        g2 = globalMinCut(stMerge(g, s, t))

        if(dict_pesi[g.nome][0] <= dict_pesi[g.nome][1]):
            return g1, dict_pesi[g.nome][0]
        else:
            return g2, dict_pesi[g.nome][1]



def stMinCut(g):
    #inizializzo nodi
    index = 0
    for nodo in g.lista_nodi_updated:
        nodo.in_h = 1
        nodo.key = 0
        nodo.heapIndex = index  #per non usare la funzione 'index'
        index += 1
    q = Heap(g.lista_nodi_updated)
    buildMaxHeap(q)
    s = None
    t = None
    while q.heapsize != 0:
        u = heapExtractMax(q)
        s = t
        t = u
        i = -1 #indice per trovare i vicini di u
        for nodo_adj in g.adj_matrix[u.id]:
            i += 1
            if nodo_adj != 0 and i > 0:
                v = g.getNodo(i)
                if isIn(v) == 1:
                    v.key += g.adj_matrix[u.id][v.id]
                    index = v.heapIndex  #ottengo la sua posizione all'interno dell'heap
                    heapIncreaseKey(q, index, v.key)
                    
    #controllo se il nuovo talgio è inferiore a quello già calcolato
    if dict_pesi[g.nome][0] == 0 or t.key < dict_pesi[g.nome][0]:
        dict_pesi[g.nome][0] = t.key
    
    return g, s, t
 


def stMerge(g, s, t):
    
    g.adj_matrix[s.id][t.id] = 0
    g.adj_matrix[t.id][s.id] = 0


    for nodo in g.lista_nodi_updated:
        #utile per il peso del globalMinCut

        g.adj_matrix[s.id][nodo.id] += g.adj_matrix[t.id][nodo.id]
        g.adj_matrix[nodo.id][s.id] += g.adj_matrix[nodo.id][t.id]
        g.adj_matrix[t.id][nodo.id] = 0 
        g.adj_matrix[nodo.id][t.id] = 0

    g.lista_nodi_updated.remove(t)    
    g.merged_n_nodi = g.merged_n_nodi - 1

    return g






######################## MAIN ########################

print("-"*50)
parsing(directory)

#lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.n_nodi, grafo.n_archi))
lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.nome))

print("fine parsing")

print("numero grafi", len(lista_grafi))

print("-"*50)

crea_dict(lista_grafi)



#plot_graph()




i = 0
while i < len(lista_grafi):
    k = round(math.log(lista_grafi[i].n_nodi)**2)
    res = kargerAndStein(lista_grafi[i], k)
    res_karger_stain.append(res[0])
    
    g, peso = globalMinCut(lista_grafi[i])
    res_stoer_wagner.append(peso)
    
    i += 1

tot_risultati(lista_grafi, res_stoer_wagner, res_karger_stain)





############################# KARGER STAIN #############################

# for grafo in lista_grafi:
#     print ("nodi numero: ",grafo.n_nodi)
#     k = round(math.log(grafo.n_nodi)**2)
#     res = kargerAndStein(grafo, k)
#     print("soluzione")
#     print(res[0])
#     print("trovata dopo:")
#     print(res[2], "iterazioni e", res[3], "nanosecondi")



############################# STOER WAGNER #############################


# for i in range(len(lista_grafi)-40):
#     rip = globalMinCut(lista_grafi[i])
#     print(rip.totPeso)


""" #STOER      PRINT
lista_grafi = []
parsing(directory)
print("fine parsing")

print("numero grafi", len(lista_grafi))

#lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.n_nodi, grafo.n_archi))
lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.nome))

print("-"*50)


res = []
i = 0
while i < len(lista_grafi)-40:
    g = globalMinCut(lista_grafi[i])
    res.append(g.totPeso)
    #print(g.n_nodi, g.totPeso)
    i += 1


table = []
table.append([grafo.nome for grafo in lista_grafi])
#table.append([grafo.n_nodi for grafo in lista_grafi])     #table[0]
table.append([[i.id for i in grafo.lista_nodi_updated] for grafo in lista_grafi])
table.append(res)                                         #table[1]


res_table = []
for i in range(len(lista_grafi)-40):
    res_table.append([table[0][i], table[1][i], table[2][i]])

#print()
print(tabulate(res_table, headers= ["nome grafo", "nodi", "stoer_wagner"], tablefmt='pretty'))

#print_m(lista_grafi[0].adj_matrix) """
