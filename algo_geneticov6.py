# hacer method .get_fitness() para objeto y clase Genoma
# hacer variable para leer archivos de excel desde los cuales cargar la informacion de la lista madre y hacer script para importar funcion en otro archivo 
# definiir representacion de clase Departamento 

import random 
import copy


class Departamento:
    
    def __init__(self, codigo, nombre, area):
        self.codigo = codigo
        self.nombre = nombre
        self.area = area

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
        deptos = random.sample(
            cls.lisa_maestra_departamentos,
            len(cls.lisa_maestra_departamentos)
        )
        deptos = [copy.deepcopy(i) for i in deptos]
        quiebres = [
            random.randint(0,1) 
            for _ in range(len(cls.lisa_maestra_departamentos))-1
        ]
        return cls(deptos, quiebres)
