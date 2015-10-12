__author__ = 'root'

import codecs
from nltk.tokenize import WhitespaceTokenizer
import numpy as np
import pickle


def get_file_sentence_length_stats():
    fen = codecs.open('file.en', 'rb', encoding='utf-8')
    fde = codecs.open('file.de', 'rb', encoding='utf-8')
    enlen = []
    for s in fen:
        enlen.append(len(WhitespaceTokenizer().tokenize(s)))
    delen = []
    for s in fde:
        delen.append(len(WhitespaceTokenizer().tokenize(s)))
    print 'English mean: ', np.mean(enlen)
    print 'English std: ', np.std(enlen)
    print 'German mean: ', np.mean(delen)
    print 'German std: ', np.std(delen)

    return True


def get_phrase_length_stats():
    p = pickle.load(open('counts_phrase_lr_dl.p','rb'))
    de_len = []
    en_len = []

    for de_p,en_p in p.keys():
        de_len.append(len(WhitespaceTokenizer().tokenize(de_p)))
        en_len.append(len(WhitespaceTokenizer().tokenize(en_p)))

    print 'English phrase mean: ', np.mean(en_len)
    print 'English phrase std: ', np.std(en_len)
    print 'German phrase mean: ', np.mean(de_len)
    print 'German phrase std: ', np.std(de_len)

    return True


if __name__ == '__main__':
    get_file_sentence_length_stats()
    get_phrase_length_stats()