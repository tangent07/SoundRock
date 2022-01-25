import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import ttk
import time
import threading
import mttkinter
from ttkthemes import themed_tk as tk
from pygame import mixer   #mixer class in pygame




root=tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')

# canvas=Canvas(root,width=550,height=500,bg='blue')
# canvas.pack()
# photo=PhotoImage(file='images/background.png')
# canvas.create_image(0,0,image=photo,anchor=NW)

mainframe=Frame(root)
mainframe.pack()
mainframe.config(background='#660066')





#root window contain -> leftframe,rightframe,middleframe
#leftframe-> the Listbax(playlist)
#rightframe -> topframe,middleframe,bottomframe

statusbar=Label(root,text='Welcome to Melody',relief=SUNKEN,anchor=W,font='Times 15 bold',fg='dark orange')
statusbar.pack(side=BOTTOM,fill=X)

#menubar
menubar=Menu(root)
root.config(menu=menubar)

#submenu
subMenu=Menu(menubar,tearoff=0)


playlist=[]

#playlist= contains the full path and the filename
#playlistbox= contains just the filename
#full_path and filename to play the music inside play_music function

def browse_file():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):   #f -> is the filename instead of path
    filename=os.path.basename(filename)  #only name will be displayed
    index=0
    playlistbox.insert(index, filename)
    playlistbox.pack()
    playlist.insert(index,filename_path)
    print(playlist)
    #print(playlistbox)
    index+=1



menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open",command=browse_file)
subMenu.add_command(label="Exit",command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody app','This is the Music Player build using Python')


subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About us",command=about_us)





mixer.init()   #initializing the mixer
#root.geometry('300x300')
root.title('Melody')
root.iconbitmap('images/win_image.ico')

leftframe=Frame(mainframe)
leftframe.pack(side=LEFT,padx=30)
leftframe.config(background='#ff9900')

playlistbox=Listbox(leftframe)
playlistbox.pack()

Addbtn=ttk.Button(leftframe,text="+ Add",command=browse_file)
Addbtn.pack(side=LEFT)


def del_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
    print(playlist)


delbtn=ttk.Button(leftframe,text="- Del",command=del_song)
delbtn.pack(side=LEFT)


rightframe=Frame(mainframe)
rightframe.pack()
rightframe.config(background='#4d0099')


topframe=Frame(rightframe)
topframe.pack()
topframe.config(background='#ff0066')

lengthlabel=ttk.Label(topframe,text="Total length : --:--")
lengthlabel.pack(pady=5)

currenttimelabel=ttk.Label(topframe,text="current length : --:--",relief=GROOVE)
currenttimelabel.pack(pady=5)

def show_details(play_song):
    #filelabel['text'] = " Playing Music -->" + ' ' + os.path.basename(play_it)

    file_data=os.path.splitext(play_song)  #it split the text in tuple with index 1 = mp3
    #print(file_data)

    if file_data[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length

    else:

        a=mixer.Sound(play_song)
        total_length=a.get_length()
        # print(total_length)

    min,sec=divmod(total_length,60)
    min=round(min)
    sec=round(sec)
    timeformat='{:02d}:{:02d}'.format(min,sec)
    print(timeformat)
    lengthlabel['text'] = " Total Length -" + ' ' +timeformat

    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    #mixer.music.get_busy()-> return false when we press the stop button (music stop playing)
    #continue->ignores all the statement below it.we check if music is paused or not
    global paused

    current_time=0
    while current_time<=t and mixer.music.get_busy():  #for stop button
        if paused:
            continue       #for pause button
        else:
            min,sec=divmod(current_time,60)
            min = round(min)
            sec = round(sec)
            timeformat = '{:02d}:{:02d}'.format(min, sec)
            currenttimelabel['text'] = " Current Time : " + ' ' + timeformat
            time.sleep(1)
            current_time +=  1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        #statusbar['text'] = "   Music Resume |~|"
        paused=False


    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            #print(play_it)
            mixer.music.load(play_it)    #filename as global variable
            mixer.music.play()
            statusbar['text']="Playing Music -> "+' '+os.path.basename(play_it)
            show_details(play_it)

        except:     #this is only for catching the error if file is not opened

            tkinter.messagebox.showerror('File Not Found','Melody could not find the File , Please check again')
           # print("well done ... its workin ")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "---->> Stopped Music <<----"


paused=False

def pause_music():
    global paused     #initializing pause button
    paused=True
    mixer.music.pause()
    statusbar['text'] = "  Music Paused -||-"


def rewind_music():
    play_music()
    statusbar['text'] = "  Music Rewinded ..."


muted=False

def mute_music():
    global muted

    if muted:    #unmute the music    (here muted=true)
        mixer.music.set_volume(70)
        volumeBtn.configure(image=volumePhoto)
        scale.set(31)
        muted=False
        statusbar['text'] = "Music Playing "

    else:  #mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted=True
        statusbar['text'] = "  Music Muted ..."

def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)
    #set_volume of mixer takes value only from 0 t0 1  example 0,0.1,0.54,0.55.0.99,1



middleframe=Frame(rightframe)
middleframe.pack(pady=30,padx=30)
middleframe.config(background='#ff9900')

playPhoto=PhotoImage(file="images/win_image2.png")
playBtn=Button(middleframe,image=playPhoto,command=play_music,bg='green')
#playBtn.pack(side=LEFT,padx=10)   #pack - a layout manager
playBtn.grid(row=0,column=0,padx=10)


stopPhoto=PhotoImage(file="images/stop.png")
stopBtn=Button(middleframe,image=stopPhoto,command=stop_music,bg='#E93610')
#stopBtn.pack(side=LEFT,padx=10)
stopBtn.grid(row=0,column=1,padx=10)

pausePhoto=PhotoImage(file="images/pause.png")
pauseBtn=Button(middleframe,image=pausePhoto,command=pause_music, bg='green')
#pauseBtn.pack(side=LEFT,padx=10)
pauseBtn.grid(row=0,column=2,padx=10)


#bottom frame for rewind,volume mute and scale etc

bottomframe=Frame(rightframe)     #second frame
bottomframe.pack(pady=30)
bottomframe.config(background='#ff9900')


rewindPhoto=PhotoImage(file="images/rewind.png")
rewindBtn=Button(bottomframe,image=rewindPhoto,command=rewind_music,bg='#10C3E9')
#pauseBtn.pack(side=LEFT,padx=10)
rewindBtn.grid(row=0,column=0)


mutePhoto=PhotoImage(file="images/mute.png")
volumePhoto=PhotoImage(file="images/volume.png")
volumeBtn=Button(bottomframe,image=volumePhoto,command=mute_music,bg='#10C3E9')
#pauseBtn.pack(side=LEFT,padx=10)
volumeBtn.grid(row=0,column=2)


#scale is a function
scale=Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol,bg='#2A6976')
scale.set(31)
mixer.music.set_volume(30)
scale.grid(row=0,column=1,padx=20,pady=10)



def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
