import numpy as np
from scipy.linalg import solve

class Reticulado(object):
    """Define un reticulado"""
    __NNodosInit__ = 100

    #constructor
    def __init__(self):
        super(Reticulado, self).__init__()
        
        #print("Constructor de Reticulado")
        
        self.xyz = np.zeros((Reticulado.__NNodosInit__,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.cargas = {}
        self.restricciones = {}
        """Implementar"""	
        


    def agregar_nodo(self, x, y, z=0):
        
        """Implementar"""	

        #print(f"Quiero agregar un nodo en ({x} {y} {z})")

        numero_de_nodo_actual = self.Nnodos

        self.xyz[numero_de_nodo_actual,:] = [x, y, z]

        self.Nnodos += 1
        
        return 0

    def agregar_barra(self, barra):
        
        self.barras.append(barra)        
        
        return 0

    def obtener_coordenada_nodal(self, n):
        
        if n >= self.Nnodos:
            return
        return self.xyz[n, :]

    def calcular_peso_total(self):
        
        peso = 0.
        
        for b in self.barras:
            peso += b.calcular_peso(self)
            
        return peso    
        

    def obtener_nodos(self):
        
        return self.xyz

    def obtener_barras(self):
        
        return self.barras



    def agregar_restriccion(self, nodo, gdl, valor=0.0):
        if nodo not in self.restricciones:
            self.restricciones[nodo] = [[gdl, valor]]
        else:
            self.restricciones[nodo].append([gdl, valor])


    def agregar_fuerza(self, nodo, gdl, valor):
        if nodo not in self.cargas:
            self.cargas[nodo] = [[gdl, valor]]
        else:
            self.cargas[nodo].append([gdl, valor])


    def ensamblar_sistema(self):
        Ngdl = self.Nnodos * self.Ndimensiones
        self.K = np.zeros((Ngdl,Ngdl), dtype=np.double)
        self.f = np.zeros((Ngdl), dtype=np.double)
        self.u = np.zeros((Ngdl), dtype=np.double)

        #Iterar sobre las barras:
        for i,b in enumerate(self.barras):
            ke = b.obtener_rigidez(self)
            fe = b.obtener_vector_de_cargas(self) 

            ni, nj = b.obtener_conectividad()


            #Metodo rigidez directa
            if self.Ndimensiones == 2:
                d = [2*ni, 2*ni+1 , 2*nj, 2*nj+1]
                   
            elif self.Ndimensiones == 3:
                d = [3*ni, 3*ni+1 , 3*ni+2, 3*nj, 3*nj+1, 3*nj+2]
                
            else:
                print("Error Ndimensiones")
                   
            for i in range(self.Ndimensiones*2): #Son dos nodos por elemento
                p = d[i]
                for j in range(self.Ndimensiones*2): #Son dos nodos por elemento
                    q = d[j]
                    self.K[p,q] += ke[i,j]
                self.f[p] = fe[i]
                



    def resolver_sistema(self):
        
        """Implementar"""	
        
        return 0

    def obtener_desplazamiento_nodal(self, n):
        
        """Implementar"""	
        
        return 0


    def obtener_fuerzas(self):
        
        """Implementar"""	
        
        return 0


    def obtener_factores_de_utilizacion(self, f):
        
        """Implementar"""	
        
        return 0

    def rediseñar(self, Fu, ϕ=0.9):
        
        """Implementar"""	
        
        return 0



    def chequear_diseño(self, Fu, ϕ=0.9):
        
        """Implementar"""	
        
        return 0







    def __str__(self):

        s = "Nodos:"
        s += "\n\n"
        

        for i in range(len(self.xyz[self.Nnodos,:])):

            n = self.xyz
            s += (f"{i} : ({n[i][0]}, {n[i][1]}, {n[i][2]})\n")

        s += "\n\n"

        s += "Barras:"
        s += "\n\n"

        for i in range(len(self.barras)):

            b = self.barras
            s += (f"{i} : [ {b[i].ni} {b[i].nj} ]\n")

        return s


    def guardar(self, nombre):

        import h5py

        print(f"Guardando en {nombre}")

        dataset = h5py.File(nombre, "w")
        dataser["xyz"] = self.xyz

        #hay que guardar nodos, barras, secciones y apoyos.
        #Secciones: solo queremos guardarlas por su nombre

        barras = np.zeros(len(self.barras), dtype = np.int32)

        
        for i, b in enumerate(self.barras):


            print(f"barra = {i} nj = {b.nj} ni = {b.ni}")
            barras[i, 0] = b.ni
            barras[i, 1] = b.nj
            