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
        Departamento('M1', 'Comedor 1', 35.937,   6),
        Departamento('M2', 'Comedor 2', 47.0744,  7),
        Departamento('M3', 'Comedor 3', 13.94,    8)
    ]

    #variable global de clase para calcular distancias y obtener fitness
    largo_produccion = 30
    largo_restaurante = 14
    distancia_instalaciones = 43
    relacion_aspecto_maxima = 4
    matriz_flujos = [
    [ 0, 45, 45, 0, 0, 135, 0, 0, 0 ],
    [ 90, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 135, 80, 0, 0, 0, 10, 0, 0, 0 ],
    [ 1, 1, 1, 0, 1, 1, 1, 1, 1 ],
    [ 0, 0, 0, 0, 0, 40, 0, 0, 0 ],
    [ 0, 0, 15, 0, 0, 0, 90, 75, 45 ],
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
                distancia = (abs(depto_i.centroide_x - depto_j.centroide_x) 
                + abs(depto_i.centroide_y - depto_j.centroide_y))

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
        fitness = costo + (deptos_subtimos**5) * costo

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
            fitness_txt = "sin evaluar"
        else:
            fitness_txt = round(self.fitness, 3)

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

        {fitness_txt}
        ---------------------
        """

class Poblacion:
    
    def __init__(self, tamaño_poblacion):
        self.genomas = []
        self.generacion = 0 
        self.mejor_genoma = None
        self.mejor_generacion = None
        self.tamaño_poblacion = tamaño_poblacion

    @classmethod
    def generar_poblacion(cls, tamaño):
        #crea un objto Poblacion el cual es una lista de objetos Genoma y las guarda en el atributo genomas
        # la cantidad de genomas depende de cls.tamaño
        poblacion = cls(tamaño)
        for _ in range(poblacion.tamaño_poblacion):
            genoma = Genoma.generar_genoma()
            genoma.calcular_fitness()
            poblacion.genomas.append(genoma)

        #for loop que itera sobre el fitness de los genomas de la poblacion y devuelve el que tenga el mejor fitness
        # empiieza iterando sobre el primer genoma de la pobalcion  
        mejor_genoma = poblacion.genomas[0]
        for genoma in poblacion.genomas:
            if genoma.fitness < mejor_genoma.fitness:
                mejor_genoma = genoma

        #se asigna el atributo de la clase .mejor_genoma con el genoma que tenga el mejor fitness el cual devuelve el for loop anterior
        #se asigna el atributo .mejor_generacion con la generacion del genoma que tenga el mejor fitness
        poblacion.mejor_genoma = mejor_genoma
        poblacion.mejor_generacion = poblacion.generacion

        return poblacion
        
    def seleccion(self, k=5):
        #iteramos sobre el largo de la poblacion elegiendo genomas aleatorias en grupos de 5 en 5
        #creamos una lista de los genomas seleccionados al azar con random.sample
        padres = []
        for _ in range(self.tamaño_poblacion):
            candidatos = random.sample(self.genomas, k)
            #hacemos una comparacion de fitness de los genomas y agregamos a padres solo los mejores
            ganador = candidatos[0]
            for candidato in candidatos:
                if candidato.fitness < ganador.fitness:
                    ganador = candidato
                padres.append(ganador)
            return padres
        
    def cruce(self, padre1, padre2):
        #los parametros padre1 y padre2 son genomas/ objetos de la clase poblacion -> poblacion.genoma[0] o pobalcion.genoma[1] 
        #la funcion devuelve : hijo = poblacion.cruce(padre1, padre2)

        #PRODUCCION
        #se crean los indices de corte con random para el vector de produccion
        indices_prod = [random.randint(0,5) for i in range(2)]
        corte1_prod = min(indices_prod) 
        corte2_prod = max(indices_prod)
        
        segmento_produccion = padre1.deptos_produccion[corte1_prod:corte2_prod]
        codigos_segmento_produccion = [d.codigo for d in segmento_produccion]

        restantes_produccion = []
        for i in range(len(padre1.deptos_produccion)):
            indice_circular_produccion = (corte2_prod + i) % len(padre1.deptos_produccion)
            depto_prod = padre2.deptos_produccion[indice_circular_produccion]
            if depto_prod.codigo not in codigos_segmento_produccion:
                restantes_produccion.append(depto_prod)

        hijo_deptos_prod = [None] * len(padre1.deptos_produccion)
        hijo_deptos_prod[corte1_prod:corte2_prod] = segmento_produccion

        j = 0
        for i in range(len(padre1.deptos_produccion)):
            if hijo_deptos_prod[i] is None:
                hijo_deptos_prod[i] = restantes_produccion[j]
                j += 1
        
        hijo_deptos_prod = [copy.deepcopy(d) for d in hijo_deptos_prod]

        punto_prod = random.randint(0,len(padre1.quiebres_produccion))
        hijo_quiebres_prod = padre1.quiebres_produccion[:punto_prod] + padre2.quiebres_produccion[punto_prod:]        
        

        #RESTAURANTE----------------------------------------------------------------------------------
        #se crean los indices de los puntos de corte con random y vector de permutacion de restaurantes
        indices_rest = [random.randint(0,4) for i in range(2)]
        corte1_rest = min(indices_rest)
        corte2_rest = max(indices_rest)
        
        
        segmento_restaurante = padre1.deptos_restaurante[corte1_rest:corte2_rest]
        codigos_segmento_restaurante = [d.codigo for d in segmento_restaurante]

        restantes_restaurante = []
        for i in range(len(padre1.deptos_restaurante)):
            indice_circular_restaurante = (corte2_rest + i) % len(padre1.deptos_restaurante)
            depto_restaurante = padre2.deptos_restaurante[indice_circular_restaurante]
            if depto_restaurante.codigo not in codigos_segmento_restaurante:
                restantes_restaurante.append(depto_restaurante)

        hijo_deptos_rest = [None] * len(padre1.deptos_restaurante)
        hijo_deptos_rest[corte1_rest:corte2_rest] = segmento_restaurante

        k = 0
        for i in range(len(padre1.deptos_restaurante)):
            if hijo_deptos_rest[i] is None:
                hijo_deptos_rest[i] = restantes_restaurante[k]
                k += 1
        
        hijo_deptos_rest = [copy.deepcopy(d) for d in hijo_deptos_rest]

        punto_rest = random.randint(0,len(padre1.quiebres_restaurante))
        hijo_quiebres_rest = padre1.quiebres_restaurante[:punto_rest] + padre2.quiebres_restaurante[punto_rest:]

        return Genoma(
            hijo_deptos_prod,
            hijo_quiebres_prod,
            hijo_deptos_rest,
            hijo_quiebres_rest
        )

    def mutacion(self, genoma):
        #hacer swap de codigos en posicion random para vector permutacion de produccion 
        #flip de elementos en vector de quiebres para produccion
        aleatorio_swap_prod = random.random()
        aleatorio_flip_prod = random.random()
        aleatorio_swap_rest = random.random()
        aleatorio_flip_rest = random.random()

        probabilidad_swap_produccion = 0.2
        probabilidad_flip_produccion = 0.1
        probabilidad_swap_restaurante = 0.2
        probabilidad_flip_restaurante = 0.1

        #PRODUCCION
        #swap
        if aleatorio_swap_prod < probabilidad_swap_produccion:
            pos_i_produccion = random.randint(0, len(genoma.deptos_produccion)-1)
            pos_j_produccion = random.randint(0, len(genoma.deptos_produccion)-1)
            genoma.deptos_produccion[pos_i_produccion], genoma.deptos_produccion[pos_j_produccion] = \
            genoma.deptos_produccion[pos_j_produccion], genoma.deptos_produccion[pos_i_produccion]
            
        #flip
        if aleatorio_flip_prod < probabilidad_flip_produccion:
            pos_produccion = random.randint(0, len(genoma.quiebres_produccion)-1)
            if genoma.quiebres_produccion[pos_produccion] == 0:
                genoma.quiebres_produccion[pos_produccion] = 1
            else:
                genoma.quiebres_produccion[pos_produccion] = 0

        #RESTAURANTE
        #swap
        if aleatorio_swap_rest < probabilidad_swap_restaurante:
            pos_i_restaurante = random.randint(0, len(genoma.deptos_restaurante)-1)
            pos_j_restaurante = random.randint(0, len(genoma.deptos_restaurante)-1)
            genoma.deptos_restaurante[pos_i_restaurante], genoma.deptos_restaurante[pos_j_restaurante] = \
            genoma.deptos_restaurante[pos_j_restaurante], genoma.deptos_restaurante[pos_i_restaurante] 

        #flip            
        if aleatorio_flip_rest < probabilidad_flip_restaurante:
            pos_restaurante = random.randint(0, len(genoma.quiebres_restaurante)-1)
            if genoma.quiebres_restaurante[pos_restaurante] == 0:
                genoma.quiebres_restaurante[pos_restaurante] = 1
            else:
                genoma.quiebres_restaurante[pos_restaurante] = 0

    def reemplazo(self, hijos):

        todos = self.genomas + hijos
        todos.sort(key = lambda genoma: genoma.fitness)
        self.genomas = todos[:self.tamaño_poblacion]


    def busqueda_local_gwo(self, n_iteraciones = 10, theta = 0.4):
        #busqueda de nuevas soluciones 
        alfa = self.genomas[0] 
        beta = self.genomas[1]
        delta = self.genomas[2]

        for lider in [alfa, beta, delta]:
            tamaño_movimientos_prod = max(1, int(len(lider.deptos_produccion) * theta))
            tamaño_movimientos_rest = max(1, int(len(lider.deptos_restaurante) * theta))

            for _ in range(n_iteraciones):
                vecino = copy.deepcopy(lider)
                pos_prod = random.randint(0,len(vecino.quiebres_produccion)-1)
                pos_rest = random.randint(0,len(vecino.quiebres_restaurante)-1)

                #para produccion
                for _ in range(tamaño_movimientos_prod):
                    if random.random() < 0.5:   
                        i = random.randint(0, len(vecino.deptos_produccion)-1)
                        j = random.randint(0, len(vecino.deptos_produccion)-1)
                        vecino.deptos_produccion[i], vecino.deptos_produccion[j] = \
                        vecino.deptos_produccion[j], vecino.deptos_produccion[i]

                    elif vecino.quiebres_produccion[pos_prod] == 0:
                        vecino.quiebres_produccion[pos_prod] = 1
                    else:
                        vecino.quiebres_produccion[pos_prod] = 0

                #para restaurante
                for _ in range(tamaño_movimientos_rest):
                    if random.random() < 0.5:
                        k = random.randint(0, len(vecino.deptos_restaurante)-1)
                        l = random.randint(0, len(vecino.deptos_restaurante)-1)
                        vecino.deptos_restaurante[k], vecino.deptos_restaurante[l] = \
                        vecino.deptos_restaurante[l], vecino.deptos_restaurante[k]

                    elif vecino.quiebres_restaurante[pos_rest] == 0:
                        vecino.quiebres_restaurante[pos_rest] = 1
                    else:
                        vecino.quiebres_restaurante[pos_rest] = 0

                
                vecino.calcular_fitness()

                if vecino.fitness < lider.fitness:
                    for i in range(len(self.genomas)):
                        if self.genomas[i] is lider:
                            self.genomas[i] = vecino
                            break
                    lider = vecino
            
        #---------------------------------------------
        #COMPORTAMIENTO DE ATAQUE
        for lider in [beta, delta]:
            #COMPORTAMIENTO PARA PRODUCCION
            for i in range(len(lider.deptos_produccion)):
                if lider.deptos_produccion[i].codigo != alfa.deptos_produccion[i].codigo:
                    vecino = copy.deepcopy(lider)

                    codigo_buscado_produccion = alfa.deptos_produccion[i].codigo
                    for j in range(len(vecino.deptos_produccion)):
                        if vecino.deptos_produccion[j].codigo == codigo_buscado_produccion:
                            posicion_j = j
                            break
                    vecino.deptos_produccion[i], vecino.deptos_produccion[posicion_j] = \
                    vecino.deptos_produccion[posicion_j], vecino.deptos_produccion[i]

                    vecino.calcular_fitness()
                    if vecino.fitness < lider.fitness:
                        for k in range(len(self.genomas)):
                            if self.genomas[k] is lider:
                                self.genomas[k] = vecino
                                break
                        lider = vecino

            #COMPORTAMIENTO PARA RESTAURANTE
            for i in range(len(lider.deptos_restaurante)):
                if lider.deptos_restaurante[i].codigo != alfa.deptos_restaurante[i].codigo:
                    vecino = copy.deepcopy(lider)

                    codigo_buscado_restaurante = alfa.deptos_restaurante[i].codigo
                    for j in range(len(vecino.deptos_restaurante)):
                        if vecino.deptos_restaurante[j].codigo == codigo_buscado_restaurante:
                            posicion_j = j
                            break
                    vecino.deptos_restaurante[i], vecino.deptos_restaurante[posicion_j] = \
                    vecino.deptos_restaurante[posicion_j], vecino.deptos_restaurante[i]

                    vecino.calcular_fitness()
                    if vecino.fitness < lider.fitness:
                        for k in range(len(self.genomas)):
                            if self.genomas[k] is lider:
                                self.genomas[k] = vecino
                                break
                        lider = vecino
                        
                             
    def actualizar_mejor(self):
        
        mejor_generacion_actual = self.genomas[0]
        if mejor_generacion_actual.fitness < self.mejor_genoma.fitness:
            self.mejor_genoma = mejor_generacion_actual
            self.mejor_generacion = self.generacion
         
    def ciclo_generacional(self, max_generaciones):

        while self.generacion < max_generaciones:
            padres = self.seleccion()

            hijos = []
            for i in range(0, len(padres)-1, 2):
                hijo = self.cruce(padres[i], padres[i+1])
                self.mutacion(hijo)
                hijo.calcular_fitness()
                hijos.append(hijo)
            
            self.reemplazo(hijos)
            self.busqueda_local_gwo()
            self.actualizar_mejor()
        
            self.generacion += 1

            if self.generacion % 10 == 0:
                print(self.generacion)
                print(self.mejor_genoma)

        return self.mejor_genoma

    
    def __repr__(self):

        mejor_fitness_txt = round(self.mejor_genoma.fitness, 3)
        mejor_generacion_txt = self.mejor_generacion
        mejor_genoma_txt = str(self.mejor_genoma)
    
        return f"""
        ===================
        POBLACION:
        ===================
        Generacion Actual: {self.generacion}
        Tamaño Poblacion : {self.tamaño_poblacion}
        -------------------
        Mejor_fitness : {mejor_fitness_txt}
        Encontrado en iteracion/generacion: {mejor_generacion_txt}
        -------------------
        MEJOR GENOMA:
        {mejor_genoma_txt}
        -------------------
        """ 
#-----------------------------------------------------------------------------------------
#VERIFICACIONES

#verificacion de que cada genoma (posible layout) se genera y tiene fitness (costo mhc)
#genoma = Genoma.generar_genoma()
#genoma.calcular_fitness()
#print(genoma)

#verificacion de la funcion que inicializa la poblacion
# devuelve automaticamente el mejor genoma de la poblacion gracias al repr method
#poblacion = Poblacion.generar_poblacion(10)
#print(poblacion)

#EJECUCION DEL ALGORITMO COMPLETO:
#parametros usados:
# tamaño de poblacion (cantidad de objetos genoma los cuales usa el algoritmo para iterar) = 30
# generaciones (iteraciones del algoritmo) = 100
# k (cantidad de hijos a seleccionar) = 3 
# probabilidad de mutacion (pobabilidad de alterar los vectores del genoma)= 0.2
# iteraciones del gw optimizer (veces que el algoritmo iterar para introducir aleatoriedad y no sobreoptimizar el algoritmo) = 10
# theta (cantidad de moficaciones al vector departamentos en el gw optimizer) = 0,4   

poblacion = Poblacion.generar_poblacion(100)
poblacion.ciclo_generacional(max_generaciones = 300)
print(f"Mejor Fitness:    {poblacion.mejor_genoma.fitness}")
print(f"Mejor Generacion: {poblacion.mejor_generacion}")
print(poblacion.mejor_genoma)
#-----------------------------------------------------------------------------------------