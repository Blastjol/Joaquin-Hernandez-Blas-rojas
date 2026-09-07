# JOAQUIN HERNANDEZ Y BLAS ROJAS
# Aca se cargan los datos del csv y se devuelven en arrays de numpy listos para usar.

import os
import numpy as np

RUTA_POR_DEFECTO = os.path.join(
    os.path.dirname(__file__), "..", "data", "dolar_observado_sii_2022_2025.csv"
)

NOMBRES_MES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

def cargar_serie(ruta=RUTA_POR_DEFECTO):
    # Carga el CSV con np.genfromtxt, saltando encabezado y la columna de texto de los meses
    matriz_precios = np.genfromtxt(
        ruta,
        delimiter=",",
        skip_header=1,
        usecols=(1, 2, 3, 4) 
    )

    # Aplanamos la matriz por columnas ('F') para que los precios queden en orden cronológico (todos los meses del 2022, luego 2023, etc.)
    precios = matriz_precios.flatten('F')

    anios = np.repeat([2022, 2023, 2024, 2025], 12)
    meses_num = np.tile(np.arange(1, 13), 4)
    nombres_mes = np.tile(NOMBRES_MES, 4)

    return anios, meses_num, nombres_mes, precios

def etiquetas_periodo(anios, meses_num):
    # Genera etiquetas cortas tipo 'Ene-22' para graficar en el eje X.
    abreviaturas = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic",
    }
    return np.array(
        [f"{abreviaturas[m]}-{str(a)[2:]}" for a, m in zip(anios, meses_num)]
    )

if __name__ == "__main__":
    anios, meses_num, nombres_mes, precios = cargar_serie()
    print(f"Se cargaron {len(precios)} registros cronológicos.")
    print("Primeros 3:", list(zip(anios[:3], nombres_mes[:3], precios[:3])))
    print("Últimos 3:", list(zip(anios[-3:], nombres_mes[-3:], precios[-3:])))