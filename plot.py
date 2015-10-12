__author__ = 'root'

import pickle
import matplotlib.pyplot as plt
import numpy as np
from nltk import compat


def plot_phrase_events(vals):

    ax = plt.subplot(111)
    width = 0.4
    x = np.arange(len(vals))
    phrase_event = plt.bar(x + width * 0.5, vals, width, color='#5f9ed1', edgecolor='None')
    ax.set_xticks(x + width)
    ax.set_xticklabels(['Monotone', 'Swap', 'Discontinuous'])
    plt.xlabel('Reordering events')
    plt.ylabel('Counts')
    # ax.legend((phrase_event[0], phrase_event[1], phrase_event[2]), ('Monotone', 'Swap', 'Discontinuous'), \
    #           frameon=False)
    # plt.show()
    plt.savefig('phrase_event', bbox_inches='tight')

    return True


def plot_phrase_vs_word(vals):

    ax = plt.subplot(111)
    width = 0.4
    x = np.arange(len(vals))
    ax.set_xticks(x + width)
    ax.set_xticklabels(['Phrase\nMonotone', 'Word\nMonotone', 'Phrase\nSwap', 'Word\nSwap', 'Phrase\nDiscontinuous',
                        'Word\nDiscontinuous'])
    plt.xlabel('Reordering events')
    plt.ylabel('Counts')
    phrase_word = plt.bar(x + width * 0.5, vals, width, color='#5f9ed1', edgecolor='None')
    # ax.legend((withoutBar[0], withoutBar[0], withoutBar[0], withoutBar[0]), ('Baseline', 'Backoff', 'Either', 'Both'), \
    #           frameon=False)
    # plt.show()
    plt.savefig('phrase_word', bbox_inches='tight')
    plt.close()

    return True

def plot_phrase_discontinuous_distortion(vals):

    phrase_discont_distance_lr_l = pickle.load(open('phrase_discont_distance_lr_l.p','rb'))
    phrase_discont_distance_lr_r = pickle.load(open('phrase_discont_distance_lr_r.p','rb'))
    phrase_discont_distance_rl_l = pickle.load(open('phrase_discont_distance_rl_l.p','rb'))
    phrase_discont_distance_rl_r = pickle.load(open('phrase_discont_distance_rl_r.p','rb'))

    means = [np.mean(phrase_discont_distance_lr_l), np.mean(phrase_discont_distance_lr_r),
            np.mean(phrase_discont_distance_rl_l), np.mean(phrase_discont_distance_rl_r)]

    stds = [np.std(phrase_discont_distance_lr_l), np.std(phrase_discont_distance_lr_r),
            np.std(phrase_discont_distance_rl_l), np.std(phrase_discont_distance_rl_r)]

    print 'Means: ', means
    print 'Stds: ', stds

    labels = ['Left2Right\nLeft', 'Left2Right\nRight', 'Right2Left\nLeft', 'Right2Left\nRight']

    plt.errorbar(np.array(range(len(means))) + .9, means, stds, marker='o', linestyle='None', \
                 ecolor='#5f9ed1', mfc='#5f9ed1', mec='None', label='Young')
    plt.axhline(y=0, color='grey', linestyle='--', alpha=0.5)
    plt.xticks(np.array(range(len(means))) + 1, [compat.text_type(s.replace(' ', '\n')) for s in labels])
    plt.xlabel('Phrase discontinuous events')
    plt.ylabel('Distortion')

    plt.savefig('phrase_discont_dist', dpi=100, bbox_inches='tight')

    return True


def plot_phrase_discontinuous(vals):
    # [counts_phrase_lr_dr, counts_phrase_lr_dl, counts_phrase_rl_dr, counts_phrase_rl_dl]
    ax = plt.subplot(111)
    width = 0.4
    x = np.arange(len(vals))
    ax.set_xticks(x + width)
    ax.set_xticklabels(['Left2Right\nRight', 'Left2Right\nLeft', 'Right2Left\nRight', 'Right2Left\nLeft'])
    plt.xlabel('Reordering events')
    plt.ylabel('Counts')
    phrase_word = plt.bar(x + width * 0.5, vals, width, color='#5f9ed1', edgecolor='None')
    # ax.legend((withoutBar[0], withoutBar[0], withoutBar[0], withoutBar[0]), ('Baseline', 'Backoff', 'Either', 'Both'), \
    #           frameon=False)
    # plt.show()
    plt.savefig('phrase_discont', bbox_inches='tight')
    plt.close()

    return True


if __name__ == '__main__':
    # counts_phrase_lr_m = pickle.load(open('counts_phrase_lr_m.p', 'rb'))  11634195
    # counts_phrase_lr_s = pickle.load(open('counts_phrase_lr_s.p','rb'))   396519
    # counts_phrase_lr_dr = pickle.load(open('counts_phrase_lr_dr.p','rb')) 5394488
    # counts_phrase_lr_dl = pickle.load(open('counts_phrase_lr_dl.p','rb')) 1558032
    # counts_word_lr_m = pickle.load(open('counts_word_lr_m.p','rb'))   2260465
    # counts_word_lr_s = pickle.load(open('counts_word_lr_s.p','rb'))   196934
    # counts_word_lr_dr = pickle.load(open('counts_word_lr_dr.p','rb')) 3385157
    # counts_word_lr_dl = pickle.load(open('counts_word_lr_dl.p','rb')) 428215
    # counts_phrase_rl_m = pickle.load(open('counts_phrase_rl_m.p','rb'))   11623374
    # counts_phrase_rl_s = pickle.load(open('counts_phrase_rl_s.p','rb'))   397747
    # counts_phrase_rl_dr = pickle.load(open('counts_phrase_rl_dr.p','rb')) 1641415
    # counts_phrase_rl_dl = pickle.load(open('counts_phrase_rl_dl.p','rb')) 5284117
    # counts_word_rl_m = pickle.load(open('counts_word_rl_m.p','rb'))   2254822
    # counts_word_rl_s = pickle.load(open('counts_word_rl_s.p','rb'))   317084
    # counts_word_rl_dr = pickle.load(open('counts_word_rl_dr.p','rb')) 507860
    # counts_word_rl_dl = pickle.load(open('counts_word_rl_dl.p','rb')) 3229258
    counts_phrase_lr_m = 11634195
    counts_phrase_lr_s = 396519
    counts_phrase_lr_dr = 5394488
    counts_phrase_lr_dl = 1558032
    counts_word_lr_m = 2260465
    counts_word_lr_s = 196934
    counts_word_lr_dr = 3385157
    counts_word_lr_dl = 428215
    counts_phrase_rl_m = 11623374
    counts_phrase_rl_s = 397747
    counts_phrase_rl_dr = 1641415
    counts_phrase_rl_dl = 5284117
    counts_word_rl_m = 2254822
    counts_word_rl_s = 317084
    counts_word_rl_dr = 507860
    counts_word_rl_dl = 3229258

    # total_phrase_lr = pickle.load(open('total_phrase_lr.p','rb'))
    # total_word_lr = pickle.load(open('total_word_lr.p','rb'))
    # total_phrase_rl = pickle.load(open('total_phrase_rl.p','rb'))
    # total_word_rl = pickle.load(open('total_word_rl.p','rb'))

    # mean = np.mean(phrase_discont_distance_lr_l+phrase_discont_distance_lr_r)
    # std = np.std(phrase_discont_distance_lr_l+phrase_discont_distance_lr_r)
    # print 'Discontinuous lr: ', mean, std   # 4.85 6.52
    #
    # mean = np.mean(phrase_discont_distance_rl_l+phrase_discont_distance_rl_r)
    # std = np.std(phrase_discont_distance_rl_l+phrase_discont_distance_rl_r)
    # print 'Discontinuous rl: ', mean, std   # 5.23 6.77

    phrase_m = counts_phrase_lr_m + counts_phrase_rl_m
    phrase_s = counts_phrase_lr_s+ counts_phrase_rl_s
    phrase_d = counts_phrase_lr_dr + counts_phrase_lr_dl + counts_phrase_rl_dr + counts_phrase_rl_dl

    word_m = counts_word_lr_m + counts_word_rl_m
    word_s = counts_word_lr_s + counts_word_rl_s
    word_d = counts_word_lr_dr + counts_word_lr_dl + counts_word_rl_dr + counts_word_rl_dl

    vals = [phrase_m, word_m, phrase_s, word_s, phrase_d, word_d]
    # plot_phrase_vs_word(vals)

    vals = [phrase_m, phrase_s, phrase_d]
    # plot_phrase_events(vals)

    vals = [counts_phrase_lr_dr, counts_phrase_lr_dl, counts_phrase_rl_dr, counts_phrase_rl_dl]
    plot_phrase_discontinuous(vals)
    # vals = [counts_phrase_lr_dr, counts_phrase_lr_dl, counts_phrase_rl_dr, counts_phrase_rl_dl]
    plot_phrase_discontinuous_distortion(None)

    print 'end'

