# JOAQUIN HERNANDEZ Y BLAS ROJAS
# Aca se cargan los datos del csv y se devuelven en arrays de numpy listos para usar.

import os
import numpy as np
import matplotlib.pyplot as plt

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
    etiquetas = etiquetas_periodo(anios, meses_num)
    
    print(f"Se cargaron {len(precios)} registros.")
    
    # Crear carpeta graficos si no existe
    dir_graficos = os.path.join(os.path.dirname(__file__), "..", "graficos")
    os.makedirs(dir_graficos, exist_ok=True)
    
    # Gráfico 1: Serie mensual del dólar
    plt.figure(figsize=(10, 5))
    plt.plot(etiquetas, precios, color="#1f6feb", linewidth=1.6)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel("CLP por USD")
    plt.title("Dolar observado SII Promedio Mensual (2022-2025)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, "1_serie_mensual.png"), dpi=140)
    plt.close()
    print("Gráfico 1 generado exitosamente.")