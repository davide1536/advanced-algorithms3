import math
class Nodo:
    def __init__(self, id, padre = None, size = 0, key = 0, in_h = 1, heapIndex = 0, d = 0, valore = None, figlio = None, sinistro = None,  destro = None, grado = 0, marcato = False ):
        self.id = id
        self.padre = padre  # padre del nodo (str)
        self.key = key      # utile per heap
        self.in_h = in_h    # = 1 perchè tutti i nodi sono nell'heap (prim)
        self.heapIndex = heapIndex      # indice del nodo all'interno dell'heap
        self.d = d
        #self.merged = merged # bit utile per sapere se quel nodo è stato compresso
