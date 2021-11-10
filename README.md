# videos.py

## Player de videos para expo

### Recibe

 - 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b => Para los videos 4K_K*.mp4
 - z => para la secuencia: HD_direc_A, HD_transicion, HD_direc_B

### Notas

 - Al principio y al final se reproduce el video HD_transicion_inv y se pausa al final esperando entrada de usuario (también se podría poner un video en loop)

### Dependencias

Los siguientes módulos son requeridos:

 - **vlc**

       pip install python-vlc

 - **keyboard**

       pip install keyboard

### Ejecutar

En un entorno de python 3.8+

    python videos.py
