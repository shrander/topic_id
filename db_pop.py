import sqlite3
from imdb import IMDb
import random
import sys

if len(sys.argv) != 2:
    raise Exception('Options Error')

movie_list = sys.argv[1]
conn = sqlite3.connect('topic.db')

c = conn.cursor()

ia = IMDb()

fh = open(movie_list, 'r')
 
for each in fh.readlines():
    
    # search the movie on IMDB
    mov_list = ia.search_movie(each)
    if len(mov_list)>0:
        query = c.execute('select count(*) from movie_table WHERE title = \"'+mov_list[0]['title']+'\";')
        if query.fetchone()[0] != 0:
            print mov_list[0]['title']+': Already in DB'
            continue
    else:
        print each+': not found'
        continue
    # get the first result
    try:
        mov = ia.get_movie(mov_list[0].getID())
    except Exception as e:
        print e
        print mov_list
    # get lead actors name !! this will not always be 
    # the lead actors name as some cast orders are alphabetically ordered
    try:
        actor = mov['cast'][0]['name']
    except KeyError as e:
        print e
        print mov['title']
        #c.execute("INSERT into movie_table VALUES ("+mov.getID()+",\""+mov['title']+'\",\"'+mov['plot'][0]+'\",'+None+","+mov['genre']+")")
        #c.commit()
        continue
    try:
        # collapse list object to string
        genre = ''
        for each in mov['genre']:
            genre += each+','
        # Enter the first movie found into the DB
        c.execute('INSERT INTO movie_table (id,title,plot,lead_actor,genre_list) VALUES ('+mov.getID()+',\"'+mov['title']+'\",\"'+mov['plot'][0]+'\",\"'+actor+'\",\"'+genre[:-1]+'\");')
    except Exception as e:
        print e
        print mov['title']
        continue
    conn.commit()
    print 'added '+mov['title']
#close the connection to the db
conn.close()