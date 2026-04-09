#para hoy 8/4/2026:
#1. crear clase Departamentos y agregar datos del excel como variable de clase en Genoma
#2. convertir los datos en clase Departamentos (atributos: codigo, nombre, area, ancho, alto, centroide X y centroide Y)
#3. refactorizar el classmethod  y __repr__ para que use los datos de las nuevas variables de clase
#4. perdirle review a chatgpt y empezar a programar el method calcular_fitness()

import random 
import copy

class Departamento:

    def __init__(self, codigo, nombre, area):
        self.codigo = codigo
        self.nombre = nombre
        self.area = area
        self.ancho = None
        self.alto =  None
        self.centroide_x = None
        self.centroide_y = None

class Genoma:
    #variables de clase a convertir en clase "Departamento"
    produccion = [
        Departamento('P1', 'Producción',     41.5552),
        Departamento('C1', 'Cocción',        6.6795),
        Departamento('A1', 'Almacenamiento', 25.2095),
        Departamento('O1', 'Oficina',        11.1112),
        Departamento('A2', 'Almacén gaseosa',4.42)
    ]   

    restaurante = [
        Departamento('C12','Cocina',    34.1648),
        Departamento('M1', 'Comedor',   35.937),
        Departamento('M2', 'Comedor 2', 47.0744),
        Departamento('M3', 'Comedor 3', 13.94)
    ]
    
    def __init__(self, deptos_produccion, quiebres_produccion, 
                       deptos_restaurante, quiebres_cocina, fitness = None):

        self.deptos_produccion = deptos_produccion
        self.deptos_restaurante = deptos_restaurante
        self.quiebres_produccion = quiebres_produccion
        self.quiebres_cocina = quiebres_cocina
        self.fitness = fitness

    @classmethod
    def generar_genoma(cls):
        permutacion_produccion = random.sample(cls.produccion, len(cls.produccion))
        permutacion_produccion = [copy.deepcopy(d) for d in permutacion_produccion]
        quiebres_produccion = [random.randint(0,1) for _ in range(len(cls.produccion)-1)]    

        permutacion_restaurante =  random.sample(cls.restaurante, len(cls.restaurante))
        permutacion_restaurante = [copy.deepcopy(d) for d in permutacion_restaurante]
        quiebres_cocina = [random.randint(0,1) for _ in range(len(cls.restaurante)-1)]

        return  cls(permutacion_produccion, quiebres_produccion, permutacion_restaurante, quiebres_cocina)
    
    def generar_bahias(self, departamentos, quiebres):
        bahia = []
        bahia_actual = []   
        for i in range(len(departamentos)):
            bahia_actual.append(departamentos[i])
            if i < len(quiebres) and quiebres[i] == 1:
                bahia.append(bahia_actual)
                bahia_actual = []
        if bahia_actual:
            bahia.append(bahia_actual)
        return bahia

    def __repr__(self):
        
        permutacion_produccion = []
        for depto in self.deptos_produccion:
            depto.codigo
            permutacion_produccion.append(depto.codigo)
            
        permutacion_restaurante = []
        for depto in self.deptos_restaurante:
            depto.codigo
            permutacion_restaurante.append(depto.codigo)

        #terminar de corregir el repr method y hacer method calculo fitness y seguir el resto de pasos del algo 
        return f'''
        permutacion produccion:  {permutacion_produccion}
        quiebres produccion:     {self.quiebres_produccion} 
        bahias produccion:       {self.generar_bahias(permutacion_produccion, self.quiebres_produccion)}
        -----------------
        permutacion restaurante: {permutacion_restaurante}
        quiebres restaurante:    {self.quiebres_cocina}
        bahias restaurante:      {self.generar_bahias(permutacion_restaurante, self.quiebres_cocina)}
        '''
          
    def calcular_fitness(self):
        pass

individuo = Genoma.generar_genoma()
print((individuo))