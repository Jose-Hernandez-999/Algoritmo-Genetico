#para hoy 8/4/2026:
#1. crear clase Departamentos y agregar datos del excel como variable de clase en Genoma
#2. convertir los datos en clase Departamentos (atributos: codigo, nombre, area, ancho, alto, centroide X y centroide Y)
#3. refactorizar el classmethod  y __repr__ para que use los datos de las nuevas variables de clase
#4. perdirle review a chatgpt y empezar a programar el method calcular_fitness()

import random 
import copy

def leer_excel():
    pass


class Departamento:

    def __init__(self, codigo, nombre, area, indice):
        self.codigo = codigo
        self.nombre = nombre
        self.area = area
        self.indice = indice
        self.ancho = None
        self.alto =  None
        self.centroide_x = None
        self.centroide_y = None

class Genoma:
    #variables de clase a convertir en clase "Departamento"
    produccion = [
        Departamento('P1', 'Producción',     41.5552, 0),
        Departamento('C1', 'Cocción',        6.6795,  1),
        Departamento('A1', 'Almacenamiento', 25.2095, 2),
        Departamento('O1', 'Oficina',        11.1112, 3),
        Departamento('A2', 'Almacén gaseosa',4.42,    4)
    ]   

    restaurante = [
        Departamento('C12','Cocina',    34.1648,  5),
        Departamento('M1', 'Comedor 1',   35.937, 6),
        Departamento('M2', 'Comedor 2', 47.0744,  7),
        Departamento('M3', 'Comedor 3', 13.94,    8)
    ]

    #variable global de clase para calcular distancias y obtener fitness
    largo_produccion = 30
    largo_restaurante = 14
    distancia_instalaciones = 43
    relacion_de_aspecto = 4


    def __init__(self, deptos_produccion, quiebres_produccion, 
                       deptos_restaurante, quiebres_restaurante, fitness = None):

        self.deptos_produccion = deptos_produccion
        self.deptos_restaurante = deptos_restaurante
        self.quiebres_produccion = quiebres_produccion
        self.quiebres_restaurante = quiebres_restaurante
        self.fitness = fitness

    @classmethod
    def generar_genoma(cls):

        permutacion_produccion = random.sample(cls.produccion, len(cls.produccion))
        permutacion_produccion = [copy.deepcopy(d) for d in permutacion_produccion]
        quiebres_produccion = [random.randint(0,1) for _ in range(len(cls.produccion)-1)]    

        permutacion_restaurante =  random.sample(cls.restaurante, len(cls.restaurante))
        permutacion_restaurante = [copy.deepcopy(d) for d in permutacion_restaurante]
        quiebres_restaurante = [random.randint(0,1) for _ in range(len(cls.restaurante)-1)]

        return  cls(permutacion_produccion, quiebres_produccion, permutacion_restaurante, quiebres_restaurante)

    def generar_bahias(self, departamentos, quiebres):
        
        bahias = []
        bahia_actual = []   
        for i in range(len(departamentos)):
            bahia_actual.append(departamentos[i])
            if i < len(quiebres) and quiebres[i] == 1:
                bahias.append(bahia_actual)
                bahia_actual = []
        if bahia_actual:
            bahias.append(bahia_actual)
        return bahias

    def calculo_anchos_altos(self, bahias_produccion, bahias_restaurante):
        
        #produccion
        for bahia in bahias_produccion:
            suma_areas = 0
            for depto in bahia:
                suma_areas += depto.area
            ancho_bahia = suma_areas/self.largo_produccion

            for depto in bahia:
                depto.ancho = ancho_bahia
                depto.alto = depto.area/ancho_bahia
        
        #restaurante
        for bahia in bahias_restaurante:
            suma_areas = 0
            for depto in bahia:
                suma_areas += depto.area
            ancho_bahia = suma_areas/self.largo_restaurante

            for depto in bahia:
                depto.ancho = ancho_bahia
                depto.alto = depto.area/ancho_bahia
    
    def calcular_centroides(self, bahias_produccion, bahias_restaurante):

        #calculo de centroides de produccion (el unico cambio es en la variable "largo" usada)
        borde_izq = 0
        for bahia in bahias_produccion:
            ancho_actual = bahia[0].ancho
            borde_sup = self.largo_produccion

            for depto in bahia:
                depto.centroide_x = borde_izq + ancho_actual/2
                depto.centroide_y = borde_sup - depto.alto/2
                borde_sup -= depto.alto
            
            borde_izq += ancho_actual

        #calculo de centroides en el restaurante
        borde_izq = 0
        for bahia in bahias_restaurante:
            ancho_actual = bahia[0].ancho
            borde_sup = self.largo_restaurante

            for depto in bahia:
                depto.centroide_x = borde_izq + ancho_actual/2
                depto.centroide_y = borde_sup - depto.alto/2
                borde_sup -= depto.alto          
                
            borde_izq += ancho_actual

    def calcular_costo(self):
        total_departamentos = self.deptos_produccion + self.deptos_restaurantes
        
        



        
        pass
        
        
        
        
        


    def __repr__(self):

        permutacion_produccion = []
        for depto in self.deptos_produccion:
            permutacion_produccion.append(depto.codigo)
            
        permutacion_restaurante = []
        for depto in self.deptos_restaurante:
            permutacion_restaurante.append(depto.codigo)

        #devuelve los objetos 
        bahias_produccion_objetos = self.generar_bahias(self.deptos_produccion, self.quiebres_produccion)
        bahias_restaurante_objetos = self.generar_bahias(self.deptos_restaurante, self.quiebres_restaurante)

        #devuelve el atributo codigo de los objetos del return de generar_bahias()
        bahias_produccion = []
        for bahia in bahias_produccion_objetos:
            sublista_produccion = []
            for depto in bahia:
                sublista_produccion.append(depto.codigo)
            bahias_produccion.append(sublista_produccion) 

        bahias_restaurante = []
        for bahia in bahias_restaurante_objetos:
            sublista_restaurante = []
            for depto in bahia:
                sublista_restaurante.append(depto.codigo)
            bahias_restaurante.append(sublista_restaurante)
    
        return f'''
        permutacion produccion:  {permutacion_produccion}
        quiebres produccion:     {self.quiebres_produccion} 
        bahias produccion:       {bahias_produccion}
        -----------------
        permutacion restaurante: {permutacion_restaurante}
        quiebres restaurante:    {self.quiebres_restaurante}
        bahias restaurante:      {bahias_restaurante}
        '''
          

    def calcular_fitness(self):
        pass

poblacion = 200
individuo = Genoma.generar_genoma()
print(individuo)

for s in range(poblacion):
    print(individuo)