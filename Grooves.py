import os
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from pygame import mixer


global stopped, paused
stopped = False
paused =  False
pressed = False

root = Tk()
mixer.init()
root.title("Grooves")
# root.geometry("360x480")

#lets define frames
frame = Frame(root)
frame.pack(padx = 10,pady=10)

#lets create an icon first
img = Image('photo',file='music-player.png')
root.call('wm','iconphoto',root._w,img)
#lets create a menu bar
menubar = Menu(root)
root.config(menu=menubar)
#lets create submenu file
def browse():
    global fname
    fname = filedialog.askopenfilename()
    filename = os.path.basename(fname)
    statusbar["text"] = filename + ' ' + 'Loaded'

def quit(event=None):
    root.destroy()

def about_us():
    tkinter.messagebox.showinfo('About Grooves','Welcome to Grooves Music app. \
                                This app is developed using python 3.5 by @karryp3775')
    statusbar["text"] = 'About Grooves'

submenu1 = Menu(menubar,tearoff=0)
submenu2 = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=submenu1)
menubar.add_cascade(label='Help',menu=submenu2)
submenu1.add_command(label="Open",command =browse)
submenu1.add_command(label='Exit',command = quit)
submenu2.add_command(label='About Us',command = about_us)

#lets create the play button
def play_music():
    global paused,stopped,pressed

    if pressed ==True: #when the music has been already playing
        mixer.music.pause()
        statusbar["text"] = 'Music paused'
        playbtn["image"] = playbtnimg
        pressed= False
        paused = True
        stopped = False
    else:
        pressed = True

    if paused==False and stopped==False:
        try:
            global fname
            mixer.music.load(fname)
            mixer.music.play()
            statusbar["text"] = 'Playing ' + os.path.basename(fname)
            pressed = True
            playbtn["image"] = pauseimg
        except:
            tkinter.messagebox.showerror('File not found','Grooves could not locate music file! Please try again!')
            statusbar["text"] = 'Use open under file menu to load music'
            pressed=False
    elif paused==True and stopped==False and pressed == True:
        mixer.music.unpause()
        statusbar["text"] = "Music resumed"
        playbtn["image"] = pauseimg
        paused = False

    elif paused==False and stopped==True:
        mixer.music.load(fname)
        mixer.music.play()
        stopped = False
        statusbar["text"] = 'Music playing from the start'
        playbtn["image"] = pauseimg


def pause_music():
    global paused,stopped
    paused = True
    stopped = False

    mixer.music.pause()
    statusbar["text"] = 'Music paused'

def stop_music():
    global stopped, paused,pressed
    stopped = True
    paused =  False
    pressed = False

    mixer.music.stop()
    statusbar["text"] = 'Music Stopped'
    playbtn["image"] = playbtnimg

playbtnimg = PhotoImage(file='play-button.png')
playbtn = Button(frame,image=playbtnimg,command = play_music)
playbtn.pack(side=LEFT,padx=10)

#lets create the stop button

stopimg = PhotoImage(file='stop.png')
stopbtn = Button(frame,image=stopimg,command=stop_music)
stopbtn.pack(side=LEFT,padx=10)

pauseimg = PhotoImage(file='pause.png')

#lets create a volume control
global muted,volbefore
muted = False
def set_vol(val):
    global muted
    vol = float(val)/100.0
    mixer.music.set_volume(vol)
    statusbar["text"] = 'Volume unmuted'
    soundbtn["image"] = unmuteimg
    muted = False

vol_ctrl = Scale(root,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
vol_ctrl.set(70)
vol_ctrl.pack(fill=X)

#lets create the mute button'

def mute_unmute():
    global muted
    global last_volume
    if muted:
        mixer.music.set_volume(last_volume*0.01)
        soundbtn.configure(image=unmuteimg)
        # vol_ctrl.set(last_volume)
        muted = False
    else:
        mixer.music.set_volume(0)
        soundbtn.configure(image=muteimg)
        last_volume = float(vol_ctrl.get())
        # vol_ctrl.set(0)
        muted= True



muteimg = PhotoImage(file='mute.png')
unmuteimg = PhotoImage(file='speaker.png')

soundbtn = Button(frame,image=unmuteimg,command=mute_unmute)
soundbtn.pack(side=LEFT,padx=10)


#lets create a status bar
statusbar = Label(root,text='Welcome to Grooves!',relief =SUNKEN,anchor=W)
statusbar.pack(side='bottom',fill=X)

#initiate the loop
root.mainloop()
