
import pathlib
import random

MAX_ROWS = 12

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
            if lines_on_page >= MAX_ROWS:
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

class Songs:
    def loadSongs(self):
        """Liest alle txt Dateien im Ordner songtexts/ ein und erstellt eine Liste von Song-Objekten
        """
        self.songlist = []
        self.folder = pathlib.Path('songtexts')

        for file in self.folder.iterdir():
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
                self.songlist.append(new_song)

        return self.songlist