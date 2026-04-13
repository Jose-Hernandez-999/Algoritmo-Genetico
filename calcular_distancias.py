import random

areas = [10, 15, 20]
largo_instalacion = 30

def calular_anchosbahias_y_altosdeptos(elementos, largo):
    
    #hace el vector de quiebres, ya lo tengo en el algo
    v_quiebres = [random.randint(0,1) for _ in range(len(elementos)-1)]
    
    #hace el vector de bahias juntando deptos de acuerdo al vector de quiebres (en este caso areas)
    bahias = []
    bahia_actual = []        
    for i in range(len(elementos)):
        bahia_actual.append(elementos[i])
        if i < len(v_quiebres) and v_quiebres[i] == 1:
            bahias.append(bahia_actual)
            bahia_actual = []
    if bahia_actual:
        bahias.append(bahia_actual)

    #devuelve la suma de las areas de los deptos por bahia (la cantidad de bahias depende de quiebres por tanto 
    # len(suma_areas) == len(quiebres))
    suma_deptos_bahia = []
    for j in range(len(bahias)):
        suma_areas = sum(bahias[j])
        suma_deptos_bahia.append(suma_areas)

    #devuelve el ancho de cada bahia de acuerdo a la formula ancho_bahia = sumatoria(areas en bahia)/largo_instalacion
    anchos_bahias = []
    for k in suma_deptos_bahia:
        ancho = k/largo
        anchos_bahias.append(ancho)

    #devuelve el alto de cada departamento en la bahia
    altos_por_bahia = []
    for l in range(len(bahias)):
        ancho = anchos_bahias[l]
        
        altos_deptos = []
        
        for area in bahias[l]:
            altos = area/ancho
            altos_deptos.append(altos)
    altos_por_bahia.append(altos_deptos)

    return v_quiebres, bahias, suma_deptos_bahia, anchos_bahias, altos_por_bahia

print(calular_anchosbahias_y_altosdeptos(areas, largo_instalacion))