import math
class Nodo:
    def __init__(self, id, padre = None, size = 0, key = 0, in_h = 1, heapIndex = 0, d = 0):
        self.id = id
        self.padre = padre  # padre del nodo (str)
        self.key = key      # utile per heap
        self.in_h = in_h    # = 1 perchè tutti i nodi sono nell'heap (prim)
        self.heapIndex = heapIndex      # indice del nodo all'interno dell'heap
        self.d = d
    
