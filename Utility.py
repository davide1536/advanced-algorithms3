#classe utile per la Union-Find e mergeSort
#capitolo 21.3/4 del libro
import copy
import random
from Nodo import Nodo
from Grafo import Grafo
from tabulate import tabulate


################################## Merge + MergeSort ##################################

# algoritmo merge modificato per confrontare i pesi degli archi, data una lista archi
# p, q, r sono indici dell'array tali che p <= q < r
# gli indici dividono l'array in sottosequenze t.c. A[p..q] A[q+1..r] 
def merge(array, p, q, r):
    #lunghezza sottoarray A[p..q]
    n1 = q-p+1
    #lunghezza sottoarray A[q+1..r]
    n2 = r-q
    left = [0] * n1
    right = [0] * n2
    
    for i in range(0, n1):
        left[i] = array[p+i]
    
    for i in range(0, n2):
        right[i] = array[q+i+1]
    
    i = 0
    j = 0
    k = p
    while i < n1 and j < n2:
        if left[i].peso <= right[j].peso:
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        k += 1
    #elementi rimanenri di left e right
    #non sono riuscito ad implementarlo con il valore infito del libro :(
    while i < n1:
        array[k] = left[i]
        i += 1
        k += 1

    while j < n2:
        array[k] = right[j]
        j += 1
        k += 1


def mergeSort_weight(array, p, r):
    if p < r:
        q = (p+r)//2
        mergeSort_weight(array, p, q)
        mergeSort_weight(array, q+1, r)
        merge(array, p, q, r)


################################## DFS_ciclo + inizializzaGrafo ##################################


# Complessità O(n)
# - se G non ha un ciclo allora G è un albero ed m = n-1
# - se G ha un ciclo allora dopo aver attraversato al più n archi la procedura termina 
#   (viene scoperto un arco all'indietro)
#
# INPUT : grafo e nodo iniziale
# OUTPUT : true, se c'è un ciclo, false altrimenti
def dfs_ciclo(g, u, padri, visitati):
    visitati[int(u.nodo)] = 1
    for v in g.lista_adiacenza_nodi[u.nodo]:
        if v.nodo != padri[int(u.nodo)]:       # escludo il padre dalla lista degli adiacenti (sarà ovviamente già visitato)
            if visitati[int(v.nodo)] == 0:
                padri[int(v.nodo)] = u.nodo
                if dfs_ciclo(g, v, padri, visitati):
                    return True     # abbiamo incontrato un nodo già visitato e stiamo risalendo la ricorsione
            else:
                return True         # caso in cui incontriamo un nodo già visitato
    return False

                

# funzione che dato in input il grafo g, inizializza il grafo n_g con gli stessi nodi
def inizializzaGrafo(n_g, g):
        n_g.n_nodi = g.n_nodi
        n_g.id2Node = g.id2Node
        n_g.lista_nodi = g.lista_nodi
        
        for nodo in n_g.getListaNodi():
            n_g.lista_adiacenza_nodi.setdefault(nodo.nodo, [])
            n_g.lista_adiacenza.setdefault(nodo.nodo, [])



################################## Union-Find ##################################

def makeSet(nodo):
    nodo.padre = nodo.nodo
    nodo.size = 0


#union-by-size
def union(nodo1, nodo2, g):
    radice_nodo1 = findSet(g, nodo1) 
    radice_nodo2 = findSet(g, nodo2)
    r1 = g.getNodo(radice_nodo1)   #ottengo gli oggetti
    r2 = g.getNodo(radice_nodo2)  
    if radice_nodo1 == radice_nodo2:      #se hanno stessa radice, sono già nello stesso insieme
        return
    if r1.size >= r2.size:
        r2.padre = r1.nodo
        r1.size += r2.size
    else:
        r1.padre = r2.nodo
        r2.size += r1.size


#operazione find set con compressione del cammino
def findSet(g, nodo1):
    if nodo1.nodo != nodo1.padre:
        nodo1.padre = findSet(g, g.getNodo(nodo1.padre))
    return nodo1.padre



################################## Funzioni di Test ##################################


def test_tot_pesi(prim, kruskal, kruskal_naive):
    i = 0
    while i < len(prim):
        res = prim[i].totPeso == kruskal[i].totPeso == kruskal_naive[i].totPeso
        if not res:
            return False
        i+=1
    print("Tutti i grafi risultanti hanno peso uguale")
    return True



# controllo se l'mst risultante è un albero di supporto
# conto i nodi che visito
# n_nodi = numero di nodi visitati
def dfs_supporto(g, u, n_nodi, visitati):
    visitati[int(u.nodo)] = 1
    n_nodi.append('1')
    for v in g.lista_adiacenza_nodi[u.nodo]:
        if visitati[int(v.nodo)] == 0:
            dfs_supporto(g, v, n_nodi, visitati)


# controllo se l'mst risultante è un albero di supporto
# input lista_grafi per ogni algoritmo
# controllo se tutti i nodi sono stati visitati
# se il numero di archi è il minimo : dati n nodi --> n-1 archi
def test_albero_supporto(lista_grafi):
    res = True
    for grafo in lista_grafi:
        visitati = [0]*(grafo.n_nodi + 1)
        n_nodi = []
        dfs_supporto(grafo, grafo.getNodo("6"), n_nodi, visitati)
        print("-"*20)
        print()
        print("Numero di nodi nel grafo: ", grafo.n_nodi)
        print("Numero di nodi visitati con dfs: ", len(n_nodi)) 
        print("Numero di archi nel grafo: ", grafo.n_archi)
        print("É un albero di supporto?: ", grafo.n_nodi == len(n_nodi) and (grafo.n_archi + 1) == len(n_nodi) )
        print("Peso totale dell'albero: ", grafo.totPeso)
        print()
        if not(grafo.n_nodi == len(n_nodi) and (grafo.n_archi + 1) == len(n_nodi)):
            res = False
    return res


def test_total_supporto(prim, kruskal_naive, kruskal):

    rand = random.randint(0,1)
    if rand == 0: 
        easter_egg = True
    else:
        easter_egg = False
    
    res_p = test_albero_supporto(prim) 
    res_kn =  test_albero_supporto(kruskal_naive) 
    res_k = test_albero_supporto(kruskal)

    res = res_p or res_k or res_kn
    
    print("-"*20)

    if res and not easter_egg:
        print ("TUTTI GLI ALBERI SONO ALBERI DI SUPPORTO")
    
    elif res and easter_egg:
        print("Autodistruzione in:")
        print("3...")
        print("2...")
        print("1...")
        print("...")
        print("scherzo... è tutto giusto")

    else:
        print("ERRORE "*300000000)



#funzione min per confronti a 3 
# list = [tempo_prim, tempo_kruskal, tempo_kruskal_naive]
def min_reloaded(list):
    algo = ""
    min = 0
    if list[0] < list[1]:
        min = list[0]
        algo = "prim"
    elif list[0] > list[1]:
        min = list[1]
        algo = "kruskal"
    else:
        min = list[0]
        algo = "prim == kruskal"

    if min > list[2]:
        min = list[2]
        algo = "kruskal_naive"
    
    res = algo + " : " + str(min)
    return res
    

#funzione di output
def output_peso(prim, kruskal, kruskal_naive, lista_grafi_originale, p_t, k_t, kn_t):
    
    #tabella [numero nodi] [numero archi] [peso_prim] [peso_kruskal] [peso_kruskal_naive] []
    table = []
    table.append([grafo.n_nodi for grafo in lista_grafi_originale])     #table[0]
    table.append([grafo.n_archi for grafo in lista_grafi_originale])    #table[1]
    table.append([grafo.totPeso for grafo in prim])                     #table[2]
    table.append([grafo.totPeso for grafo in kruskal])                  #table[3]
    table.append([grafo.totPeso for grafo in kruskal_naive])            #table[4]
    table.append([tempo for tempo in p_t])                              #table[5]
    table.append([tempo for tempo in k_t])                              #table[6]
    table.append([tempo for tempo in kn_t])                             #table[7]

    #valori tabella
    
    tabella = []
    for i in range(len(lista_grafi_originale)):
        tabella.append([table[0][i], table[1][i], table[2][i], table[3][i], table[4][i], table[5][i], table[6][i], table[7][i], min_reloaded([table[5][i], table[6][i], table[7][i]])])

    print()
    print(tabulate(tabella, headers= ["n_nodi originali", "n_archi originali", "peso prim", "peso kruskal", "peso_kruskal_naive", "tempo Prim", "tempo Kruskal", "tempo Kruskal naive", "algoritmo migliore"], tablefmt='pretty'))

 
    








