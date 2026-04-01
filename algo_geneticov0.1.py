import random

class IndividuoGA:
    def __init__(self, fitness = None):
        self.fitness = fitness


    def get_fitness(individuo):
        return None



departamentos = 9 
def generar_individuo():
    deptos = random.sample(range(0,9), 9)
    quiebres = []
    for q in range(departamentos - 1):
        quiebre = random.randint(0,1)
        quiebres.append(quiebre)
    return deptos, quiebres


#falta hacer que me devuelva un diccionario, terminar de definir clase individuo y agregar metodo para
# calcular fitness 
