# JOAQUIN HERNANDEZ Y BLAS ROJAS
# Aca se cargan los datos del csv y se devuelven en arrays de numpy listos para usar.

import os
import numpy as np

RUTA_POR_DEFECTO = os.path.join(
    os.path.dirname(__file__), "..", "data", "dolar_observado_sii_2022_2025.csv"
)

def cargar_serie(ruta=RUTA_POR_DEFECTO):
    # Carga el csv con np.genfromtxt, saltando la primera fila (encabezado original)
    # y asignando nuestros propios nombres de columnas.
    datos = np.genfromtxt(
        ruta,
        delimiter=",",
        skip_header=1,
        dtype=None,
        encoding="utf-8",
        names=["anio", "mes", "mes_num", "precio"],
    )

    anios = datos["anio"].astype(int)
    meses_num = datos["mes_num"].astype(int)
    nombres_mes = datos["mes"].astype(str)
    precios = datos["precio"].astype(np.float64)

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
    print(f"Se cargaron {len(precios)} registros.")
    print("Primeros 3:", list(zip(anios[:3], nombres_mes[:3], precios[:3])))
    print("Ultimos 3:", list(zip(anios[-3:], nombres_mes[-3:], precios[-3:])))