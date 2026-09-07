# La ganancia que se evapora

Cancelación y propagación del error con el Dólar Observado del SII (2022–2025)

Universidad Católica del Maule — Laboratorio Evaluado 1

## Autores

- Blas Rojas
- Joaquín Hernández

## Descripción

Este proyecto analiza cómo el redondeo a pocas cifras significativas (simulando la pérdida de precisión de punto flotante) afecta los cálculos financieros de comprar y vender dólares. Usando el dataset del Dólar Observado del SII (2022-2025), se calcula el error absoluto y relativo de cada precio, se propaga ese error a través de las operaciones de compra, venta y ganancia, y se estudia el efecto de cancelación que ocurre al restar dos meses con precios muy parecidos. El objetivo final es determinar, con respaldo numérico, en qué meses conviene comprar y vender, y en qué casos la diferencia calculada es demasiado incierta como para sacar una conclusión.

## Estructura del Repositorio

```
problema2-dolar-sii/
├── README.md
├── INFORME.md                             <- Respuestas A1-A5, B1-B4
├── requirements.txt                       <- numpy, matplotlib
├── data/
│   └── dolar_observado_sii_2022_2025.csv
├── src/
│   ├── cargar_datos.py                    <- Carga el CSV con numpy
│   ├── errores.py                         <- Redondeo, error absoluto, relativo y propagación
│   ├── anualidad.py                       <- Variación interanual y su error
│   └── punto_flotante.py                  <- Deriva numérica float32 vs float64
└── graficos/                              <- PNG generados y tabla de errores
    └── evaluacion_errores.csv
```

## Instrucciones de Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Los scripts deben ejecutarse desde la raíz del proyecto:

```bash
python src/cargar_datos.py
python src/errores.py
python src/anualidad.py
python src/punto_flotante.py
```

Los resultados (gráficos y tablas) quedan guardados en `graficos/`.


Resultados y conclusión

Ver [`INFORME.md`](./INFORME.md) para el detalle de cada pregunta (A1-A5,
B1-B4) y la conclusión final sobre cuándo conviene comprar y vender dólares.
