# digitos.py

## Fecha de cumpleaños en los dígitos de PI

### Recibe

Dígito por dígito desde el teclado una Fecha en formato

    DD MM AA

### Notas

Cada dígito que se ingresa se checa que sea posible esa fecha.

Una vez ingresada la fecha "nos lleva" hasta el lugar de PI donde esos seis números estén.

La animación empieza por recorrer los primeros dígitos de PI (3.141592...) luego acelera al punto que no distinguimos qué dígitos aparecen y empieza a frenar en los últimos 1000 dígitos antes de la fecha hasta detenerse en ella.

### Dependencias

**Se necesita el archivo "data/out1000.csv" descomprimido con 7zip para poder ejecutar el script**

Los siguientes módulos son requeridos:

#### Tkinter

    pip install tkinter

### Instrucciones:

Definir VARIABLES GENERALES (líneas 50 y 51) y el archivo de imagen de fondo (línea 99) en el código y ejecutar en un entorno de **python 2.7+**:

    python digitos.py
