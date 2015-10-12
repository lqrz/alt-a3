__author__ = 'root'

import pickle
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    counts_phrase_lr_m = pickle.load(open('counts_phrase_lr_m.p', 'rb'))
    counts_phrase_lr_s = pickle.load(open('counts_phrase_lr_s.p','rb'))
    counts_phrase_lr_dr = pickle.load(open('counts_phrase_lr_dr.p','rb'))
    counts_phrase_lr_dl = pickle.load(open('counts_phrase_lr_dl.p','rb'))
    counts_word_lr_m = pickle.load(open('counts_word_lr_m.p','rb'))
    counts_word_lr_s = pickle.load(open('counts_word_lr_s.p','rb'))
    counts_word_lr_dr = pickle.load(open('counts_word_lr_dr.p','rb'))
    counts_word_lr_dl = pickle.load(open('counts_word_lr_dl.p','rb'))
    counts_phrase_rl_m = pickle.load(open('counts_phrase_rl_m.p','rb'))
    counts_phrase_rl_s = pickle.load(open('counts_phrase_rl_s.p','rb'))
    counts_phrase_rl_dr = pickle.load(open('counts_phrase_rl_dr.p','rb'))
    counts_phrase_rl_dl = pickle.load(open('counts_phrase_rl_dl.p','rb'))
    counts_word_rl_m = pickle.load(open('counts_word_rl_m.p','rb'))
    counts_word_rl_s = pickle.load(open('counts_word_rl_s.p','rb'))
    counts_word_rl_dr = pickle.load(open('counts_word_rl_dr.p','rb'))
    counts_word_rl_dl = pickle.load(open('counts_word_rl_dl.p','rb'))
    total_phrase_lr = pickle.load(open('total_phrase_lr.p','rb'))
    total_word_lr = pickle.load(open('total_word_lr.p','rb'))
    total_phrase_rl = pickle.load(open('total_phrase_rl.p','rb'))
    total_word_rl = pickle.load(open('total_word_rl.p','rb'))
    phrase_discont_distance_lr_l = pickle.load(open('phrase_discont_distance_lr_l.p','rb'))
    phrase_discont_distance_lr_r = pickle.load(open('phrase_discont_distance_lr_r.p','rb'))
    phrase_discont_distance_rl_l = pickle.load(open('phrase_discont_distance_rl_l.p','rb'))
    phrase_discont_distance_rl_r = pickle.load(open('phrase_discont_distance_rl_r.p','rb'))

    phrase_m = sum(counts_phrase_lr_m.values() + counts_phrase_rl_m.values())
    phrase_s = sum(counts_phrase_lr_s.values() + counts_phrase_rl_s.values())
    phrase_d = sum(counts_phrase_lr_dr.values() + counts_phrase_lr_dl.values() + counts_phrase_rl_dr.values() + counts_phrase_rl_dl.values())

    word_m = sum(counts_word_lr_m.values() + counts_word_rl_m.values())
    word_s = sum(counts_word_lr_s.values() + counts_word_rl_s.values())
    word_d = sum(counts_word_lr_dr.values() + counts_word_lr_dl.values() + counts_word_rl_dr.values() + counts_word_rl_dl.values())

    ax = plt.subplot(111)
    width = 0.4
    vals = [phrase_m, word_m, phrase_s, word_s, phrase_d, word_d]
    x = np.arange(len(vals))

    ax.set_xticks(x+width)
    ax.set_xticklabels(['Phrase\nMonotone', 'Word\nMonotone', 'Phrase\nSwap', 'Word\nSwap', 'Phrase\nDiscontinuous', 'Word\nDiscontinuous'])

    phrase_word = plt.bar(x+width*0.5, vals, width, color='#5f9ed1', edgecolor='None')
    # ax.legend((withoutBar[0], withoutBar[0], withoutBar[0], withoutBar[0]), ('Baseline', 'Backoff', 'Either', 'Both'), \
    #           frameon=False)
    # plt.show()
    plt.savefig('phrase_word', bbox_inches='tight')

    ax = plt.subplot(111)
    width = 0.4
    vals = [phrase_m, phrase_s, phrase_d]
    x = np.arange(len(vals))
    phrase_event = plt.bar(x+width*0.5, vals, width, color='#5f9ed1', edgecolor='None')

    ax.set_xticks(x+width)
    ax.set_xticklabels(['Monotone', 'Swap', 'Discontinuous'])

    # ax.legend((phrase_event[0], phrase_event[1], phrase_event[2]), ('Monotone', 'Swap', 'Discontinuous'), \
    #           frameon=False)
    # plt.show()
    plt.savefig('phrase_event', bbox_inches='tight')
    print 'end'

