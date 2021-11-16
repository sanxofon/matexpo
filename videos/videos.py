# Author Santiago Chávez Novaro
# Player de videos de toros
# Python 3.8+

import vlc
import time
import keyboard

# Variables Generales
tiempomax = 30 # En segundos, aproximados, el tiempo de espera en "idle" para que se corra la animación "z"

class VLC:
    def __init__(self):
        # self.vlist = ['./videos/video0.mp4','./videos/video1.mp4','./videos/video2.mp4']
        self.vlist = {
            'w':'./videos/HD_transicion_inv.mp4',
            'x':'./videos/HD_transicion.mp4',
            'y':'./videos/HD_direc_A.mp4',
            'z':'./videos/HD_direc_B.mp4',
            '0':'./videos/4K_K23.mp4',
            '1':'./videos/4K_K25.mp4',
            '2':'./videos/4K_K27.mp4',
            '3':'./videos/4K_K32.mp4',
            '4':'./videos/4K_K35.mp4',
            '5':'./videos/4K_K37.mp4',
            '6':'./videos/4K_K52.mp4',
            '7':'./videos/4K_K53.mp4',
            '8':'./videos/4K_K57.mp4',
            '9':'./videos/4K_K72.mp4',
            'a':'./videos/4K_K73.mp4',
            'b':'./videos/4K_K75.mp4',
        }
        self.tabla = {
            '23':'0',
            '25':'1',
            '27':'2',
            '32':'3',
            '35':'4',
            '37':'5',
            '52':'6',
            '53':'7',
            '57':'8',
            '72':'9',
            '73':'a',
            '75':'b',
        }

        instance = vlc.Instance()
        self.player = instance.media_player_new()
        self.player.set_fullscreen(True)
        # self.playing = set([1,2,3,4]) # ??
        self.play = False
        self.current = -1

    def playVideo(self,i):
        # print("Play video",i)
        self.current = i
        self.player.set_mrl(self.vlist[i])
        self.player.play()
        self.play = True

    def is_playing(self):
        return self.player.is_playing()


# Variables internas, no modificar
salir = False
canPlay = True
memoria = ['',''] # Aquí se guardan las entradas del teclado (dos números entre [2,3,5,7])

def pressN(e):
    global canPlay,memoria
    if e.name=='esc':
        global salir
        salir=True
        # print("set Salir")
        return

    if str(e.name) in ['2','3','5','7']:
        if memoria[0]!='': # Si ya se recibió el anterior
            if memoria[0]==str(e.name): # Si se recibe dos veces el mismo se resetea
                memoria=['','']
            else:
                memoria[1]=str(e.name)
            m = memoria[0]+memoria[1]
            
            if canPlay and memoria[0]+memoria[1] in player.tabla:
                canPlay = False
                player.playVideo(player.tabla[memoria[0]+memoria[1]])
                memoria=['','']
                time.sleep(1) # This may be obligatory
        else:
            memoria[0]=str(e.name)

        print(memoria)

def playW(e,q='w'):
    # Default de ida
    global canPlay
    canPlay = True
    player.playVideo(q)
    time.sleep(1) # This may be obligatory


# keyboard.on_press_key("esc", pressEsc) # Salir
keyboard.on_press(pressN)

# Create the object
# print("Create the object")
player = VLC()

# Play first video --> Not needed!
# playW(None)
tiempo = 0
while True:
    if salir:
        # print("Salir")
        break
    if player.is_playing():
        # Do nothing
        time.sleep(1) # Less CPU usage?
        tiempo = 0
    else:
        if player.current=='z': # Si se recibió 'Z'
            playW(None,'x')
        elif player.current=='x':
            playW(None,'y')
        elif player.current!='w':
            playW(None,'w')
        else:
            tiempo+=1
            if tiempo>tiempomax: # si ha pasado un tiempo en pausa muy largo
                tiempo = 0
                playW(None,'z')
            # print(tiempo,end='         \r')

        time.sleep(1) # This may be obligatory
