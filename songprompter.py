'''
Created on 02.03.2021

@author: sven
'''

import tkinter
import sys
from pprint import pprint

screen = None
pages  = 1
position = 1
songnumber = 0
max_rows = 12
strophenrows = None
linescount = 0
strophencount = 0

songlist = [
  ["Titel1", "Interpret1", ["Strophe1","Strophe2","Strophe3"],[3, 2, 2]],
  ["Titel2", "Interpret2", ["Strophe1","Strophe2","Strophe3"],[]],
  ["Titel3", "Interpret3", ["Strophe1","Strophe2","Strophe3"],[]],
]

# Todo: Use dict instead
songlist_dict = [
  {
    "title": "Titel1",
    "artist": "Interpret1",
    "stanzas": ["Strophe1", "Strophe2", "..."],
    "pagination": [2, 3, 2, 3]
  },
]

songtext = ''

title = ''
interpreten = ''


# Todo: Use OOP?
class Song:
    pass



# Up
def up(e):
    global position
    if position > 1:
        position -= 1
    updateStatus()
    createScreen()
    
# Down
def down(e):
    global position
    if position < pages:
        position += 1
    updateStatus()
    createScreen()

# Enter
def enter(e):
    print(e)

# Escape
def escape(e):
    sys.exit()


def parseSongFile():
    for line in songtext:
        print(line)


def loadSongs():
    """Songtexte einlesen und auf mehrere Seiten verteilen
    """
    global songtext, title, interpreten, strophenrows, max_rows, pages
    #and_the_lamb_lies_down_on_Broadway
    with open('pi.txt') as songtextfile:
        for line in songtextfile.readlines():
            if line.startswith('# '):
                title = line.replace('# ', '').rstrip()
                continue
            if line.startswith('## '):
                interpreten = line.replace('## ', '').rstrip()
                continue
            #if line == ''
            songtext += line
            #print(line, end='')
    songtext = songtext.split('\n\n')
    
    strophenrows = [len(s.lstrip('\n').split('\n')) for s in songtext]

    # Todo
    songlist[0] = [title, interpreten, songtext, pagination(strophenrows)]
    



def pagination(strophenrows):
  """Erstellt eine Liste von Indizes, um die Strophen in songlist seitenweise zu gruppieren
  """
    rows = 0
    page_count = [0]

    for idx, strophe in enumerate(strophenrows):
        rows += strophe
        if rows > max_rows:
            rows = 0
            page_count.append(idx)
        if idx == (len(strophenrows)-1):
            page_count.append(idx)

    return page_count


def updateStatus():
    """Zeigt alle Seiten als Pills oben links, aktuelle Seite schwarz
    """
    fill = 'white'
    screen.delete('dots')
    for dot in range(1, pages+1):  # range(): start inclusive, stop exclusive
        if position == dot:
            fill = 'black'
        else:
            fill = 'white'
        screen.create_oval(20+(20*dot),20,40+(20*dot),40, fill=fill, tag="dots")
    screen.create_text(1280/2, 30, text=songlist[songnumber][0] + " - " +  songlist[songnumber][1], font=("Courier", 20, 'bold'), tag="dots")


def createScreen():
    """
    """
    global linescount, strophencount, pages
    linescount = 0
    text = ''
    for count, row in enumerate(songlist[songnumber][2]):
        if count >= strophencount: 
            linescount += len(row.split('\n'))
            if linescount >= 20:
                break
            strophencount += 1
            text += row + 2*'\n'
    
  
    text = songlist[songnumber][2][position-1]
    screen.delete("songtext")    
    screen.create_text(20, 80, text=text, tag="songtext", font=("Courier", 20), anchor='nw')
    

if __name__ == '__main__':
    app = tkinter.Tk()
    app.geometry("1280x720+100+100")
    app.title("pySpace Song Prompter")
    screen = tkinter.Canvas(app, bg='white')
    
    loadSongs()
    updateStatus()
    print(title)
    print(interpreten)
    #pprint(songlist)
    #parseSongFile()
    #print(strophenrows)

    createScreen()
    print(strophencount)
        
    screen.pack(expand=True, fill=tkinter.BOTH)
    
    app.bind('<Escape>', escape)
    app.bind('<Return>', down)
    app.bind('<space>', enter)
    app.bind('<BackSpace>', up)
    
    app.mainloop()
    
