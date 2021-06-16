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

#lista di grafi prim
p_g = []
#lista grafi kruskal
k_g = []
#lista grafi kruskal naive
kn_g = []

#lista dei tempi di prim
p_t = [] 
#lista dei tempi di kruskal
k_t = []
#lista dei tempi di kruakl naive
kn_t = []


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
    g.lista_nodi_updated = []
    g.lista_merged = []
    g.merged_matrix = [] #matrice con nodo compresso
    g.merged_matrix[:] = adj_matrix
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

    if graphs[0].n_nodi <=100:         #per avere valori più precisi le istanze con un basso numero di nodi vengono ripetute più volte
        iterations = 30
    else:
        iterations = 1
    #liste per confrontare gli algoritmi
    global p_g
    global k_g
    global kn_g
    global p_t 
    global k_t 
    global kn_t


    print("testing graph size: ", graphs[0].n_nodi)
    for i in range(n_instances):
        print("istanza numbero: ",i)
        if algorithm == "prim":
            gc.disable()
            nodo_casuale = next(iter(graphs[i].lista_nodi))    #casuale perchè il set lista_nodi cambia ordine ad ogni parsing

            start_time = perf_counter_ns()
            m = 0
            while m < iterations:
                #prim(graphs[i],graphs[i].getNodo(nodo_casuale))
                m+=1
            end_time = perf_counter_ns()
            #p_g.append(prim(graphs[i],graphs[i].getNodo(nodo_casuale)).getGrafoPrim())
            p_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "NaiveKruskal":
            gc.disable()
            start_time = perf_counter_ns()
            j = 0
            while j < iterations:
                #naiveKruskal(graphs[i])
                j+=1
            end_time = perf_counter_ns()
            #kn_g.append(naiveKruskal(graphs[i]))
            kn_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "Kruskal":
            gc.disable()
            start_time = perf_counter_ns()
            k = 0
            while k < iterations:
                #kruskal(graphs[i])     
                k += 1
            end_time = perf_counter_ns()
            #k_g.append(kruskal(graphs[i]))
            k_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

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

    algorithmsToTest = ["prim", "Kruskal", "NaiveKruskal"]
    totTimes = []
    totRatios = []
    totConstant = []
    for algorithm in algorithmsToTest:
        print("sto testando", algorithm)
        times = [measure_run_time(len(graphs_groupped[key]), graphs_groupped[key], algorithm) for key in graphs_groupped]
        totTimes.append(times)
        ratios = [None] + [round(times[i+1]/times[i],3) for i in range(len(sizes)-1)] 
        totRatios.append(ratios)

        if algorithm == "NaiveKruskal":
            totConstant.append([round(times[i]/(sizes[i][1] *sizes[i][0]),3) for i in range(len(sizes))])

        else:
            totConstant.append([round(times[i]/(sizes[i][1] * math.log(sizes[i][0])),3) for i in range(len(sizes))])

    return totTimes, totRatios, totConstant, sizes, graphs_groupped
    


def plot_graph():
    
    #misuro le performance per ogni algoritmo, i valori times, ratios, constant sono matrici di dimensione 4*n n sono il numero di dimensioni dei grafi
    [times, ratios, constant, sizes, graphs_groupped] = measurePerformance()
    algorithmsToTest = ["prim","Kruskal", "NaiveKruskal"]

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
        if algorithmsToTest[i] == "NaiveKruskal":
            for j in range (len(sizes)):
                reference.append (constant[i][len(constant[0]) - 1] * sizes[j][1] * sizes[j][0])
        else:
            for j in range (len(sizes)):
                reference.append (constant[i][len(constant[0]) - 1] * sizes[j][1] * math.log(sizes[j][0]))

        plt.plot(graphs_groupped.keys(), times[i], graphs_groupped.keys(), reference)
        plt.title("performance " + algorithmsToTest[i])
        plt.ylabel('run time(ns)')
        plt.xlabel('size')
        plt.show()

    plt.plot(graphs_groupped.keys(), times[0], label = 'Prim')
    plt.plot(graphs_groupped.keys(), times[1],label = 'Kruskal')
    plt.plot(graphs_groupped.keys(), times[2], label = 'Kruskal naive')
    plt.legend()
    plt.title("grafici in relazione")
    plt.ylabel('run time(ns)')
    plt.xlabel('size')
    plt.show()

    plt.plot(graphs_groupped.keys(), times[0], label = 'Prim')
    plt.plot(graphs_groupped.keys(), times[1],label = 'Kruskal')
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
    #print("massimo di c:", max(c))
    r = random.randint(c[0], c[len(c)-1])
    #print("elemento casuale:", r)
    # for i in c:
    #     print("lista c:", i)
    index = binarySearch(c, 0, len(c)-1, r)
    vertex = g.getListaNodi()[index]
    #print("il vertice corrispondente e'", vertex.id)
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

    return u,v


def contractEdge(g, edge):
    u = edge[0]
    v = edge[1]
    u.d = u.d + v.d - (2*g.adj_matrix[u.id][v.id])
    v.d = 0
    g.adj_matrix[u.id][v.id] = 0
    g.adj_matrix[v.id][u.id] = 0
    for i in range(1,len(g.adj_matrix)):
        g.adj_matrix[u.id][i] = g.adj_matrix[u.id][i] + g.adj_matrix[v.id][i]
        g.adj_matrix[i][u.id] = g.adj_matrix[i][u.id] + g.adj_matrix[i][v.id]
        g.adj_matrix[v.id][i] = 0
        g.adj_matrix[i][v.id] = 0 
    
    g.merged_n_nodi -= 1


def contract(g, k):
    n = g.merged_n_nodi
    for i in range(n-k):
        u,v = edgeSelect(g)
        edge = [u,v]
        contractEdge(g, edge)
    return g


#funzione che consente di trovare un taglio
def recursiveContract(g):
    w = []
    n = g.merged_n_nodi
    if n <= 6:
        g = contract(g, 2)
        return 1 #da cambiare
    t = round(g.merged_n_nodi/math.sqrt(2) + 1)
    
    for i in range(2):
        g = contract(g, t)
        w.append(recursiveContract(g))
    return min(w)


def kargerAndStein(g, k):
    gradoPesato(g, g.getListaNodi())
    g2 = g
    minCut = float('inf')
    for i in range(k):
        cut = recursiveContract(g2)
        if cut < minCut:
            minCut = cut
    return minCut



#---------------------------------------------------------------Stoer & Wagner---------------------------------------------------------------

def globalMinCut(g):
    if g.merged_n_nodi == 2:
        #print([i.id for i in g.lista_nodi_updated])
        g.totPeso = g.adj_matrix[g.lista_nodi_updated[0].id][g.lista_nodi_updated[1].id]
        #print(g.totPeso)
        return g
    else:
        g1, s, t = stMinCut(g)
        #print("g1", g1.totPeso)
        g2 = globalMinCut(stMerge(g, s, t))
        #print("g2", g2.totPeso)
        #print("-"*50)
        #print("nodi null", [i.id for i in g2.null_node])
        #print("nodi merged", s.id, t.id, [i.id for i in g2.merged_node])
        #print("-"*50)
        if(g1.totPeso < g2.totPeso):
            #print("peso stMin minore")
            return g1
        else:
            #print("peso global minore")
            return g2
        
        

def stMinCut(g):
    #inizializzo nodi
    index = 0
    for nodo in g.lista_nodi_updated:
        nodo.in_h = 1
        nodo.key = 0  #float('inf') indica un valore superiore a qualsiasi altro valore
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
        for nodo_adj in g.merged_matrix[u.id]:
            i += 1
            if nodo_adj != 0 and i > 0:
                v = g.getNodo(i)
                if isIn(v) == 1:
                    v.key += g.merged_matrix[u.id][v.id]
                    index = v.heapIndex  #ottengo la sua posizione all'interno dell'heap
                    heapIncreaseKey(q, index, v.key)
    
    #return min_peso, s, t
    g.totPeso = s.key
    return g, s, t



def stMerge(g,s,t):
    new_matrix = [] #matrice con nodo compresso
    new_matrix[:] = g.adj_matrix
    new_matrix[s.id][t.id] = 0
    new_matrix[t.id][s.id] = 0
    g.merged_node.add(s)
    g.null_node.add(t)
    g.lista_nodi_updated.remove(t)

    for nodo in g.lista_nodi_updated:
        new_matrix[s.id][nodo.id] += new_matrix[t.id][nodo.id]
        new_matrix[nodo.id][s.id] += new_matrix[nodo.id][t.id]
        new_matrix[t.id][nodo.id] = 0 
        new_matrix[nodo.id][t.id] = 0

    g.merged_matrix = new_matrix
    g.merged_n_nodi = g.merged_n_nodi - 1
    return g


























######################## MAIN ########################
print("-"*50)
parsing(directory)
print("fine parsing")

print("numero grafi", len(lista_grafi))

lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.n_nodi, grafo.n_archi))

print("-"*50)

# n_tot = 0
# a_tot = 0
# for g in lista_grafi:
#     n_tot += g.n_nodi
#     a_tot += g.n_archi 
# print(n_tot, a_tot) #11640 15452

# for g in lista_grafi:
#     if g.n_nodi == 10 and g.n_archi == 14:
#         print(g.adj_matrix[1][2])
#         print(g.adj_matrix[1][3])

# for i in range(len(lista_grafi)):
#     ripetizioni = round(math.log(lista_grafi[i].n_nodi)**2)
#     #print(ripetizioni)
#     mincut = kargerAndStein(lista_grafi[i], ripetizioni)
#     #print("faccio grafo da:", lista_grafi[i].n_nodi,"|", "min_cut: ", mincut)
#     if i <= 10:
#         print_m(lista_grafi[i].adj_matrix)





res = []
i = 0
while i < len(lista_grafi):
    g = globalMinCut(lista_grafi[i])
    res.append(g.totPeso)
    #print(g.n_nodi, g.totPeso)
    i += 1


table = []
table.append([grafo.n_nodi for grafo in lista_grafi])     #table[0]
table.append(res)                                         #table[1]


res_table = []
for i in range(len(lista_grafi)):
    res_table.append([table[0][i], table[1][i]])

#print()
print(tabulate(res_table, headers= ["numero nodi", "stoer_wagner"], tablefmt='pretty'))





#print_m(lista_grafi[0].adj_matrix)
#peso, s, t = stMinCut(lista_grafi[0])
#print("peso", peso)
#print("s", s.id)
#print("t", t.id)
# i = -1
# for nodo in lista_grafi[0].adj_matrix[2]:
#     i += 1
#     if nodo != 0:
#         print("nodo v", i)
#     print(nodo)


