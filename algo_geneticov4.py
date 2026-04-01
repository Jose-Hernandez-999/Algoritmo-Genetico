import random
#falta terminar de definir objeto genoma/individuo 

class GenomaGA:
    def __init__(self, genoma):
        genoma.self = genoma

    def get_fitness(self):
        return None

lista_maestra_departamentos = ['P1', 'C1', 'A1', 'O1', 'A2', 'C12', 'M1', 'M2', 'M3'] 
lista_departamentos = ['P1', 'C1', 'A1', 'O1', 'A2', 'C12', 'M1', 'M2', 'M3']
total_departamentos = 9

def generar_individuo():
    deptos = random.sample(lista_departamentos, 9)
    quiebres = []
    for _ in range(len(lista_departamentos)-1):
        quiebre = random.randint(0,1)
        quiebres.append(quiebre)
    return deptos, quiebres

departamentos , quiebres = generar_individuo()

bahias = []
bahias_actuales = []
for i in range(len(departamentos)):
    bahias_actuales.append(departamentos[i])
    if i < len(quiebres) and quiebres[i] == 1:
        bahias.append(bahias_actuales)
        bahias_actuales = []
if bahias_actuales:
    bahias.append(bahias_actuales)

individuo = bahias

print()
print(f'vectores: {departamentos, quiebres}')
print()
print(f'genoma: {individuo}')
print()


#falta hacer que me devuelva un diccionario, terminar de definir clase individuo y agregar metodo para
# calcular fitness en clase Individuo
#agregar funcion que penalice layouts
#terminar clase individuo con atributos de cada layout para el algoritmo