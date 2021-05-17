"""
This tkinter module parses song lyrics in txt format and displays them for use in karaoke.

Created on 02.03.2021 for PySpaceBremen

@author: sven
@author: christian
"""

from songs import Songs
from application import Application



songslist = Songs().loadSongs()
#print(songslist)

app = Application(songslist)




