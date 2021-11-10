#video4.py

import vlc
import time
import keyboard

class VLC:
    def __init__(self):
        # self.vlist = ['.\\videos\\video0.mp4','.\\videos\\video1.mp4','.\\videos\\video2.mp4']
        self.vlist = {
            'w':'.\\videos\\HD_transicion_inv.mp4',
            'x':'.\\videos\\HD_transicion.mp4',
            'y':'.\\videos\\HD_direc_A.mp4',
            'z':'.\\videos\\HD_direc_B.mp4',
            '0':'.\\videos\\4K_K23.mp4',
            '1':'.\\videos\\4K_K25.mp4',
            '2':'.\\videos\\4K_K27.mp4',
            '3':'.\\videos\\4K_K32.mp4',
            '4':'.\\videos\\4K_K35.mp4',
            '5':'.\\videos\\4K_K37.mp4',
            '6':'.\\videos\\4K_K52.mp4',
            '7':'.\\videos\\4K_K53.mp4',
            '8':'.\\videos\\4K_K57.mp4',
            '9':'.\\videos\\4K_K72.mp4',
            'a':'.\\videos\\4K_K73.mp4',
            'b':'.\\videos\\4K_K75.mp4',
        }

        instance = vlc.Instance()
        self.player = instance.media_player_new()
        self.player.set_fullscreen(True)
        self.playing = set([1,2,3,4]) # ??
        self.play = False
        self.current = -1

    def playVideo(self,i):
        print("Play video",i)
        self.current = i
        self.player.set_mrl(self.vlist[i])
        self.player.play()
        self.play = True

    def is_playing(self):
        return self.player.is_playing()

# General Variables
salir = False
canPlay = True

def pressN(e):
    global canPlay
    if e.name=='esc':
        global salir
        salir=True
        print("set Salir")
        return
    if e.name in player.vlist and canPlay:
        canPlay = False
        player.playVideo(e.name)
        time.sleep(1) # This may be obligatory

def playW(e,q='w'):
    # Default de ida
    global canPlay
    canPlay = True
    player.playVideo(q)
    time.sleep(1) # This may be obligatory


# keyboard.on_press_key("esc", pressEsc) # Salir
keyboard.on_press(pressN)

# Create the object
print("Create the object")
player = VLC()

# Play first video --> Not needed!
# playW(None)

while True:
    if salir:
        print("Salir")
        break
    if player.is_playing():
        # Do nothing
        time.sleep(1) # Less CPU usage?
    else:
        if player.current=='z':
            playW(None,'x')
        elif player.current=='x':
            playW(None,'y')
        elif player.current!='w':
            playW(None)
        time.sleep(1) # This may be obligatory
