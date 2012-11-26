import sys
from imdb import IMDb
import sqlite3 as sql

class parser:
    def 
class app:
    def __init__(self):
        self.db_file = ''
        self.db_hndl = None
        self.db_connection = None
        self.db_cursor = None
        self.synopsis_file = ''
        self.syn_hndl = None
        self.training_flag = False
        
    def usage(self):
        print 'USAGE: topic_id.py [options] [synapsis file]\n'
        print 'This program will determine what genres a movie is in by the contents of the title and synapsis'
        print 'Options:'
        print ' -k              Not sure if I need this flag'
        print ' -T [filename]   Sets the training flag.  The file expected is one generated'
        print '                  by db_pop.py.'
        print ''
        sys.exit()

    def parse_args(self, args):
        i=0
        while(i<len(args)):
            if args[i] == -T:
                i+=1
                self.db_file=args[i]
            else:
                #assume the synopsis file is the unknown
                self.synopsis_file = args[i]
                self.training_flag = True
    
    def init_data(self):
        try:
            if self.training_flag:
                self.db_hndl = open(self.db_file, 'r')
            else:
                self.syn_hndl = open(self.synopsis_file, 'r')
        except IOError e:
            print e
    
    def main(self, args):
        self.parse_args(args)
        self.init_data()



if __name__ == '__main__':
    a = app()
    a.main(sys.argv)