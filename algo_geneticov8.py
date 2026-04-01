# hacer method .get_fitness() para objeto y clase Genoma
# hacer variable para leer archivos de excel desde los cuales cargar la informacion de la lista madre y hacer script para importar funcion en otro archivo 
# definiir representacion de clase Departamento 

#objetivos hoy: hacer method get_fitness() y hacee funcion para leer excel y importarla a este archivo

import random 
import copy

def leer_excel():
    return None

class Departamento:
    
    def __init__(self, codigo, nombre, area):
        self.codigo = codigo
        self.nombre = nombre
        self.area = area
        self.ancho = None
        self.alto = None
        self.centroide_x = None
        self.centroide_y = None

class GenomaAG:

    lista_maestra_departamentos = [
        Departamento('P1', 'Producción', 41.5552),
        Departamento('C1', 'Cocción', 6.6795),
        Departamento('A1', 'Almacenamiento', 25.2095),
        Departamento('O1', 'Oficina', 11.1112),
        Departamento('A2', 'Almacén gaseosa', 4.42  ),
        Departamento('C12', 'Cocina', 34.1648),
        Departamento('M1', 'Comedor', 35.937 ),
        Departamento('M2', 'Comedor 2', 47.0744),
        Departamento('M3', 'Comedor 3', 13.94  ),
    ]

    def __init__(self, departamentos, quiebres):
        self.departamentos = departamentos
        self.quiebres = quiebres
        self.fitness = None

    @classmethod
    def generar_genoma(cls):
        deptos = random.sample(cls.lista_maestra_departamentos, len(cls.lista_maestra_departamentos))
        deptos = [copy.deepcopy(i) for i in deptos]
        cantidad_quiebres = len(cls.lista_maestra_departamentos)-1
        quiebres = [random.randint(0,1) for _ in range(cantidad_quiebres)]
        return cls(deptos, quiebres)
    
    def crear_bahias(self):
        bahia = []
        bahia_actual = []
        for i in range(len(self.departamentos)):
            bahia_actual.append(self.departamentos[i])
            if i < len(self.quiebres) and self.quiebres[i] == 1:
                bahia.append(bahia_actual)
                bahia_actual = []
        if bahia_actual:
            bahia.append(bahia_actual)
        return bahia
    
    def __repr__(self):
        codigos = []
        for depto in self.departamentos:
            codigo_departamento = depto.codigo
            codigos.append(codigo_departamento)

        
        return f'Permutacion de departamentos: {str(codigos)}'



individuo = GenomaAG.generar_genoma()
print(repr(individuo))
#print(individuo.departamentos)