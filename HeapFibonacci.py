import math

class heap_fibonacci:

    class Nodo:
        def __init__(self, key, valore):
            self.key = key
            self.valore = valore
            self.padre = None
            self.figlio = None
            self.sinistro = None    #fratello sinistro
            self.destro = None      #fratello destro
            self.grado = 0      
            self.marcato = False

    def itera(self, p):
        n = s = p
        flag = False
        while True:
            if n == s and flag is True:
                break
            elif n == s:
                flag = True
            yield n
            n = n.destro

    radice_lista = None             #puntatore alla prima radice della lista
    nodo_massimo = None             #puntatore alla radice con chiave massima
    tot_nodi = 0                    #numero complessivo di nodi

    def trova_massimo(self):
        return self.nodo_massimo

    def estrai_massimo(self):
        m = self.nodo_massimo
        if m != None:
            if m.figlio != None:
                #sposto tutti i suoi figli come radice
                figli = [x for x in self.itera(m.figlio)]
                for i in range(0, len(figli)):
                    self.unisco_liste(figli[i])
                    figli[i].padre = None
            self.tolgo_radice(m)
            #aggiorno il nuovo nodo massimo 
            if m == m.destro:
                self.nodo_massimo = self.radice_lista = None        #se il massimo era l'unico nodo mette il campo massimo a NULL
            else:
                self.nodo_massimo = m.destro 
                self.consolida()
            self.tot_nodi -= 1
        return m

    #Il nuovo elemento viene inserito in testa alla lista delle radici e vengono opportunamente inizializzati tutti i suoi campi
    def aggiungi_nodo(self, key, valore=None):
        n = self.Nodo(key, valore)
        n.sinistro = n.destro = n
        self.unisco_liste(n)
        if self.nodo_massimo == None or n.key > self.nodo_massimo.key:
            self.nodo_massimo = n
        self.tot_nodi += 1
        return n

    def incrementa_key(self, x, k):     #la chiave di x va incrementata, k nuovo valore della chiave
        if k < x.key:                   #valore vecchio maggiore del nuovo
            return None
        x.key = k
        y = x.padre
        if y != None and x.key > y.key:
            self.taglia(x, y)
            self.taglio_a_cascata(y)
        if x.key > self.nodo_massimo.key:
            self.nodo_massimo = x

    def taglia(self, x, y):
        self.tolgi_figlio(y, x)
        y.grado -= 1
        self.unisco_liste(x)
        x.padre = None
        x.marcato = False

    def taglio_a_cascata(self, y):
        z = y.padre
        if z != None:
            if y.marcato == False:
                y.marcato = True
            else:
                self.taglia(y, z)
                self.taglio_a_cascata(z)

    #La funzione consolida() ha il compito di ricompattere il più possibile gli alberi
    def consolida(self):
        A = [None] * int(math.log(self.tot_nodi) * 2)
        nodi = [w for w in self.itera(self.radice_lista)]
        for w in range(0, len(nodi)):
            x = nodi[w]
            d = x.grado
            while A[d] != None:
                y = A[d]
                if x.key < y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        for i in range(0, len(A)):
            if A[i] != None:
                if A[i].key > self.nodo_massimo.key:
                    self.nodo_massimo = A[i]

    def heap_link(self, y, x):
        self.togli_figlio(x, y)
        y.sinistro = y.destro = y
        self.unisco_figlio(x, y)
        x.grado += 1
        y.padre = x
        y.marcato = False

    def unisco_liste(self, n):
        if self.radice_lista == None:
            self.radice_lista = n
        else:
            n.destro = self.radice_lista.destro
            n.sinistro = self.radice_lista
            self.radice_lista.destro.sinistro = n
            self.radice_lista.destro = n

    def unisco_figlio(self, padre, n):
        if padre.figlio == None:
            padre.figlio = n
        else:
            n.right = padre.figlio.destro
            n.sinistro = padre.figlio
            padre.figlio.destro.sinistro = n
            padre.figlio.destro = n

    #rimuovo il nodo dalla lista radice
    def tolgo_radice(self, n):
        if n == self.radice_lista:
            self.radice_lista = n.destro
        n.sinistro.destro = n.destro
        n.destro.sinistro = n.sinistro

    def togli_figlio(self, padre, n):
        if padre.figlio and padre.figlio == padre.figlio.destro:
            padre.figlio = None
        elif padre.figlio == n:
            padre.figlio = n.destro
            n.destro.padre = padre
        n.sinistro.destra = n.destro
        n.destro.sinistro = n.sinistro

