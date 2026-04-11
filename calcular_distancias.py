areas = [10, 15, 20]
largo_instalacion = 30

def calcular_altos_anchobahia(area, largo_instalacion):
    
    suma_areas = sum(area)
    ancho_bahia = suma_areas/largo_instalacion

    altos_deptos = []    
    for a in area:
        alto_depto = a/ancho_bahia
        altos_deptos.append(alto_depto)

    return ancho_bahia , altos_deptos

print(calcular_altos_anchobahia(areas, largo_instalacion)) 