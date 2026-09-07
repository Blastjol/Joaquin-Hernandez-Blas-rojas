# INFORME DEL TRABAJO Y RESPUESTA DE LAS PREGUNTAS 
**Integrantes:**   
Blas Emilio Rojas Diaz  
Joaquin Alonso Hernandez Castro

## PREGUNTAS

### A1: Redondea a 2 cifras signifi cativas los precios que vayas a usar. Para cada uno calcula su error absoluto y su error relativo. ¿Qué mes quedó con el mayor error relativo al redondear?

El mes que queda con el mayor error relativo al redondear es abril de 2022, 
siendo este superior por mucho al resto de meses
teniendo un valor real de 815.12CLP, al aproximarlo nos queda 820.00CLP
Un error absoluto de 4.88 CLP
Un error relativo porcentual de 0.60%

### A2. Evaluación entre dos puntos (una compra-venta).
Elige un mes de compra y uno de venta. Con M = 1.000.000 y las tasas aproximadas: calcula USD = M / P_compra (división), pesos_fi nal = USD × P_venta (multiplicación) y G = pesos_fi nal − M (resta). Propaga el error: suma los relativos en la compra y la venta, pásalos a error absoluto y arrástralos a la ganancia. Entrega la ganancia como valor ± error y su error porcentual.



### A3. Cancelación (dos meses casi iguales).
Aca comparamos diciembre 2022 contra diciembre 2023, se ocuparon 3 cifras significaticas, por tanto el 875,66 de diciembre 2022 quedo en 876, lo que da un error absoluto de 0,34. Ahora viendo a diciembre 2023, que corresponde a 874,67 este queda en 875, que da un error absoluto de 0,33. Si se restan para poder ver la diferencia de precio, nos da -1, si se suman los 2 errores absolutos nos da 0,67.
En conclusion el margen error propagado total es de 0.67 tanto para arriba como hacia abajo con una diferencia de -1 peso.





### A4. Anualidad (variación enero→diciembre).
Aca se calculo la diferencia de enero y diciembre de cada año con 2 cifras significativas y se ordenaron del menor error porcentual al mayor error porcentual.  
  En 2025 el precio cayo con 80 con un error de 4.60, tuvo error relativo de 5.8  
En 2024 el precio subió con 70 pesos con un error de 4.31, tuvo un error relativo de 6.2  
En 2023 el precio subió con 40 pesos con un error de 8.33, tuvo un error relativo de 20.8  
En 2022 el precio subió con 60 pesos con un error de 6.39, tuvo un error relativo de 10.6  

Como se comento anteriormente, el error relativo mas alto corresponde al año 2023, por tanto, este es elñ año en que menos podemos confiar en los datos del codigo.



### A5. Mejor compra y mejor venta.  
Buscamos el mes mas barato y mas caro del dataset. El mas barato fue en febrero 2023 a 798.26, en cambio, lo mas caro fue en enero 2025 con 1000.76.

Rentabilidad obtenida: 25.0% ± 0.37%

Análisis de incertidumbre: Esta conclusión sobrevive holgadamente al error. La ganancia real que genera el mercado (un 25% de rendimiento) es inmensamente superior al pequeño error propagado por la incertidumbre de la máquina (solo un 0.37%). Por lo tanto, la recomendación de comprar en ese mínimo y vender en ese máximo es totalmente sólida y matemáticamente irrefutable, ya que el margen de error jamás podría alcanzar ni opacar semejante diferencia de precio.



### B1. Cifras significativas = mantisa corta
 
En punto flotante, la mantisa almacena exclusivamente los dígitos significativos de un número, determinando su precisión. Restringir un valor a 2 cifras significativas es el equivalente directo a tener una mantisa con pocos bits: al agotarse el espacio, el sistema se ve obligado a truncar o redondear, perdiendo resolución.

**Cálculo del error con 1000.76 a 3 cifras:**  
- Valor real: $1000.76$ (o $1.00076 \times 10^3$)  
- Valor almacenado (3 cifras):** $1.00 \times 10^3$ (equivale a $1000$)  
- Error de representación: $|\text{Valor Real} - \text{Valor Almacenado}|$  
- Error absoluto: 1000.76 - 1000 = 0.76


### B2. La ida y vuelta que no vuelve.
Idealmente se supone que si tomamos un monto (1000000) y lo transofrmamos dos veces deberiamos llegar al mismo monto, esto no es asi, debido a que siemopre hay una diferencia  

Si usamos float64, esa diferencia es casi invisible y microscópica, por lo que las matemáticas inversas funcionan casi perfecto.  
Pero si obligamos al computador a usar float32, el error se nota harto y la diferencia sube. Esto pasa porque al dividir los precios, la máquina tiene que cortar decimales a la fuerza, y esa "basura" se va acumulando de tal forma que ya no te deja recuperar tu saldo exacto, esto siendo casi aleatorio y no dependiendo del mes de del dolar.   

### B4. Cancelación en la máquina.

Hicimos la resta de 874,67 menos 875,66 directamente en Python para ver qué pasaba. Usando datos de 64 bits nos da -0.9900000000000091. Logra guardar como 14 cifras buenas. Pero si lo forzamos a 32 bits, nos da -0.989990234375, En float64, la mantisa más larga nos permite conservar cerca de 15 a 17 cifras significativas, arrastrando consigo mismo una basura al final. En float32, la memoria es mucho más corta unos 7 bits de precision (la mitad del otro). Como restamos dos números casi iguales, los bits importantes se cancelan entre sí y la máquina se ve obligada a rellenar el espacio restante con ceros o números inexactos, dejándonos con apenas 4 o 5 cifras significativas realmente válidas.  

Su relacion con A3 es que va literal de la mano, ya que es el mismo ejemplo de restar dos numeros casi exactos teniendo una perdida de datos de bits haciendo que la diferencia real sea tan chica que se ve opacada por los redondeos de la maquina.  







