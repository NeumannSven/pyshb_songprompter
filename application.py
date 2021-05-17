
import tkinter
import sys

class Application(tkinter.Tk):

    def __init__(self, songlist):
        tkinter.Tk.__init__(self)
        self.screen = None
        self.position = 1

        self.songlist = songlist
        self.song_number = 0
        self.song = self.songlist[self.song_number]
        self.geometry("1280x720+0+0")
        self.attributes("-fullscreen", True)
        self.title("pySpace Song Prompter")
        self.screen = tkinter.Canvas(self,  bg='black')
        self.create_menu()
        self.mainloop()

    def setSong(self, song):
        self.song = song

    def updateStatus(self):
        """Zeigt alle Seiten als Pills oben links, aktuelle Pill (Seite) schwarz
        """
        self.screen.delete('dots')
        for dot in range(1, self.song.pages+1):  # range(): start inclusive, stop exclusive
            if self.position == dot:
                fill = 'white'
            else:
                fill = 'black'
            self.screen.create_oval(20+(20*dot), 20, 40+(20*dot), 40, fill=fill, tag="dots", outline='white')
        self.screen.create_text(1280/2, 30, text=self.song, font=("Courier", 20, 'bold'), tag="dots", fill='white')

    # Enter im Song Screen
    def next_page(self, e):
        if self.position < self.song.pages:
            self.position += 1
        self.updateStatus()
        self.showScreen()

    # Backspace im Song Screen
    def previous_page(self, e):
        if self.position > 1:
            self.position -= 1
        self.updateStatus()
        self.showScreen()

    # Space im Song Screen
    def song_screen(self, e):
        self.songs_menu.pack_forget()
        self.createScreen()

    # Enter im Menu Screen
    def next_item(self, e):
        if self.song_number < self.songs_menu.size()-1: 
            self.song_number += 1
        self.songs_menu.selection_clear(0, tkinter.END)
        self.songs_menu.see(self.song_number)
        self.songs_menu.selection_set(self.song_number)



    # Backspace im Menu Screen
    def previous_item(self, e):
        if self.song_number > 0:
            self.song_number -= 1
        self.songs_menu.selection_clear(0, tkinter.END)
        self.songs_menu.see(self.song_number)
        self.songs_menu.selection_set(self.song_number)


    # Space im Menu Screen
    def menu_screen(self, e):
        self.screen.pack_forget()
        self.create_menu()

    def createScreen(self):
        self.screen = tkinter.Canvas(self, bg='black')
        self.updateStatus()
        self.showScreen()
        self.screen.pack(expand=True, fill=tkinter.BOTH)

    def showScreen(self):
        """Zeigt einen Ausschnitt aus dem Songtext, erstellt mit Hilfe von Song._pagination()
        """
        stanzas_for_page = self.song.get_stanzas_for_page(page=self.position)
        text = '\n\n'.join(stanzas_for_page)

        self.screen.delete("songtext")

        self.screen.create_text(20, 80, text=text, tag="songtext", font=("Courier", 20), anchor='nw', fill='white')
        self.bind('<space>', self.menu_screen)
        self.bind('<Return>', self.next_page)
        self.bind('<BackSpace>', self.previous_page)

    def create_menu(self):
        """Zeigt die Liste aller Songs 
        """

        self.songs_menu = tkinter.Listbox(self, width=50, selectmode=tkinter.SINGLE, font=("Courier", 20), fg='white', bg='black')

        menu_entrys = [f'\"{song.title}\" by {song.artist}' for song in self.songlist]

        for menu_entry in menu_entrys:
            self.songs_menu.insert(tkinter.END, menu_entry)
    
        self.songs_menu.pack(expand=True, fill=tkinter.BOTH)

        self.songs_menu.see(self.song_number)
        self.songs_menu.selection_set(self.song_number)
        self.songs_menu.activate(self.song_number)
        self.bind('<space>', self.song_screen)
        self.bind('<Return>', self.next_item)
        self.bind('<BackSpace>', self.previous_item)

