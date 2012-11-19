import sqlite3
from imdb import IMDb
import random

conn = sqlite3.connect('topic.db')

c = conn.cursor()

ia = IMDb()

fh = open('movie_list', 'r')

i=0
while(i<1000):
	mov_list = ia.search_movie(random.randint(1,1332012))
	
	c.execute("INSERT into movie_table VALUES ("+mov['']+") ")
