import sys
from imdb import IMDb
import sqlite3 as sql

class app:
    def _init_(self):
      pass
    
    def usage(self):
      print 'USAGE: topic_id.py [options] [synapsis file]\n'
      print 'This program will determine what genres a movie is in by the contents of the title and synapsis'
      print 'Options:'
      print ' -k'

def parse_args(self, args):
      pass
    
    def main(self, args):
      self.parse_args(args)




if __name__ == '__main__':
    a = app()
    a.main(sys.argv)