#!/usr/bin/python
import time 
import sys
import operator
import pygame
import cPickle
from imdb import IMDb
import sqlite3 as sql
import pytagcloud

class parser:
    def __init__(self):
        pass

    def text_to_list(self, text, n):
        """
        create tokenized word list - word list will consist of a list of n-grams
        text - text blob to be tokenized
        n - n-gram depth
        """
        wordlist = text.lower().split()
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
        self.synopsis_flag = False
        self.training_flag = False
        self.n_depth = 2
        
        self.norm = False
        
        self.genre_hist = {}
        
        self.p = parser()
        
        # sound file to play when finished
        sound = '/Developer/Python/pygame/Examples/data/punch.wav'
        
    def usage(self):
        print 'USAGE: topic_id.py [options] [file]\n'
        print 'This program will determine what genres a movie is in by the contents of the title and synapsis'
        print 'Options:'
        print ' -n              depth for the n-gram parser'
        print ' -T [file]       Sets the training flag.  The file expected is one generated'
        print '                  by db_pop.py.'
        print '[file]           Synopsis file to identify topics'
        sys.exit()

    def parse_args(self, args):
        i=0
        while(i<len(args)):
            if args[i] == '-T':
                i+=1
                self.db_file=args[i]
                self.training_flag = True
            elif args[i] == '-n':
                i+=1
                self.n_depth = int(args[i])
            elif args[i] == '-N':
                self.Normalize=True
            else:
                #assume the synopsis file is the unknown
                self.synopsis_file = args[i]
                self.synopsis_flag = True
            i+=1
    
    def init_data(self):
        pygame.init()
        pygame.mixer.init()
        try:
            if self.training_flag:
                # connect to DB
                self.db_conn = sql.connect(self.db_file)
                self.db_cursor = self.db_conn.cursor()
            if self.synopsis_flag:
                # or open synopsis file
                self.syn_hndl = open(self.synopsis_file, 'r')
        except IOError as e:
            print e
        except sql.Error, e:
            print e
    
    def get_genres(self):
        genre_list=[]
        genre_query = self.db_cursor.execute('SELECT genre_list FROM movie_table;')
        for each in genre_query.fetchall():
            genre = each[0].split(',')
            for each_gen in genre:
                if each_gen not in genre_list:
                    genre_list.append(each_gen)
        return genre_list
        
    def train(self):
        """
        Build a trained object to be able to compare future synopses against
        
        returns a dictionary of histograms.  Keys of the dict are the genres
        """
        genre_list = self.get_genres()
        genre_hist={}
        for each in genre_list:
            plot_blob = ''
            print 'Training on '+each
            plot_query = self.db_cursor.execute('SELECT plot FROM movie_table WHERE genre_list LIKE \'%'+each+'%\';')
            for row in plot_query.fetchall():
                 plot_blob += ' '+row[0].split('::')[0]
            genre_hist[each] = self.p.build_hist(plot_blob, self.n_depth)
        self.normalize(genre_hist)
        print '\nStoring Training data'
        self.store_genre_data(genre_hist)        
        return genre_hist
    
    def normalize(self, hist):
        """
        normalizes the data
        hist
        """
        return
        sums={}
        for each_genre in hist.keys():
            sum[each_genre]=0
            for each in hist[each_genre].keys():
                hist[each_genre][each]
        
    def store_genre_data(self, data):
        self.genre_hist = data
        fh = open('.topic_id.dat', 'w')
        cPickle.dump(data, fh)
        fh.close()
    
    def load_genre_data(self):
        fh = open('.topic_id.dat', 'r')
        self.genre_hist = cPickle.load(fh)
        fh.close()
        # make sure that the n-gram depth matches the training data
        genre = self.genre_hist.keys()[0]
        if self.n_depth != len(self.genre_hist[genre].keys()[0]):
            print 'Alter ngram depth to match trained data'
            self.n_depth = len(self.genre_hist[genre].keys()[0])
        
    def score(self, hist):
        """
        builds a dictionary of genres and scores the input text with the training data
        hist - a dictionary of n-grams and their counts
        """
        scores = {}
        for each_genre in self.genre_hist.keys():
            scores[each_genre]=0
            for each_n_gram in self.genre_hist[each_genre].keys():
                for each in hist.keys():
                    if each == each_n_gram:
                        scores[each_genre] += hist[each]*self.genre_hist[each_genre][each_n_gram]
        return scores

    def find_topics(self):
        #parse text
        # send to parser object and build hist
        # somehow need to figure out what are good n-grams and determine if those are 
        # 
        syn_hist = self.p.build_hist(self.syn_hndl.read(),self.n_depth)
        scores = self.score(syn_hist)
        for each in scores.keys():
            print each +': '+str(scores[each])

    def main(self, args):
        self.parse_args(args)
        self.init_data()
        
        if self.training_flag:
            self.train()
        else:
            try:
                self.load_genre_data()
                if self.norm:
                    self.normalize(self.genre_hist)
            except IOError as e:
                print e
                print 'Could not load pregenerated data.  Retrainning required!'
                raise Exception('LoadError')
        
        if self.synopsis_flag:
            self.find_topics()

        # Noise to signal stop
        pygame.mixer.Sound('/Developer/Python/pygame/Examples/data/punch.wav').play()
        time.sleep(1)
        

if __name__ == '__main__':
    try:
        a = topic_id()
        a.main(sys.argv[1:])
    except KeyboardInterrupt as e:
        print e