# DESCRIZIONE CLASSE E FUNZIONI HEAP:
# La classe heap è costituita da:
#     vettore associato all'heap
#     lunghezza del vettore
#     lunghezza dell'heap (che all'inizio equivale alla lunghezza del vettore)
# Le funzioni disponibili sono:
#     BuildMinHeap(h) --> h = oggetto heap, la funzione dato un oggetto heap h costruisce una minHeap
#     HeapDecreaseKey(h, i, key) --> h = oggetto heap, i=valore indice, key = nuova chiave, dato un oggetto heap h sostituisce il valore del vettore associato
#                                                                                             all'indice i con il nuovo valore key
#     MinHeapInsert(h, key) --> h= heap, key = nuovo valore da aggiungere all'heap, dato un oggetto heap aggiungo un nuovo valore key
#     HeapMinimum(h) --> ottengo il valore minimo dell'heap
#     HeapExtractMin(h) --> recupera il valore minimo dall'heap e eliminalo
from numpy import maximum
from Nodo import Nodo
import math

class Heap:
    def __init__(self, vector):
        new_vector = []
        new_vector[:] = vector #così il vettore originale non viene modificato
        self.vector = new_vector
        self.length = len(vector)
        self.heapsize = self.length


def buildMaxHeap(h):
    for i in range(h.length//2-1, -1, -1):
        maxHeapify(h, i)


def maxHeapify (h, i):
    l = left(i)
    r = right(i)
    maximum = i
    if l <= h.heapsize-1 and h.vector[l].key > h.vector[i].key:
        maximum = l
    else:
        maximum = i
    if r <= h.heapsize-1 and h.vector[r].key > h.vector[maximum].key:
        maximum = r
    if maximum != i:
        #salvo gli indici
        indexCurrent = h.vector[i].heapIndex
        indexMaximum = h.vector[maximum].heapIndex
        #scambio gli indici
        h.vector[i].heapIndex = indexMaximum
        h.vector[maximum].heapIndex = indexCurrent
        #scambio i valori
        #temp = h.vector[i]                  #devo sia scambiare i valori ma anche l'indice associato ad ogni valore
        h.vector[i], h.vector[maximum] = h.vector[maximum], h.vector[i]
        #h.vector[maximum] = temp

        return maxHeapify(h,maximum)


def heapIncreaseKey(h, i, key):
    if key < h.vector[i].key:
        exit("la nuova chiave è più piccola di quella corrente")
    h.vector[i].key = key
    while i>0 and h.vector[parent(i)].key < h.vector[i].key:
        #salvo gli indici
        currentIndex = h.vector[i].heapIndex
        parentIndex = h.vector[parent(i)].heapIndex

        #scambio gli indici
        h.vector[i].heapIndex = parentIndex
        h.vector[parent(i)].heapIndex = currentIndex

        #scambio i valori
        #temp = h.vector[i]
        h.vector[i], h.vector[parent(i)] = h.vector[parent(i)], h.vector[i]
        #h.vector[parent(i)] = temp
        i = parent(i)

def maxHeapInsert(h, key):
    h.heapsize = h.heapsize+1
    h.vector[h.heapsize-1] = -math.inf #il valore più piccolo di tutti
    heapIncreaseKey(h, h.heapsize-1, key)


# def HeapMinimum(h):
#     return h.vector[0]

def heapExtractMax(h):
    if h.heapsize < 1:
        print ("underflow dell'heap")
    max = h.vector[0]
    h.vector[0] = h.vector[h.heapsize-1]
    h.vector[0].heapIndex = 0
    h.heapsize = h.heapsize - 1
    maxHeapify(h, 0)
    max.in_h = 0
    return max

def isIn(v):
    if v.in_h == 1:
        return 1
    return 0

def right(index):
    return 2*index+2

def left(index):
    return 2*index+1

def parent(index):
    return (index-1)//2 







