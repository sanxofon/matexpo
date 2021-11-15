# videos.py

## Player de videos para expo

### Recibe

 - 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b => Para los videos 4K_K*.mp4
 - z => para la secuencia: HD_direc_A, HD_transicion, HD_direc_B

### Notas

 - Al principio y al final se reproduce el video HD_transicion_inv y se pausa al final esperando entrada de usuario (también se podría poner un video en loop)

### Dependencias

Los siguientes módulos son requeridos:

#### vlc

       pip install python-vlc

#### keyboard

       pip install keyboard

### Instrucciones

En un entorno de **python 3.8+**:

    python videos.py



# ciudad.py

## Ciudad de los números

### Recibe

21 números en total.
- primeros 7 son el primer edificio
- segundos 7 son el segundo edificio
- terceros 7 son el tercer edificio

### Notas

Cada dígito se lee en la tabla de los primeros 9 números primos:
- 2, 3, 5, 7, 9, 11, 13, 17, 19

Siempre que se detecta un cambio se vuelve a dibujar el canvas completo

### Dependencias

Los siguientes módulos son requeridos:

#### PySerial

    pip install pyserial

#### Tkinter

    pip install tkinter

#### Pillow

    pip install pillow

### Instrucciones:

Definir VARIABLES GENERALES en el código y ejecutar en un entorno de **python 2.7+**:

    python videos.py


### ToDo

- [ ] Recibe un numero entre [2,3, 5, 7] lo "memoriza" y "espera el siguiente"
- [ ] Cada cierto tiempo de espera se manda la secuencia de **z** como *demo* de videojuego.
