import numpy as np
from cargar_datos import cargar_serie
from errores import evaluar_variacion

CIFRAS_SIGNIFICATIVAS = 2  # norma general de la seccion 4 del enunciado
def variacion_anual(anios, meses_num, precios, cifras=CIFRAS_SIGNIFICATIVAS):
    # obtenemos los años unicos y ordenados
    anios_unicos = sorted(set(anios.tolist()))
    resultados = []

    for anio in anios_unicos:
        mask = anios == anio
        precios_anio = precios[mask]
        meses_anio = meses_num[mask]

        precio_enero = float(precios_anio[meses_anio == 1][0])
        precio_diciembre = float(precios_anio[meses_anio == 12][0])

        r = evaluar_variacion(precio_enero, precio_diciembre, cifras=cifras)
        r["anio"] = anio
        resultados.append(r)

    resultados.sort(key=lambda r: r["er_delta_pct"])
    return resultados
