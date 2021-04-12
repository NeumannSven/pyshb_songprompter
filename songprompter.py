"""
This tkinter module parses song lyrics in txt format and displays them for use in karaoke.

Created on 02.03.2021 for PySpaceBremen

@author: sven
@author: christian
"""
import pathlib
import random
import tkinter
import sys

screen = None
position = 1
max_rows = 12


class Song:
    """Geparste Songtexte werden als Song-Objekte instanziert
    Pagination-Logik für die Darstellung der Text in createScreen() findet ausschließlich hier statt,
    der aktuelle Ausschnitt kann mit self.get_stanzas_for_page() erzeugt werden.
    """
    def __init__(self, title, artist, stanzas):
        self.title = title
        self.artist = artist
        self.stanzas = stanzas
        self._pagination = self._pagination()
        self.pages = len(self._pagination) - 1

    def __repr__(self):
        return 'Song("{} - {}")'.format(self.artist, self.title)

    def __str__(self):
        return '{} - {}'.format(self.artist, self.title)

    def _pagination(self):
        """Erstellt eine Liste von Indizes, um die Strophen in Song (self.stanzas) seitenweise zu gruppieren
        Bsp.:   [0, 3, 5]
                Strophen 1-4 (Index 0:3) werden auf Seite 1 gezeigt,
                Strophen 5-6 (Index 3:5) auf Seite 2
        """
        lines_in_stanza = [len(s.lstrip('\n').split('\n')) for s in self.stanzas]
        lines_on_page = 0
        pagination_idx = [0]

        for idx, lines in enumerate(lines_in_stanza, start=1):
            lines_on_page += lines
            if lines_on_page >= max_rows:
                lines_on_page = 0
                pagination_idx.append(idx)
            elif idx == len(lines_in_stanza):
                pagination_idx.append(idx)

        return pagination_idx

    def get_stanzas_for_page(self, page=1):
        """Nutzt die Indizes aus self._pagination um den Ausschnitt für die aktuelle Seite zu generieren
        Die var 'page' ist identisch mit global_var 'position'
        """
        # Check for IndexError
        if page > self.pages:
            page = self.pages

        if page == 1:
            start = 0
        else:
            start = self._pagination[page - 1]
        stop = self._pagination[page]

        return self.stanzas[start:stop]


def loadSongs():
    """Liest alle txt Dateien im Ordner songtexts/ ein und erstellt eine Liste von Song-Objekten
    """
    songlist = []

    folder = pathlib.Path('songtexts')

    for file in folder.iterdir():
        with open(file) as songtextfile:
            songtext = ''
            for line in songtextfile.readlines():
                if line.startswith('# '):
                    title = line.replace('# ', '').rstrip()
                    continue
                elif line.startswith('## '):
                    artist = line.replace('## ', '').rstrip()
                    continue
                else:
                    songtext += line

            stanzas = songtext.split('\n\n')  # list of stanzas

            new_song = Song(title=title, artist=artist, stanzas=stanzas)
            songlist.append(new_song)

    return songlist


def updateStatus(song: Song):
    """Zeigt alle Seiten als Pills oben links, aktuelle Pill (Seite) schwarz
    """
    screen.delete('dots')
    for dot in range(1, song.pages+1):  # range(): start inclusive, stop exclusive
        if position == dot:
            fill = 'black'
        else:
            fill = 'white'
        screen.create_oval(20+(20*dot), 20, 40+(20*dot), 40, fill=fill, tag="dots")
    screen.create_text(1280/2, 30, text=song, font=("Courier", 20, 'bold'), tag="dots")


# Enter
def next_page(e, song: Song):
    global position
    if position < song.pages:
        position += 1
    updateStatus(song)
    createScreen(song)


# Backspace
def previous_page(e, song: Song):
    global position
    if position > 1:
        position -= 1
    updateStatus(song)
    createScreen(song)


# Space
def show_code(e):
    print(e)


# Escape
def escape(e):
    sys.exit()


def createScreen(song: Song):
    """Zeigt einen Ausschnitt aus dem Songtext, erstellt mit Hilfe von Song._pagination()
    """
    stanzas_for_page = song.get_stanzas_for_page(page=position)
    text = '\n\n'.join(stanzas_for_page)

    screen.delete("songtext")
    screen.create_text(20, 80, text=text, tag="songtext", font=("Courier", 20), anchor='nw')
    

if __name__ == '__main__':
    app = tkinter.Tk()
    app.geometry("1280x720+100+100")
    app.title("pySpace Song Prompter")
    screen = tkinter.Canvas(app, bg='white')
    
    songlist = loadSongs()
    # Todo: Choose a song form list; just pick a random one for now
    current_song = random.choice(songlist)

    updateStatus(current_song)
    createScreen(current_song)

    screen.pack(expand=True, fill=tkinter.BOTH)

    app.bind('<Escape>', escape)
    app.bind('<space>', show_code)
    app.bind('<Return>', lambda event: next_page(event, song=current_song))
    app.bind('<BackSpace>', lambda event: previous_page(event, song=current_song))
    
    app.mainloop()
