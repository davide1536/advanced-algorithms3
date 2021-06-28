from Nodo import Nodo
import copy
class Grafo:
    def __init__(self):
        self.nome = ""
        self.n_nodi = 0
        self.n_archi = 0
        self.lista_nodi_obj = []
        self.lista_nodi_id = [] #lista nodi contentente gli id univoci
        self.id2Node = {}
        self.adj_matrix = None
        self.merged_n_nodi = 0 #numero di nodi rimasti
        self.lista_nodi_updated = []

    
    
    #restituisce l'oggetto nodo, dato l'id 
    def getNodo(self, id_nodo):
        return self.id2Node[id_nodo]
