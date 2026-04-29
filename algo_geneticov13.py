#para hoy 8/4/2026:
#1. crear clase Departamentos y agregar datos del excel como variable de clase en Genoma
#2. convertir los datos en clase Departamentos (atributos: codigo, nombre, area, ancho, alto, centroide X y centroide Y)
#3. refactorizar el classmethod  y __repr__ para que use los datos de las nuevas variables de clase
#4. perdirle review a chatgpt y empezar a programar el method calcular_fitness()

import random 
import copy

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

    def __repr__(self):

        if self.ancho is None:
            ancho_dp = '---'
        else:
            ancho_dp = round(self.ancho, 3)

        if self.alto is None:
            alto_dp = '---'
        else:
            alto_dp = round(self.alto, 3)
            
        if self.centroide_x is None:
            centroide_x_dp = '---'
        else:
            centroide_x_dp = round(self.centroide_x, 3)
        
        if self.centroide_y is None:
            centroide_y_dp = '---'
        else:
            centroide_y_dp = round(self.centroide_y, 3)
            
        return f"""
        Depto({self.codigo} | area: {self.area} | ancho: {ancho_dp} | alto: {alto_dp}
        centroide_x: {centroide_x_dp} | centroide_y: {centroide_y_dp})"""

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
        Departamento('M1', 'Comedor 1', 35.937, 6),
        Departamento('M2', 'Comedor 2', 47.0744,  7),
        Departamento('M3', 'Comedor 3', 13.94,    8)
    ]

    #variable global de clase para calcular distancias y obtener fitness
    largo_produccion = 30
    largo_restaurante = 14
    distancia_instalaciones = 43
    relacion_aspecto_maxima = 4
    matriz_flujos = [
        [ 0, 175, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 175, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 105, 70, 0 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 0, 0, 0, 0, 0, 0, 60, 0, 0 ],
        [ 0, 0, 175, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ] 

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

    def calcular_anchos_altos(self, bahias_produccion, bahias_restaurante):
        
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
        #se agrupan todos los departamentos en una sola variable para que permita hacer el calculo de costo 
        # por parejas
        total_departamentos = self.deptos_produccion + self.deptos_restaurante
        costo = 0

        #se itera sobre cada departamento de cada instalacion
        for depto_i in total_departamentos:
            for depto_j in total_departamentos:
                if depto_i is depto_j: #se agrega este condicional en caso de que la pareja de deptos sean los mismo
                    continue 
                
                #calculo de distancia usando el atributo .centroide
                distancia = abs(depto_i.centroide_x - depto_j.centroide_x) 
                + abs(depto_i.centroide_y - depto_j.centroide_y)

                #verificacion de si los deptos estan en la misma instalacion usando el atributo indice
                # los deptos de produccion tiene indices de 0 a 4 por tanto si no tienen el mismo .indice
                # son de instalaciones distintas, por tanto se suma la distancia entre cada instalacion
                mismo_espacio = (depto_i.indice <= 4) == (depto_j.indice <= 4)
                if not mismo_espacio:
                    distancia += self.distancia_instalaciones      

                #se encuentra el flujo entre el par de deptos usando el .indice ya que cada pareja representa una fila
                # y una columna
                flujo = self.matriz_flujos[depto_i.indice][depto_j.indice]

                costo += flujo * distancia
        
        return costo

    def calcular_penalizacion(self, costo):
        
        total_departamentos = self.deptos_produccion + self.deptos_restaurante
        #acumulador de los deptos que no cumplan la restriccion de relacion de aspecto
        deptos_subtimos = 0

        #iteramos sobre cada depto de ambas instalaciones sin condicionao
        for depto in total_departamentos:
            #definimso la variable de relacion de aspecto para cada depto haciendo el calculo del ancho y alto mas largo entre el mas costo
            #si la relacion de aspecto del depto es mayor al de la restriccion sumamos 1 al acumulador
            relacion_aspecto = max(depto.ancho, depto.alto) / min(depto.ancho, depto.alto)
            if relacion_aspecto > self.relacion_aspecto_maxima:
                deptos_subtimos += 1
        #aumentamos el valor del fitness haciendo al individuo suboptimo por romper mucho la restriccion
        fitness = costo + (deptos_subtimos**3) * costo

        return fitness

    def calcular_fitness(self):
        
        bahias_prod = self.generar_bahias(
            self.deptos_produccion, 
            self.quiebres_produccion
        )

        bahias_rest = self.generar_bahias(
            self.deptos_restaurante, 
            self.quiebres_restaurante
        )
    
        self.calcular_anchos_altos(bahias_prod, bahias_rest)
        self.calcular_centroides(bahias_prod, bahias_rest)

        mhc = self.calcular_costo()
        self.fitness = self.calcular_penalizacion(mhc)
    
    def __repr__(self):

        codigos_prod = []
        for depto in self.deptos_produccion:
            codigos_prod.append(depto.codigo)
    
        bahias_prod = self.generar_bahias(self.deptos_produccion, 
        self.quiebres_produccion)

        texto_bahias_prod = ''
        for i, bahia in enumerate(bahias_prod):
            texto_bahias_prod += f" bahia {i+1}:\n"
            for depto in bahia:
                texto_bahias_prod += f"     {depto}\n"

        
        codigos_rest = []
        for depto in self.deptos_restaurante:
            codigos_rest.append(depto.codigo)

        bahias_rest = self.generar_bahias(self.deptos_restaurante, 
        self.quiebres_restaurante)

        texto_bahias_rest = ''
        for i, bahia in enumerate(bahias_rest):
            texto_bahias_rest += f"bahia {i+1}:\n"
            for depto in bahia:
                texto_bahias_rest += f"{depto}\n"

        if self.fitness is None:
            fitnes_txt = "sin evaluar"
        else:
            fitnes_txt = round(self.fitness, 3)

        return f"""
        PRODUCCION-----------
        permutacion: {codigos_prod}
        quiebres:    {self.quiebres_produccion}
        bahias:      {texto_bahias_prod}
        RESTAURANTE----------
        permutacion: {codigos_rest}
        quiebres:    {self.quiebres_restaurante}
        bahias:      {texto_bahias_rest}
        FITNESS--------------

        {fitnes_txt}
        ---------------------
        """

class Poblacion:
    pass


#verificacion
individuo = Genoma.generar_genoma()
individuo.calcular_fitness()
print(individuo)