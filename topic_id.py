import sys
import operator
import pygame
from imdb import IMDb
import sqlite3 as sql

class parser:
    def __init__(self):
        pass

    def text_to_list(self, text, n):
        """
        create tokenized word list - word list will consist of a list of n-grams
        text - text blob to be tokenized
        n - n-gram depth
        """
        wordlist = text.split()
        i=0
        nGramList = []
        while(i<len(wordlist)):
            tlist = []
            j=0
            while(i+j < len(wordlist) and j<n):
                tlist.append(wordlist[i+j])
                j+=1
            if len(tlist) == n:
                nGramList.append(tuple(tlist))
            i+=1
        return nGramList

    def print_top_n_most_ngrams(self, hist, length=100):
        """
        creates a table of the most used ngrams in the corpus
        hist - histogram to parse over
        length - number of most frequently seen n-grams
        """
        sortedHist = sorted(hist.iteritems(), key=operator.itemgetter(1), reverse=True)
        for each in range(length):
            for j in sortedHist[each][0]:
                print '%-10s' % j,
            print '%5d' % sortedHist[each][1]
    
    def build_hist(self, text, n):
        """
        create a histogram of n-grams 
        text - string to convert into histogram
        n - n-gram depth
        returns a dict [key=n-gram, value=counts]
        """
        ngram_list = self.text_to_list(text, n)
        hist = {}
        for each in ngram_list:
            if each not in hist:
                hist[each] = ngram_list.count(each)
        return hist
    

        
class topic_id:
    def __init__(self):
        self.db_file = ''
        self.db_conn = None
        self.db_cursor = None
        self.synopsis_file = ''
        self.syn_hndl = None
        self.training_flag = False
        self.n_depth = 2
        
        self.p = parser()
        
        # sound file to play when finished
        sound = '/Developer/Python/pygame/Examples/data/punch.wav'
        
    def usage(self):
        print 'USAGE: topic_id.py [options] [file]\n'
        print 'This program will determine what genres a movie is in by the contents of the title and synapsis'
        print 'Options:'
        print ' -n              depth for the n-gram parser'
        print ' -T              Sets the training flag.  The file expected is one generated'
        print '                  by db_pop.py.'
        print '[file]           File to train against (requires the \'T\' flag) or a synopsis file'
        print '                  synopsis file to detect genre'
        sys.exit()

    def parse_args(self, args):
        i=0
        if len(args)<=1:
            self.usage()
        while(i<len(args)):
            if args[i] == '-T':
                i+=1
                self.db_file=args[i]
                self.training_flag = True
            elif args[i] == '-n':
                i+=1
                self.n_depth = int(args[i])
            else:
                #assume the synopsis file is the unknown
                self.synopsis_file = args[i]
            i+=1
    
    def init_data(self):
        try:
            if self.training_flag:
                # connect to DB
                self.db_conn = sql.connect(self.db_file)
                self.db_cursor = self.db_conn.cursor()
            else:
                # or open synopsis file
                self.syn_hndl = open(self.synopsis_file, 'r')
        except IOError as e:
            print e
        except sql.Error, e:
            print e
    
    def train(self):
        # walk through db
        # cat all plot summaries for a genre and send to create_hist
        # workout some training object
        # build training object
        genre_query = self.db_cursor.execute('SELECT genre_list FROM movie_table;')
        genre_list = []
        for each in genre_query.fetchall():
            genre = each[0].split(',')
            for each_gen in genre:
                if each_gen not in genre_list:
                    genre_list.append(each_gen)
        
        for each in genre_list:
            plot_blob = ''
            print 'Training on '+each
            plot_query = self.db_cursor.execute('SELECT plot FROM movie_table WHERE genre_list LIKE \'%'+each+'%\';')
            for row in plot_query.fetchall():
                 plot_blob += ' '+row[0].split('::')[0]
            self.p.print_top_n_most_ngrams(self.p.build_hist(plot_blob, self.n_depth))
            return 
    
    def find_topics(self):
        #parse text
        # send to parser object and build hist
        # somehow need to figure out what are good n-grams and determine if those are 
        # 
        pass
        
    def main(self, args):
        self.parse_args(args)
        self.init_data()
        if self.training_flag:
            self.train()
        else:
            self.find_topics()
        print 'play sound'
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound('/Developer/Python/pygame/Examples/data/punch.wav')
        sound.play()

if __name__ == '__main__':
#    try:
    a = topic_id()
    a.main(sys.argv)
#    except KeyboardInterrupt as e:
#        print e