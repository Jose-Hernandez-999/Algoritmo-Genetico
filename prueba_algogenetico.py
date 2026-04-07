
import random 
import copy

class Genoma:

    produccion = ['a', 'b', 'c', 'd', 'e']    
    cocina = ['f', 'g', 'h', 'j']    

    def __init__(self, deptos_produccion, quiebres_produccion, 
                       deptos_cocina, quiebres_cocina, fitness = None):

        self.deptos_produccion = deptos_produccion
        self.deptos_cocina = deptos_cocina
        self.quiebres_produccion = deptos_produccion
        self.quiebres_cocina = deptos_cocina
        self.fitness = fitness

    @classmethod
    def generar_individuo(cls):
        permutacion_produccion = random.sample(cls.produccion, len(cls.produccion))
        permutacion_produccion = [copy.deepcopy(d) for d in permutacion_produccion]
        quiebres_produccion = [random.randint(0,1) for _ in range(len(cls.produccion)-1)]    

        permutacion_cocina =  random.sample(cls.cocina, len(cls.cocina))
        permutacion_cocina = [copy.deepcopy(d) for d in permutacion_cocina]
        quiebres_cocina = [random.randint(0,1) for _ in range(len(cls.cocina)-1)]

        return  cls(permutacion_produccion, quiebres_produccion, permutacion_cocina, quiebres_cocina)

    def __repr__(self):
        valores_produccion = []    
        for d in range(self.deptos_produccion):
            pass


        return None

individuo = Genoma.generar_individuo()
print(repr(individuo))