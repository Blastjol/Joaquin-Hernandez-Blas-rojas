#JOAQUIN HERNANDEZ Y BLAS ROJAS
#funciones de error vectorizadas con numpy, redondeamos 2 cifras significativas para todo, como pide el enunciado.

import numpy as np
import os
import matplotlib.pyplot as plt
from cargar_datos import cargar_serie, etiquetas_periodo


def redondear_cifras_significativas(valor, cifras=2):
    #convertimos a numpy array para poder usar log10 y floor de manera vectorizada
    valor = np.asarray(valor, dtype=np.float64)
    # Evita log(0)
    valor_seguro = np.where(valor == 0, 1, valor)
    exponente = np.floor(np.log10(np.abs(valor_seguro)))
    factor = 10.0 ** (cifras - 1 - exponente)
    redondeado = np.round(valor * factor) / factor
    return np.where(valor == 0, 0.0, redondeado)


def error_absoluto(valor_real, valor_aproximado):
    #Ea = | valor_verdadero - valor_aproximado |
    return np.abs(np.asarray(valor_real, dtype=np.float64) - np.asarray(valor_aproximado, dtype=np.float64))


def error_relativo(valor_real, ea):
    #Er (%) = (Ea / valor_verdadero) * 100
    valor_real = np.asarray(valor_real, dtype=np.float64)
    ea = np.asarray(ea, dtype=np.float64)
    return (ea / np.abs(valor_real)) * 100.0


def propagar_relativo_multiplicacion_division(er_a, er_b):
    #En multiplicacion o division, los errores relativos (%) se SUMAN.
    return np.asarray(er_a, dtype=np.float64) + np.asarray(er_b, dtype=np.float64)


def propagar_absoluto_suma_resta(ea_a, ea_b):
    #En suma o resta, los errores absolutos se SUMAN.
    return np.asarray(ea_a, dtype=np.float64) + np.asarray(ea_b, dtype=np.float64)


def relativo_a_absoluto(er_porcentual, valor):
    #Convierte un error relativo (%) de vuelta a un error absoluto, dado el valor.
    return (np.asarray(er_porcentual, dtype=np.float64) / 100.0) * np.abs(np.asarray(valor, dtype=np.float64))


def resumen_representacion(precios, cifras=2):
    # Convertimos a numpy array para poder usar log10 y floor de manera vectorizada
    aprox = redondear_cifras_significativas(precios, cifras)
    ea = error_absoluto(precios, aprox)
    er = error_relativo(precios, ea)
    return {
        "real": np.asarray(precios, dtype=np.float64),
        "aproximado": aprox,
        "error_absoluto": ea,
        "error_relativo_pct": er,
    }


def evaluar_operacion_compra_venta(monto, p_compra_real, p_venta_real, cifras=2):
    #flujo de pregunta A2, paso a paso, con redondeo y propagacion de error.
    # 1) Representacion con pocas cifras significativas
    p_compra_aprox = float(redondear_cifras_significativas(p_compra_real, cifras))
    p_venta_aprox = float(redondear_cifras_significativas(p_venta_real, cifras))

    ea_compra = float(error_absoluto(p_compra_real, p_compra_aprox))
    ea_venta = float(error_absoluto(p_venta_real, p_venta_aprox))

    er_compra = float(error_relativo(p_compra_real, ea_compra))
    er_venta = float(error_relativo(p_venta_real, ea_venta))

    # 2) USD = Monto / P_compra  (Monto se asume exacto, error relativo 0)
    usd = monto / p_compra_aprox
    er_usd = propagar_relativo_multiplicacion_division(0.0, er_compra)

    # 3) pesos_final = USD * P_venta
    pesos_final = usd * p_venta_aprox
    er_pesos_final = propagar_relativo_multiplicacion_division(er_usd, er_venta)
    ea_pesos_final = relativo_a_absoluto(er_pesos_final, pesos_final)

    # 4) Ganancia = pesos_final - Monto  (Monto exacto -> ea = 0)
    ganancia = pesos_final - monto
    ea_ganancia = propagar_absoluto_suma_resta(ea_pesos_final, 0.0)
    er_ganancia = error_relativo(ganancia, ea_ganancia) if ganancia != 0 else np.inf

    # 5) Rentabilidad = Ganancia / Monto * 100 (Monto exacto -> error relativo = er_ganancia)
    rentabilidad = (ganancia / monto) * 100.0
    er_rentabilidad = er_ganancia
    ea_rentabilidad = relativo_a_absoluto(er_rentabilidad, rentabilidad) if np.isfinite(er_rentabilidad) else np.inf

    return {
        "p_compra_real": p_compra_real, "p_compra_aprox": p_compra_aprox,
        "p_venta_real": p_venta_real, "p_venta_aprox": p_venta_aprox,
        "er_compra_pct": er_compra, "er_venta_pct": er_venta,
        "usd": usd, "pesos_final": pesos_final,
        "ea_pesos_final": ea_pesos_final, "er_pesos_final_pct": er_pesos_final,
        "ganancia": ganancia, "ea_ganancia": ea_ganancia, "er_ganancia_pct": er_ganancia,
        "rentabilidad_pct": rentabilidad, "ea_rentabilidad_pct": ea_rentabilidad,
    }


def evaluar_variacion(p_inicial_real, p_final_real, cifras=2):
    #redondeamos los precios a pocas cifras significativas
    p_inicial_aprox = float(redondear_cifras_significativas(p_inicial_real, cifras))
    p_final_aprox = float(redondear_cifras_significativas(p_final_real, cifras))

    ea_inicial = float(error_absoluto(p_inicial_real, p_inicial_aprox))
    ea_final = float(error_absoluto(p_final_real, p_final_aprox))

    delta_real = p_final_real - p_inicial_real
    delta_aprox = p_final_aprox - p_inicial_aprox
    ea_delta = propagar_absoluto_suma_resta(ea_inicial, ea_final)
    er_delta = error_relativo(delta_aprox, ea_delta) if delta_aprox != 0 else np.inf

    # ¿El intervalo [delta - ea, delta + ea] cambia de signo?
    limite_inf = delta_aprox - ea_delta
    limite_sup = delta_aprox + ea_delta
    signo_confiable = (limite_inf > 0) or (limite_sup < 0)

    return {
        "p_inicial_real": p_inicial_real, "p_inicial_aprox": p_inicial_aprox, "ea_inicial": ea_inicial,
        "p_final_real": p_final_real, "p_final_aprox": p_final_aprox, "ea_final": ea_final,
        "delta_real": delta_real, "delta_aprox": delta_aprox,
        "ea_delta": ea_delta, "er_delta_pct": er_delta,
        "intervalo": (limite_inf, limite_sup), "signo_confiable": signo_confiable,
    }


if __name__ == "__main__":
    print("963.44 a 2 cifras ->", redondear_cifras_significativas(963.44, 2))
    print("1000.76 a 3 cifras ->", redondear_cifras_significativas(1000.76, 3))
    
    # Cargar datos para graficar
    anios, meses_num, nombres_mes, precios = cargar_serie()
    etiquetas = etiquetas_periodo(anios, meses_num)
    dir_graficos = os.path.join(os.path.dirname(__file__), "..", "graficos")
    os.makedirs(dir_graficos, exist_ok=True)
    cifras = 2
    monto = 1_000_000.0

    # Gráfico 2: Variación mes a mes
    delta = np.diff(precios)
    r_ini = resumen_representacion(precios[:-1], cifras)
    r_fin = resumen_representacion(precios[1:], cifras)
    ea_delta = r_ini["error_absoluto"] + r_fin["error_absoluto"]
    colores = np.where(np.abs(delta) <= ea_delta, "#7a0808", "#41c541")
    plt.figure(figsize=(10, 5))
    plt.bar(etiquetas[1:], delta, color=colores)
    plt.errorbar(etiquetas[1:], delta, yerr=ea_delta, fmt="none", ecolor="black", elinewidth=0.8, capsize=2)
    plt.axhline(0, color="grey", linewidth=0.8)
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Variación mes a mes — rojo: |Variacion| <= error propagado (cancelación)")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, "2_variacion_mensual.png"), dpi=140)
    plt.close()

    # Gráfico 3: Error de representación
    r3 = resumen_representacion(precios, cifras)
    plt.figure(figsize=(10, 5))
    plt.bar(etiquetas, r3["error_relativo_pct"], color="#452c5c")
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Error de representación mensual a 2 cifras")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, "3_error_representacion.png"), dpi=140)
    plt.close()

    # Gráfico 4: Rentabilidad
    i_min = int(np.argmin(precios))
    rentabilidades, errores_rent = [], []
    for j in range(i_min + 1, len(precios)):
        r = evaluar_operacion_compra_venta(monto, precios[i_min], precios[j], cifras)
        rentabilidades.append(r["rentabilidad_pct"])
        errores_rent.append(r["ea_rentabilidad_pct"] if np.isfinite(r["ea_rentabilidad_pct"]) else 0.0)
    plt.figure(figsize=(10, 5))
    plt.bar(etiquetas[i_min + 1:], rentabilidades, color="#31708d")
    plt.errorbar(etiquetas[i_min + 1:], rentabilidades, yerr=errores_rent, fmt="none", ecolor="black", elinewidth=0.8, capsize=2)
    plt.axhline(0, color="grey", linewidth=0.8)
    plt.xticks(rotation=90, fontsize=7)
    plt.title(f"Rentabilidad de comprar en el mínimo ({etiquetas[i_min]}) y vender después")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, "4_rentabilidad_desde_minimo.png"), dpi=140)
    plt.close()

    # CSV de evaluación (Evaluación A3 a 3 cifras)
    ruta_csv = os.path.join(dir_graficos, "evaluacion_errores.csv")
    with open(ruta_csv, "w", encoding="utf-8") as f:
        f.write("tipo,periodo_inicial,periodo_final,valor_real,valor_aprox,error_absoluto,error_relativo_pct,signo_confiable\n")
        
        def _fmt(x):
            if isinstance(x, bool): return str(x)
            if not np.isfinite(x): return "inf"
            return f"{float(x):.2f}"
            
        # 1. A3 (cancelacion Dic-22 vs Dic-23 a 3 cifras)
        r_a3 = evaluar_variacion(875.66, 874.67, cifras=3)
        f.write(f"cancelacion_a3,Dic-22,Dic-23,{_fmt(r_a3['delta_real'])},{_fmt(r_a3['delta_aprox'])},{_fmt(r_a3['ea_delta'])},{_fmt(r_a3['er_delta_pct'])},{_fmt(r_a3['signo_confiable'])}\n")

        # 2. Representación mensual (a 2 cifras)
        r_mensual = resumen_representacion(precios, cifras)
        for i in range(len(precios)):
            f.write(f"representacion_mensual,{etiquetas[i]},,{_fmt(precios[i])},{_fmt(r_mensual['aproximado'][i])},{_fmt(r_mensual['error_absoluto'][i])},{_fmt(r_mensual['error_relativo_pct'][i])},\n")

        # 3. Variación mes a mes
        for i in range(1, len(precios)):
            r_var = evaluar_variacion(precios[i - 1], precios[i], cifras)
            f.write(f"variacion_mes_a_mes,{etiquetas[i - 1]},{etiquetas[i]},{_fmt(r_var['delta_real'])},{_fmt(r_var['delta_aprox'])},{_fmt(r_var['ea_delta'])},{_fmt(r_var['er_delta_pct'])},{_fmt(r_var['signo_confiable'])}\n")
            
        # 4. Variación anual (Enero a Diciembre de cada año)
        anios_unicos = sorted(set(anios.tolist()))
        for anio in anios_unicos:
            mask = anios == anio
            precios_anio = precios[mask]
            meses_anio = meses_num[mask]
            precio_enero = float(precios_anio[meses_anio == 1][0])
            precio_diciembre = float(precios_anio[meses_anio == 12][0])
            r_anio = evaluar_variacion(precio_enero, precio_diciembre, cifras)
            f.write(f"variacion_anual,Ene-{str(anio)[2:]},Dic-{str(anio)[2:]},{_fmt(r_anio['delta_real'])},{_fmt(r_anio['delta_aprox'])},{_fmt(r_anio['ea_delta'])},{_fmt(r_anio['er_delta_pct'])},{_fmt(r_anio['signo_confiable'])}\n")
            
    print("Gráficos 2, 3, 4 y tabla de evaluación (completa) generados exitosamente.")