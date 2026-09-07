#JOAQUIN HERNANDEZ Y BLAS ROJAS
#respuesta a preguntas B1, B2 y B4
import numpy as np
from cargar_datos import cargar_serie
from errores import redondear_cifras_significativas, error_absoluto
import os
import matplotlib.pyplot as plt
from cargar_datos import etiquetas_periodo

def demo_b1():
    """Cifras significativas = mantisa corta."""
    valor = 1000.76
    aprox_3 = redondear_cifras_significativas(valor, 3)
    ea = error_absoluto(valor, aprox_3)
    return {"valor": valor, "aprox_3_cifras": float(aprox_3), "error_absoluto": float(ea)}


def ida_y_vuelta(monto, precios, dtype=np.float64):
    # Convertimos a numpy array con el dtype indicado

    precios = np.asarray(precios, dtype=dtype)
    monto_dtype = dtype(monto)

    usd = monto_dtype / precios
    monto_recuperado = usd * precios

    desviacion = monto_recuperado - monto_dtype
    return desviacion.astype(np.float64)  # se sube a float64 solo para poder imprimir/graficar comodo


def demo_b4():
    #cancelacion en float32 vs float64: 874.67 - 875.66
    a64 = np.float64(874.67)
    b64 = np.float64(875.66)
    resultado_64 = a64 - b64

    a32 = np.float32(874.67)
    b32 = np.float32(875.66)
    resultado_32 = a32 - b32

    return {
        "float64": float(resultado_64),
        "float32": float(resultado_32),
        "diferencia_entre_dtypes": float(abs(float(resultado_64) - float(resultado_32))),
    }


if __name__ == "__main__":
    print("B1 ->", demo_b1())
    print("B4 ->", demo_b4())
    
    anios, meses_num, nombres_mes, precios = cargar_serie()
    etiquetas = etiquetas_periodo(anios, meses_num)
    monto = 1_000_000.0
    
    dev64 = ida_y_vuelta(monto, precios, dtype=np.float64)
    dev32 = ida_y_vuelta(monto, precios, dtype=np.float32)
    print("B2 -> desviacion maxima float64:", np.max(np.abs(dev64)))
    print("B2 -> desviacion maxima float32:", np.max(np.abs(dev32)))

    # Gráfico 5: Deriva ida y vuelta
    dir_graficos = os.path.join(os.path.dirname(__file__), "..", "graficos")
    os.makedirs(dir_graficos, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.plot(etiquetas, dev64, marker="o", markersize=3, color="#17becf")
    ax1.set_title("Deriva ida y vuelta (pesos->USD->pesos) — float64")
    ax1.grid(alpha=0.3)
    ax2.plot(etiquetas, dev32, marker="o", markersize=3, color="#e377c2")
    ax2.set_title("Deriva ida y vuelta (pesos->USD->pesos) — float32")
    ax2.set_xticks(np.arange(len(etiquetas)))
    ax2.set_xticklabels(etiquetas, rotation=90, fontsize=7)
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, "5_deriva_punto_flotante.png"), dpi=140)
    plt.close()
    print("Gráfico 5 generado exitosamente.")