from Grafo import Grafo
from Nodo import Nodo
import random
import os
import math
import time
import gc
from time import perf_counter_ns
from collections import defaultdict
import collections
import matplotlib.pyplot as plt
import copy
from Utility import *
from Heap import *
from datetime import datetime

#lista di grafi stoer wagner
res_stoer_wagner = []
#lista grafi karger stain
res_karger_stain = []

time_out = False



#lista dei tempi di stoer wagner
time_stoer_wagner = [] 
#lista dei tempi di karger stain
time_karger_stain = []

discovery_times = []
discovery_iterations = []


directory = "dataset/"
lista_grafi = []
dict_pesi = {}




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

    
    #creo gli oggetti nodo e il dizionario id2Node
    for nodo in lista_nodi:
        obj_nodo = Nodo(nodo)
        id2Node[obj_nodo.id] = obj_nodo
        lista_nodi_obj.append(obj_nodo)


    #setto gli attributi dell'arco
    g.nome = path[:-4]
    g.lista_nodi_updated = []
    g.id2Node = id2Node
    g.lista_nodi_obj = sorted(lista_nodi_obj, key=lambda nodo: (nodo.id))
    g.lista_nodi_id = [n for n in range(1, g.n_nodi+1)]     
    g.adj_matrix = adj_matrix
    g.merged_n_nodi = g.n_nodi
    g.lista_nodi_updated[:] = lista_nodi_obj
    lista_grafi.append(g)



def measure_run_time(n_instances, graphs, algorithm, start):
    sum_times = 0

    if graphs[0].n_nodi <=20:         #per avere valori più precisi le istanze con un basso numero di nodi vengono ripetute più volte
        iterations = 30
    else:
        iterations = 1
    

    print("testing graph size: ", graphs[0].n_nodi)
    
    #tempo prima del timeout
    PERIOD_OF_TIME = 900
    
    for i in range(n_instances):
        print("istanza numbero: ",i)
        if algorithm == "kargerAndStein":
            
            gc.disable()
            #nodo_casuale = next(iter(graphs[i].lista_nodi))    #casuale perchè il set lista_nodi cambia ordine ad ogni parsing
            
            start_time = perf_counter_ns()
            m = 0
            res = []
            
            #controllo timeout
            if time.time() < start + PERIOD_OF_TIME :
            
                while m < iterations:
                    #prim(graphs[i],graphs[i].getNodo(nodo_casuale))
                    k = round(math.log(graphs[i].n_nodi)**2)
                    res = kargerAndStein(graphs[i], k)
                    m+=1

                end_time = perf_counter_ns()
                res_karger_stain.append(res[0])
                #p_g.append(prim(graphs[i],graphs[i].getNodo(nodo_casuale)).getGrafoPrim())
                discovery_time = res[3]
                discovery_iteration = res[2]

                discovery_times.append(discovery_time)
                discovery_iterations.append(discovery_iteration)
                time_karger_stain.append(round((end_time - start_time)/iterations//1000, 3))
                gc.enable()
            
            else:
                res_karger_stain.append(0)
                time_karger_stain.append(0)
                discovery_times.append(math.inf)
                end_time = 0

        res_s = 0
        if algorithm == "storeAndWagner":            
            gc.disable()
            j = 0
            newGrafi = []
            
            for k in range(iterations):
                newGrafi.append(copy.deepcopy(graphs[i]))

            start_time = perf_counter_ns()
            
            #controllo timeout
            if time.time() < start + PERIOD_OF_TIME :
            
                while j < iterations:
                    g,res_s = globalMinCut(newGrafi[j])
                    j+=1
                end_time = perf_counter_ns()
                res_stoer_wagner.append(res_s)
                #kn_g.append(naiveKruskal(graphs[i]))
                time_stoer_wagner.append(round((end_time - start_time)/iterations//1000, 3))
                gc.enable()
            
            else:
                res_stoer_wagner.append(0)
                time_stoer_wagner.append(0)
                end_time = 0

        

        sum_times += (end_time - start_time)/iterations


    avg_time = round((sum_times / n_instances)//1000, 3) #millisecondi

    return avg_time



def measurePerformance(perform):
    
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


    algorithmsToTest = ["kargerAndStein","storeAndWagner"]
    totTimes = []
    totRatios = []
    totConstant = []

    if perform == True:
        for algorithm in algorithmsToTest:
            
            #inizio timer per timeout
            start = time.time()
            
            print("sto testando", algorithm)
            times = [measure_run_time(len(graphs_groupped[key]), graphs_groupped[key], algorithm, start) for key in graphs_groupped]
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
    perform = True
    [times, ratios, constant, sizes, graphs_groupped] = measurePerformance(perform)
    #data, dimensions = measureProbability(graphs_groupped)
    algorithmsToTest = ["kargerAndStein","storeAndWagner"]

    if perform == True:
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



def measureProbability(graphs_groupped):
    dimensions = []
    realValue = [3056,1526, 2137,1282, 969, 341,951, 484,346, 1137, 676, 508, 400, 43]
    data = [0]*len(realValue)

    for key in graphs_groupped.keys():
        dimensions.append(key)
    print(dimensions)
    j = 0
    while j < 300:
        print("sto facendo iterazione ", j)
        for i, key in enumerate(graphs_groupped):
            graph = graphs_groupped[key][0]
            k = round(math.log(graph.n_nodi)**2)
            res = kargerAndStein(graph,k)
            if res[0] != realValue[i]:
                data[i] += 1
        j += 1
    
    return data, dimensions

#---------------------------------------------------------------Karger & Stein---------------------------------------------------------------

            

def gradoPesato(g, nodi):
    for u in nodi:
        for peso in g.adj_matrix[u.id][1:]:
            u.d = u.d + peso


def randomSelect(g,c):
    minValue = 0
    maxValue = c[len(c)-1]-1
    r = random.randint(minValue, maxValue)

    avg = sum(c) / len(c)
   
    index = binarySearch(c, 0, len(c)-1, r, avg)
    
    vertex = g.lista_nodi_obj[index]
    
    return vertex


def edgeSelect(g):

    pesiComulativi_u = []
    tot_u = 0

    for u in g.lista_nodi_obj:
        tot_u = tot_u + u.d
        pesiComulativi_u.append(tot_u)
    
    
    u = randomSelect(g,pesiComulativi_u)

    pesiComulativi_v = []
    tot_v = 0

    for v in g.lista_nodi_obj:
        tot_v += g.adj_matrix[u.id][v.id]
        pesiComulativi_v.append(tot_v)
        
    v = randomSelect(g,pesiComulativi_v)

       

    return u,v


def contractEdge(g, edge):
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
        u,v = edgeSelect(g)
        edge = [u,v]
        contractEdge(g, edge)
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
    gradoPesato(g, g.lista_nodi_obj)
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

    discoveredTime = round((discoveredTime - start_time) / 1000000000,5)

    return minCut, gMin, discoveredIteration, discoveredTime



#---------------------------------------------------------------Stoer & Wagner---------------------------------------------------------------

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



#--------------------------------------------------------------- Main ---------------------------------------------------------------

print("-"*50)
parsing(directory)


lista_grafi = sorted(lista_grafi, key=lambda grafo: (grafo.nome))

print("fine parsing")

print("numero grafi", len(lista_grafi))

print("-"*50)

crea_dict(lista_grafi)



plot_graph()
tot_risultati(lista_grafi, res_stoer_wagner, res_karger_stain, time_stoer_wagner, time_karger_stain, discovery_times)

