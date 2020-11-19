from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog
import pygame
from mutagen.mp3 import MP3
import time
import tkinter.ttk as ttk

root=Tk()
root.title("MyMp3")
root.geometry('500x400')

pygame.mixer.init()

my_songs=Listbox(root,width=70,bg="white",fg="green",selectbackground="blue")
my_songs.pack(pady=20)

frame_controls=Frame(root)
frame_controls.pack(pady=15)

img_play=Image.open("C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Images\\play.png")
img_stop=Image.open("C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Images\\stop.jpg")
img_rewind=Image.open("C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Images\\rewind.png")
img_foward=Image.open("C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Images\\Foward.png")
img_pause=Image.open("C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Images\\pause.png")

#resizing images

img_play=img_play.resize((32,32),Image.ANTIALIAS)
img_stop=img_stop.resize((32,32),Image.ANTIALIAS)
img_rewind=img_rewind.resize((32,32),Image.ANTIALIAS)
img_foward=img_foward.resize((32,32),Image.ANTIALIAS)
img_pause=img_pause.resize((32,32),Image.ANTIALIAS)

#CONVERTING IMAGES

img_play=ImageTk.PhotoImage(img_play)
img_stop=ImageTk.PhotoImage(img_stop)
img_rewind=ImageTk.PhotoImage(img_rewind)
img_foward=ImageTk.PhotoImage(img_foward)
img_pause=ImageTk.PhotoImage(img_pause)

global paused
paused=False

def pause():
    global paused
    if(paused==False):
        pygame.mixer.music.pause()
        paused=True
    else:
        pygame.mixer.music.unpause()
        paused=False

def play():


    song_playing=my_songs.get(ACTIVE)
    song_playing=f"C:/Users/faraz/PycharmProjects/Tkinter/MP3 Player/Music/{song_playing}.mp3"
    pygame.mixer.music.load(song_playing)
    pygame.mixer.music.play(loops=0)

    play_time()

    #UPDATE SLIDER TO POSITION
    slider_position=int(song_length)
    my_slider.config(to=slider_position,value=0)

def stop():
    pygame.mixer.music.stop()

def rewind():
    global next
    current_song=my_songs.curselection()
    if(current_song[0]!=0):
        current_song=current_song[0]-1
        song_to_be_played=my_songs.get(current_song)
        song=f"C:/Users/faraz/PycharmProjects/Tkinter/MP3 Player/Music/{song_to_be_played}.mp3"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #MOVING ACTIVE BAR IN PLAYLIST
        my_songs.selection_clear(0,END)
        my_songs.activate(current_song)
        my_songs.selection_set(current_song,last=None)


def foward():
    try:
        current_song=my_songs.curselection()
        current_song = current_song[0] + 1
        song_to_be_played = my_songs.get(current_song)
        song = f"C:/Users/faraz/PycharmProjects/Tkinter/MP3 Player/Music/{song_to_be_played}.mp3"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        # MOVING ACTIVE BAR IN PLAYLIST
        my_songs.selection_clear(0, END)
        my_songs.activate(current_song)
        my_songs.selection_set(current_song, last=None)
    except pygame.error:
        print("Increase Playlist to move foward")
#BUTTONS

btn_play=Button(frame_controls,image=img_play,command=play)
btn_stop=Button(frame_controls,image=img_stop,command=stop)
btn_rewind=Button(frame_controls,image=img_rewind,command=rewind)
btn_foward=Button(frame_controls,image=img_foward,command=foward)
btn_pause=Button(frame_controls,image=img_pause,command=pause)

btn_play.grid(row=0,column=0,padx=10)
btn_stop.grid(row=0,column=1,padx=10)
btn_rewind.grid(row=0,column=2,padx=10)
btn_foward.grid(row=0,column=3,padx=10)
btn_pause.grid(row=0,column=4,padx=10)

#CREATING MENU
my_menu=Menu(root)
root.config(menu=my_menu)

#ADDING SONG SUB-CATEGORY

def add_single_song():
    song=filedialog.askopenfilename(initialdir='C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Music',title="Choose A Song",filetypes=(("mp3 files","*.mp3"),))
    song=song.replace("C:/Users/faraz/PycharmProjects/Tkinter/MP3 Player/Music/","")
    song=song.replace(".mp3","")
    my_songs.insert(END,song)

def add_multiple_songs():
    songs=filedialog.askopenfilenames(initialdir="C:\\Users\\faraz\\PycharmProjects\\Tkinter\\MP3 Player\\Music",title="Choose Multiple Songs",filetypes=(("mp3 files","*.mp3"),))
    songs=list(songs)
    for i in range(len(songs)):
        songs[i]=songs[i].replace("C:/Users/faraz/PycharmProjects/Tkinter/MP3 Player/Music/","")
        songs[i]=songs[i].replace(".mp3","")
        my_songs.insert(END,songs[i])

add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist",command=add_single_song)
add_song_menu.add_command(label="Add multiple songs to playlist",command=add_multiple_songs)

Exit_menu=Menu(my_menu)
my_menu.add_cascade(label="Exit",menu=Exit_menu)
Exit_menu.add_command(label="Exit",command=root.quit)

def play_time():
    global song_length
    current_time=pygame.mixer.music.get_pos()

    current_song=my_songs.curselection()
    song=my_songs.get(current_song)
    song=f"C:/Users/faraz/PycharmProjects/Tkinter/MP3 Player/Music/{song}.mp3"
    #LOADING SONG
    song_load=MP3(song)
    song_length=song_load.info.length#LENGTH IN SECONDS
    full_time_song=time.strftime("%M:%S",time.gmtime(song_length))
    timeas=time.strftime("%M:%S",time.gmtime(current_time/1000))
    time_status_bar.config(text=f'{timeas} of {full_time_song}')
    my_slider.config(value=current_time/1000)
    print(f'current time:- {current_time/1000} of  {song_length}')
    time_status_bar.after(1000,play_time)


def slide(x):
    global song_length,time_my_slider,time_song_length
    time_my_slider=time.strftime("%M:%S",time.gmtime(my_slider.get()))
    time_song_length=time.strftime("%M:%S",time.gmtime(song_length))
    slider_label.config(text=f'{time_my_slider} of {time_song_length}')
    my_slider.config(to=song_length)



#Create a slider

my_slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
my_slider.pack(pady=20)

slider_label=Label(root,text="0")
slider_label.pack(pady=10)


time_status_bar=Label(root,text="",bd=1,relief=GROOVE,anchor=E)
time_status_bar.pack(fill=X,side=BOTTOM,ipady=2)



root.mainloop()