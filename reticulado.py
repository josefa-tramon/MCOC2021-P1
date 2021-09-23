import numpy as np
from scipy.linalg import solve

class Reticulado(object):
    """Define un reticulado"""
    __NNodosInit__ = 1

    #constructor
    def __init__(self):
        super(Reticulado, self).__init__()
        
        #print("Constructor de Reticulado")
        
        self.xyz = np.zeros((Reticulado.__NNodosInit__,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.cargas = {}
        self.restricciones = {}
        self.Ndimensiones = 3
        """Implementar"""	
        


    def agregar_nodo(self, x, y, z=0):

        #print(f"Quiero agregar un nodo en ({x} {y} {z})")

        numero_de_nodo_actual = self.Nnodos
        self.xyz.resize((numero_de_nodo_actual+1, 3))
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


    def ensamblar_sistema(self, factor_peso_propio):
        
        self.Ngdl = self.Nnodos * self.Ndimensiones
        
        self.K = np.zeros((self.Ngdl,self.Ngdl), dtype=np.double)
        self.f = np.zeros((self.Ngdl), dtype=np.double)
        self.u = np.zeros((self.Ngdl), dtype=np.double)
        self.fpeso = factor_peso_propio

        #Ensamblar rigidez y vector de cargas
        for i,barra in enumerate(self.barras):
            Ke = barra.obtener_rigidez(self)
            fe = barra.obtener_vector_de_cargas(self)

            ni = barra.obtener_conectividad()[0]
            nj = barra.obtener_conectividad()[1]
                       
            
            d = [3*ni, 3*ni+1, 3*ni+2, 3*nj, 3*nj+1, 3*nj+2]
            

            for i in range(self.Ndimensiones*2):
                p = d[i]
                for j in range(self.Ndimensiones*2):
                    q = d[j]
                    self.K[p,q] += Ke[i,j]
                if factor_peso_propio != [0., 0., 0.]:
                    self.f[p] += fe[i]


    def resolver_sistema(self):
        
        N_gdl = self.Nnodos * self.Ndimensiones
        gdl_libres       = np.arange(N_gdl)
        gdl_restringidos = []


        for n in self.restricciones:

            for restriccion in self.restricciones[n]:


                gdl = restriccion[0]
                valor = restriccion[1]
                gdl_global = n*3 + gdl
                self.u[gdl_global] += valor
                gdl_restringidos.append(gdl_global)

       


        for nodo in self.cargas:

            for carga in self.cargas[nodo]:

                gdl = carga[0]
                valor = carga[1]
                gdl_global = nodo*3 + gdl
                self.f[gdl_global] += valor


        gdl_libres = np.setdiff1d(gdl_libres,gdl_restringidos)
                

        Kff = self.K[np.ix_(gdl_libres,gdl_libres)]
        Kfc = self.K[np.ix_(gdl_libres,gdl_restringidos)]
        Kcf = Kfc.T
        Kcc = self.K[np.ix_(gdl_restringidos,gdl_restringidos)]
        
        uf = self.u[gdl_libres]
        uc = self.u[gdl_restringidos]

        ff = self.f[gdl_libres]
        fc = self.f[gdl_restringidos]

        uf = solve(Kff, ff- Kfc @ uc)

        # Resolver para obtener uf -->  Kff uf = ff - Kfc*uc
        self.Rc = Kcf@uf + Kcc@uc - fc  

        #Asignar uf al vector solucion
        self.u[gdl_libres] = uf

        #Marcar internamente que se tiene solucion
        self.tiene_solucion = True
        

    def obtener_desplazamiento_nodal(self, n):

        dofs = [3*n, 3*n+1, 3*n+2]

        return self.u[dofs]


    def obtener_fuerzas(self):
        
        fuerzas = np.zeros((len(self.barras)), dtype=np.double)
        for i,b in enumerate(self.barras):
            fuerzas[i] = b.obtener_fuerza(self)

        return fuerzas


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

        s = " nodos:"
        s += "\n"

        for i in range(self.Nnodos):

            n = self.xyz
            s += (f"  {i} : ({n[i][0]}, {n[i][1]}, {n[i][2]})\n")

        s += "\n\n"

        s += " barras:"
        s += "\n"

        for i in range(len(self.barras)):

            b = self.barras
            s += (f"  {i} : [ {b[i].ni} {b[i].nj} ]\n")

        s += "\n\n"
        
        s += " restricciones:"
        s += "\n"
        
        for nodo in self.restricciones:
            s += f"  {nodo} : {self.restricciones[nodo]}\n"
            
        s += "\n\n"
        
        s += " cargas:"
        s += "\n"
        
        for nodo in self.cargas:
            s += f"  {nodo} : {self.cargas[nodo]}\n"
            
        s += "\n\n"

        s += " desplazamientos:"
        s += "\n"
        
        if self.Ndimensiones == 3:
                uvw = self.u.reshape((-1,3))
                for n in range(self.Nnodos):
                    s += f"  {n} : ( {uvw[n,0]}, {uvw[n,1]}, {uvw[n,2]})\n "
                    
        s += "\n\n"

        s += " fuerzas:"
        s += "\n"
        
        f = self.obtener_fuerzas()
        for b in range(len(self.barras)):
            s += f"  {b} : {f[b]}\n"
            
        s += "\n"
       
        s += f"Ndimensiones = {self.Ndimensiones}"
        
        s += "\n\n\n"
        return s

    def guardar(self, nombre):

        import h5py

        print(f"Guardando en {nombre}")

        dataset = h5py.File(nombre, "w")
        dataset["xyz"] = self.xyz

        #hay que guardar nodos, barras, secciones y apoyos.
        #Secciones: solo queremos guardarlas por su nombre

        barras = np.zeros(len(self.barras), dtype = np.int32)

        
        for i, b in enumerate(self.barras):


            print(f"barra = {i} nj = {b.nj} ni = {b.ni}")
            barras[i, 0] = b.ni
            barras[i, 1] = b.nj
            