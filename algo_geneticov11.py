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
    produccion = ['a', 'b', 'c', 'd', 'e']    
    cocina = ['f', 'g', 'h', 'j']    

    def __init__(self, deptos_produccion, quiebres_produccion, 
                       deptos_cocina, quiebres_cocina, fitness = None):

        self.deptos_produccion = deptos_produccion
        self.deptos_cocina = deptos_cocina
        self.quiebres_produccion = quiebres_produccion
        self.quiebres_cocina = quiebres_cocina
        self.fitness = fitness

    @classmethod
    def generar_genoma(cls):
        permutacion_produccion = random.sample(cls.produccion, len(cls.produccion))
        permutacion_produccion = [copy.deepcopy(d) for d in permutacion_produccion]
        quiebres_produccion = [random.randint(0,1) for _ in range(len(cls.produccion)-1)]    

        permutacion_cocina =  random.sample(cls.cocina, len(cls.cocina))
        permutacion_cocina = [copy.deepcopy(d) for d in permutacion_cocina]
        quiebres_cocina = [random.randint(0,1) for _ in range(len(cls.cocina)-1)]

        return  cls(permutacion_produccion, quiebres_produccion, permutacion_cocina, quiebres_cocina)
    
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
            permutacion_produccion.append(depto)        
        
        return f'''
        permutacion produccion: {self.deptos_produccion}
        quiebres produccion:    {self.quiebres_produccion}
        bahias produccion:      {self.generar_bahias(self.deptos_produccion, self.quiebres_produccion)}

        permutacion cocina:     {self.deptos_cocina}
        quiebres cocina:        {self.quiebres_cocina}
        bahias cocina:          {self.generar_bahias(self.deptos_cocina, self.quiebres_cocina)}
        '''

individuo = Genoma.generar_genoma()
print((individuo))