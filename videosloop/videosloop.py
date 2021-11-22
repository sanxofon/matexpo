# importing vlc module
import vlc
  
import time
import os
  
# creating a media player object
media_player = vlc.MediaListPlayer()
  
# creating Instance class object
player = vlc.Instance()
  
# creating a new media list
media_list = player.media_list_new()

path = r"./videos/"
lista = os.listdir(path)

for i in lista:

	# creating a new media
	media = player.media_new(path+i)
  
	# adding media to media list
	media_list.add_media(media)
  
# setting media list to the media player
media_player.set_media_list(media_list)
media_player.set_playback_mode(vlc.PlaybackMode.loop) 
  
# new media player instance
new = player.media_player_new()
new.set_fullscreen(True)

# setting media player to it
media_player.set_media_player(new)
  
# start playing video
media_player.play()

input("\n--- Apretar ENTER para terminar el programa ---\n\n")
# while True:
#     time.sleep(1)