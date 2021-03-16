'''
Created on 02.03.2021

@author: sven
'''

import tkinter
import sys

screen = None
number = 6
position = 3
songnumber = 0
rows = 24


songlist = [["Titel1", "Interpret1", ["Strophe1","Strophe2","Strophe3"]],
            ["Titel2", "Interpret2", ["Strophe1","Strophe2","Strophe3"]],
            ["Titel3", "Interpret3", ["Strophe1","Strophe2","Strophe3"]],
            ]
songtext = ''




def updateStatus():
    fill = 'white'
    screen.delete('dots')
    for dot in range(1, number+1):
        if position == dot:
            fill = 'black'
        else:
            fill = 'white'
        screen.create_oval(20+(20*dot),20,40+(20*dot),40, fill=fill, tag="dots")
    screen.create_text(1280/2, 30, text=songlist[songnumber][0] + " - " +  songlist[songnumber][1], font=("Courier", 20, 'bold'), tag="dots")
# Up
def up(e):
    global position
    position -= 1
    updateStatus()

# Down
def down(e):
    global position
    position += 1
    updateStatus()

# Enter
def enter(e):
    print(e)

# Escape
def escape(e):
    sys.exit()


def parseSongFile():
    pass


def loadSongs():
    global songtext
    with open('pi.txt') as songtextfile:
        for line in songtextfile.readlines():
            songtext += line

def createScreen():
    text = ''
    for row in songlist[songnumber][2]:
        text += row + 2*'\n'
        
    screen.create_text(20, 80, text=text, font=("Courier", 20), anchor='nw')
    

if __name__ == '__main__':
    app = tkinter.Tk()
    app.geometry("1280x720+100+100")
    app.title("pySpace Song Prompter")
    screen = tkinter.Canvas(app, bg='white')

    updateStatus()
    
    loadSongs()
    createScreen()
    
    screen.pack(expand=True, fill=tkinter.BOTH)
    
    app.bind('<Escape>', escape)
    app.bind('<Return>', down)
    app.bind('<space>', enter)
    app.bind('<BackSpace>', up)
    
    app.mainloop()
    