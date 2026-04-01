lista_maestra_departamentos = ['P1', 'C1', 'A1', 'O1', 'A2', 'C12', 'M1', 'M2', 'M3'] 
lista_departamentos = ['P1', 'C1', 'A1', 'O1', 'A2', 'C12', 'M1', 'M2', 'M3']
total_departamentos = 9

deptos  = [3,  7,  0,  5,  2,  8,  1,  6,  4]
quiebres =  [0,  1,  0,  0,  1,  0,  1,  0]
bahias = []
bahias_actuales = []

for i in range(len(deptos)):
    bahias_actuales.append(deptos[i])
    if i < len(quiebres) and quiebres[i] == 1:
        bahias.append(bahias_actuales)
        bahias_actuales = []
if bahias_actuales:
    bahias.append(bahias_actuales)

for i in range(len(deptos)):
    print(i)