from numpy import pi, sqrt, nan
from numpy.random import rand
from constantes import g_, ρ_acero, mm_
import pandas as pd
 
class Circular(object):
    """define una seccion Circular"""

    def __init__(self, D, Dint, color=rand(3)):
        super(Circular, self).__init__()
        self.D = D
        self.Dint = Dint
        self.color = color  #color para la seccion

    def area(self):
        return pi*(self.D**2 - self.Dint**2)/4

    def peso(self):
        return self.area()*ρ_acero*g_

    def inercia_xx(self):
        return pi*(self.D**4 - self.Dint**4)/4

    def inercia_yy(self):
        return self.inercia_xx()

    def nombre(self):
        return f"O{self.D*1e3:.0f}x{self.Dint*1e3:.0f}"

    def __str__(self):
        return f"Seccion Circular {self.nombre()}"


        
#Mas adelante, no es para P1E1

class SeccionICHA(object):
    """Lee la tabla ICHA y genera una seccion apropiada"""


    def obtener_perfil(self):

        den = []

        denominacion = self.denominacion

        info = denominacion.split('x')

        for l in info[0]:
            
            if not l.isdigit():
                den.append(l)
                info[0] = info[0][1:]

            else:
                break

        den = "".join(den)
        info.insert(0,den)

        
        for n in range(len(info[1:])):
            info[n+1] = float(info[n+1])


        return info

    def __init__(self, denominacion, base_datos="Perfiles ICHA.xlsx", debug=False, color=rand(3)):
        super(SeccionICHA, self).__init__()
        self.denominacion = denominacion
        self.color = color  #color para la seccion


        perfil = self.obtener_perfil()                          #lista con valores de denominación

        
        if perfil[0] == "H":
            hoja = 'H'

        elif perfil[0] == "PH":
            hoja = 'PH'

        elif perfil[0] == "HR" or perfil[0] == "W":
            hoja = 'HR'

        elif perfil[0] == "[]":
            hoja = 'Cajon'

        elif perfil[0] == "O":
            hoja = 'Circulares Mayores'

        elif perfil[0] == "o":
            hoja = 'Circulares Menores'

        else:
            hoja = 'h'


        df = pd.read_excel(io = base_datos, sheet_name = hoja)

        i = 0

        for f in df.index:

            if str(df.iloc[f, 0]) != 'nan':

                break

            i += 1

        e_1 = i
        e_2 = e_1 + 2
        e_3 = e_2 + 2
        df.columns = df.loc[e_2]

        self.row = df.iloc[0,:]

        for index, row in df.iterrows():

            if row['d'] == perfil[1] and row['bf'] == perfil[2] and row['peso'] == perfil[3]:
                self.row = df.iloc[index, : ]

   
    def area(self):

        return self.row['A']/1e6

    def peso(self):
        return self.row['peso']

    def inercia_xx(self):
        return self.row['Ix/10⁶']

    def inercia_yy(self):
        return self.row['Iy/10⁶']

    def __str__(self):

        find = True
        for c in self.row:
            if str(c) == 'nan':
                find = False
            else:
                find = True

        if find:

            s = f"{self.denominacion} encontrada. A={self.area()} Ix={self.inercia_xx()} Iy={self.inercia_yy()}\n"

        else:

            s = f"Tipo de seccion {self.denominacion} no encontrada en base de datos.\n"


        s += f"Seccion ICHA {self.denominacion}\n"
        s += f" Area : {self.area()}\n"
        s += f" Peso : {self.peso()}\n"
        s += f" Ixx  : {self.inercia_xx()}\n"
        s += f" Iyy  : {self.inercia_yy()}\n"


        return s
