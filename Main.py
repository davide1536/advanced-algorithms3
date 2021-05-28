from numpy import square
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
    lista_archi = []
    
    
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

        #set di nodi, per evitare i duplicati
        lista_nodi.add(nodo_1)
        lista_nodi.add(nodo_2)
        
        arco_1 = Arco(nodo_1, nodo_2, peso)
        lista_archi.append(arco_1)

    
    #creo gli oggetti nodo e il dizionario id2Node
    for nodo in lista_nodi:
        obj_nodo = Nodo(nodo)
        id2Node[obj_nodo.id] = obj_nodo


    #setto gli attributi dell'arco
    g.id2Node = id2Node
    g.lista_archi = lista_archi
    g.lista_nodi = lista_nodi
    g.lista_nodi_id = [n for n in range(1, g.n_nodi+1)]     
    g.adj_matrix = adj_matrix
    
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
                prim(graphs[i],graphs[i].getNodo(nodo_casuale))
                m+=1
            end_time = perf_counter_ns()
            p_g.append(prim(graphs[i],graphs[i].getNodo(nodo_casuale)).getGrafoPrim())
            p_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "NaiveKruskal":
            gc.disable()
            start_time = perf_counter_ns()
            j = 0
            while j < iterations:
                naiveKruskal(graphs[i])
                j+=1
            end_time = perf_counter_ns()
            kn_g.append(naiveKruskal(graphs[i]))
            kn_t.append(round((end_time - start_time)/iterations//1000, 3))
            gc.enable()

        if algorithm == "Kruskal":
            gc.disable()
            start_time = perf_counter_ns()
            k = 0
            while k < iterations:
                kruskal(graphs[i])     
                k += 1
            end_time = perf_counter_ns()
            k_g.append(kruskal(graphs[i]))
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
        print("grado pesato: u", u.d)

def randomSelect(g,c):
    r = random.randint(0, max(c)-1)
    print("elemento casuale:", r)
    for i in c:
        print("lista c:", i)
    index = binarySearch(c, 0, len(c), r)
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

    return u,v


def contractEdge(g, edge):
    u = edge[0]
    v = edge[1]
    u.d = u.d + v.d - (2*g.adj_matrix[u.id][v.id])
    v.d = 0

    for i in range(1,len(g.adj_matrix)):
        g.adj_matrix[u.id][i] = g.adj_matrix[u.id][i] + g.adj_matrix[v.id][i]
        g.adj_matrix[i][u.id] = g.adj_matrix[i][u.id] + g.adj_matrix[i][v.id]
        g.adj_matrix[v.id][i] = 0
        g.adj_matrix[i][v.id] = 0 

def contract(g, k):
    n = g.n_nodi
    for i in range(n-k):
        u,v = edgeSelect(g)
        edge = [u,v]
        contractEdge(g, edge)
    return g

#funzione che consente di trovare un taglio 
def recursiveContract(g):
    w = []
    n = g.n_nodi
    if n <= 6:
        g = contract(g, 2)
        return 1 #da cambiare
    t = round(g.n_nodi/math.sqrt(2) + 1)
    
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
    lista_nodi = g.getListaNodi()
    if g.n_nodi == 2:
        l1 = lista_nodi[0]
        l2 = lista_nodi[1]
        return l1, l2
    else:
        l1, l2, s, t = stMinCut(g)
        
        


def stMinCut(g):
    pass

def stMerge(g,s,t):
    pass
    





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

ripetizioni = round(math.log(lista_grafi[0].n_nodi)**2)
kargerAndStein(lista_grafi[0], ripetizioni)

