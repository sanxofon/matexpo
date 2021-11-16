# coding: utf-8
# Author Santiago Chávez Novaro
# Ciudad de los números
# Python 2.7+

import serial
from Tkinter import Tk, Label, Canvas, StringVar, PhotoImage
from PIL import ImageTk, Image
import time
import sys

from random import randint

"""
    CONTROLES ASIGNADOS:
         ______________________________________________
        |                                              |
        |  RECIVE DESDE SERIAL                         |
        |     21 números en total                      |
        |       primeros 7 son el primer edificio      |
        |       segundos 7 son el segundo edificio     |
        |       terceros 7 son el tercer edificio      |
        |     Cada dígito se lee en la tabla de        |
        |       los primeros 9 números primos:         |
        |         2, 3, 5, 7, 9, 11, 13, 17, 19        |
        |     Siempre que se detecta un cambio se      |
        |       vuelve a dibujar el canvas completo    |
        |______________________________________________|
 
    INSTRUCCIONES:
        
        1. Definir VARIABLES GENERALES de Desarrollo o Producción en código (VER __init__ ABAJO)

        2. Ejecutar el programa con el acceso directo que se encuentra en la misma carpeta.
            2.1. Ejecutar desde consola:
                python ciudad.py

"""

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class ciudad(object):
    def __init__(self, port, baud, fullscreen=1, smallscreen=0, debuguear=0):
        self.port = port
        self.baud = baud
        self.fullscreen = fullscreen
        self.smallscreen = smallscreen
        self.debuguear = debuguear
        self.memdatos = ''

    def iniciar(self, master):
        ######### VARIABLES GENERALES #########
        self.velocidad = 100 #Milisegundos
        self._job = None
        self.res = None
        #############iniciar##########################

        self.master = master
        self.master.configure(background='black')
        # self.master.wm_attributes('-transparentcolor','blue')

        if self.fullscreen>0:
            # Full screen
            if self.debuguear:
                print('W:',root.winfo_screenwidth())
                print('H:',root.winfo_screenheight())
            master.overrideredirect(True)
            master.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
            master.focus_set()  # <-- move focus to this widget
            # Otra opción
            # master.attributes('-fullscreen', True)
        else:
            master.geometry("%dx%d+0+0" % (master.winfo_screenwidth()-16, master.winfo_screenheight()-80))

        master.title(u"Ciudad de los números")

        master.bind("<Escape>", lambda e: e.widget.quit()) # Python 2

        # Background MASCARILLA
        bgfil = ImageTk.PhotoImage(Image.open("imagen/fondoCiudadNumeros"+("ch" if self.smallscreen else "")+".png"))
        bglabel = Label(master, image=bgfil)
        bglabel.place(x=0, y=0, relwidth=1, relheight=1)
        bglabel.image = bgfil

        self.bgcolor = '#1D1D1B'
        if self.debuguear:
            self.bgcolor = '#FF0000' # Test

        self.primos = [0,2,3,5,7,11,13,17,19,23]
        self.images = [
            "imagen/white",
            "imagen/edificio-1","imagen/edificio-2","imagen/edificio-3",
            "imagen/edificio-4","imagen/edificio-5","imagen/edificio-6",
            "imagen/edificio-7","imagen/edificio-8","imagen/edificio-9",
            "imagen/edificioTop"
        ]

        self.cols = [] # Guarda los labels de cada piso
        self.coli = [] # Guarda las imagenes de cada piso
        self.colr = [] # Guarda los labels de los resultados de cada columna

        topy = 0.133    # Pos top
        ma = 0.02       # Margen superior
        hr = 0.105       # Altura de la fila
        colx = [0.021,0.354,0.6873]
        rowy = [0.783, 0.678, 0.573, 0.468, 0.363, 0.258, 0.153] # De abajo a arriba
        coliy = [0.758, 0.653, 0.549, 0.445, 0.341, 0.237, 0.133, 0.032] # De abajo a arriba

        # Columnas de Numeros
        for c in range(3):
            self.cols.append([])
            self.coli.append([])
            for r in range(7):
                # Define los lbl de cada piso
                nu = [
                    (colx[c],rowy[r]), # Se invierte el orden de las posiciones para ir de abajo a arriba
                    "", #str(c)+"x"+str(r),
                    StringVar(),
                    None
                ]
                nu[2].set(nu[1])
                nu[3]=Label(master, textvariable=nu[2], bg=self.bgcolor, fg="#eee", width=4, justify="center", font="Roboto 28 bold")
                self.cols[c].append(nu)

                #imagen de cada piso
                im = [
                    (colx[c]+0.18,coliy[r]),
                    self.images[0]+("ch" if self.smallscreen else "")+".png",
                    None,
                    None
                ]
                im[2] = ImageTk.PhotoImage(Image.open(im[1]))
                if self.debuguear:
                    im[3] = Label(master, font="Roboto 8", fg="red", text="Piso "+str(r+1), image=im[2], borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
                else:
                    im[3] = Label(master, image=im[2], borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
                im[3].image = im[2]
                self.coli[c].append(im)

            # Define lbl de resultado
            nu = [
                (colx[c]+0.002,0.902),
                "= 1", #+str(c),
                StringVar(),
                None
            ]
            nu[2].set(self.fillSpaces(nu[1],16,' '))
            nu[3]=Label(master, textvariable=nu[2], bg=self.bgcolor, fg="#eee", width=16, justify="left", font="Courier 30 bold")
            self.cols[c].append(nu)
            self.colr.append(nu)

            # Ultima imagen (azotea)
            im = [
                (colx[c]+0.18,coliy[7]),
                self.images[0]+("ch" if self.smallscreen else "")+".png",
                None,
                None
            ]
            im[2] = ImageTk.PhotoImage(Image.open(im[1]))
            im[3] = Label(master, image=im[2], borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
            im[3].image = im[2]
            self.coli[c].append(im)

        # Posiciona
        for c in range(3):
            for r in range(7):
                self.cols[c][r][3].place(relx=self.cols[c][r][0][0], rely=self.cols[c][r][0][1]) # Labels
                self.coli[c][r][3].place(relx=self.coli[c][r][0][0], rely=self.coli[c][r][0][1]) # Images
            self.colr[c][3].place(relx=self.colr[c][0][0], rely=self.colr[c][0][1]) # Result labels
            self.coli[c][7][3].place(relx=self.coli[c][7][0][0], rely=self.coli[c][7][0][1]) # Images (azotea)
        #######################################
        self._job = self.master.after(self.velocidad, self.onUpdate)


    def fillSpaces(self,t,n=16,q=' '):
        l=len(t)
        if l<n:
            t=t.rjust(n,q)
        return t

    def calcelUpdate(self,quien=''):
        if self._job is not None:
            self.master.after_cancel(self._job)
            self._job = None

    def onUpdate(self):
        self.calcelUpdate()

        # if self.port!=0:
        # Intenta leer del serial
        datos = None
        uart = serial.Serial(port=self.port, baudrate=self.baud, timeout=3)
        data = uart.readline() #.decode()
           # if not data:
           #    break
        datos=str(data).strip()
        uart.close()

        print("Datos crudos:",datos)
        if len(datos)==0 or len(datos)!=21 or datos==self.memdatos:
            datos = None
            # else:
            #     print("No data")
        # else:
        #     # Genera datos random
        #     ra = [0,9,99,999,9999,99999,999999,9999999,9999999]
        #     datos = None
        #     if randint(0,1)==0:
        #         datos = [
        #             str(randint(0,ra[randint(0,8)])).ljust(7,'0'),
        #             str(randint(0,ra[randint(0,8)])).ljust(7,'0'),
        #             str(randint(0,ra[randint(0,8)])).ljust(7,'0')
        #         ]
        #         time.sleep(1)
        if datos is not None:
            if self.debuguear:
                print("Datos a corregir:",datos)
            self.memdatos = datos
            #divide cada 7 caracteres
            n = 7
            datos = [datos[i:i+n] for i in range(0, len(datos), n)]
            for c in range(3):
                datos[c] = list(datos[c])
                m = 1
                for r in range(len(datos[c])):
                    n = self.primos[int(datos[c][r])]
                    if n>0:
                        if r==0:
                            fin = 'b'+("ch" if self.smallscreen else "")+'.png'
                        else:
                            fin = ("ch" if self.smallscreen else "")+'.png'
                        self.cols[c][r][2].set(str(n)+" x")
                        im = ImageTk.PhotoImage(Image.open(self.images[int(datos[c][r])]+fin))
                        self.coli[c][r][3].config(image = im)
                        self.coli[c][r][3].photo_ref = im # keep a reference
                        m*=n # Filtra por la tabla
                    else:
                        for rr in range(r,len(datos[c])):
                            datos[c][rr]='0'
                            if rr==0:
                                imurl = self.images[10]+"b"+("ch" if self.smallscreen else "")+".png"
                            elif r==rr:
                                imurl = self.images[10]+("ch" if self.smallscreen else "")+".png"
                            else:
                                imurl = self.images[0]+("ch" if self.smallscreen else "")+".png"
                            self.cols[c][rr][2].set(self.cols[c][rr][1])
                            im = ImageTk.PhotoImage(Image.open(imurl))
                            self.coli[c][rr][3].config(image = im)
                            self.coli[c][rr][3].photo_ref = im # keep a reference
                        break

                 # Poner azotea hasta arriba
                if self.primos[int(datos[c][6])]:
                    imurl = self.images[10]+("ch" if self.smallscreen else "")+".png"
                else:
                    imurl = self.images[0]+("ch" if self.smallscreen else "")+".png"
                im = ImageTk.PhotoImage(Image.open(imurl))
                self.coli[c][7][3].config(image = im)
                self.coli[c][7][3].photo_ref = im # keep a reference

                # Label de resultado por columna
                self.colr[c][2].set(self.fillSpaces("= "+'{:,}'.format(m),16,' '))


                datos[c] = "".join(datos[c])
            datos = "".join(datos)
            if self.debuguear:
                print("Datos corregidos:",datos)

        self._job = self.master.after(self.velocidad, self.onUpdate)

#######################
# VARIABLES GENERALES #
#######################
port = 'COM3'   # Puerto serial
baud = 9600     # Baudios. Velocidad de muestreo
fullscreen = 1  # Abrir en pantalla completa. Dev: 0, Prd: 1
smallscreen = 1 # Usa las imágenes pequeñas, para probar en una pantalla de laptop (1366x786px)
debuguear = 0   # Verbose. Muestra las tripas durante desarrollo. Permite probar el programa sin el Arduino

# Test de puertos seriales
listPorts = serial_ports()
if port not in listPorts:
    print("No se detecta el puerto del arduino: "+port)
    print("Lista de puertos disponibles: ["+", ".join(listPorts)+"]")
    print("Edite el nombre del puerto a partir de la línea 300 o habilite el modo debug para testear...")
    if debuguear: # or testeo:
        port=0
    else:
        exit(0)

root = Tk()
cu = ciudad(port,baud,fullscreen,smallscreen,debuguear);
cu.iniciar(root);
root.mainloop()
