__author__ = 'root'

import pickle
import matplotlib.pyplot as plt
import numpy as np
from nltk import compat


def plot_phrase_events(vals):
    '''
    histogram of phrase events
    :param vals:
    :return:
    '''
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
    plt.close()

    return True


def plot_phrase_vs_word(vals):
    '''
    histogram of phrase vs word events.
    :param vals:
    :return:
    '''
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

def plot_phrase_discontinuous_distortion():
    '''
    phrase discontinuous distortion
    :return:
    '''
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
    # plt.axhline(y=0, color='grey', linestyle='--', alpha=0.5)
    plt.xticks(np.array(range(len(means))) + .9, [compat.text_type(s.replace(' ', '\n')) for s in labels])
    plt.yticks(range(1,21), [str(i) for i in range(1,21)])
    plt.xlabel('Phrase discontinuous events')
    plt.ylabel('Distortion')

    plt.ylim((1,20))

    plt.savefig('phrase_discont_dist', dpi=100, bbox_inches='tight')
    plt.close()

    return True


def plot_word_discontinuous_distortion():
    '''
    word discontinuous distortion
    :return:
    '''
    phrase_discont_distance_lr_l = pickle.load(open('word_discont_distance_lr_l.p','rb'))
    phrase_discont_distance_lr_r = pickle.load(open('word_discont_distance_lr_r.p','rb'))
    phrase_discont_distance_rl_l = pickle.load(open('word_discont_distance_rl_l.p','rb'))
    phrase_discont_distance_rl_r = pickle.load(open('word_discont_distance_rl_r.p','rb'))

    means = [np.mean(phrase_discont_distance_lr_l), np.mean(phrase_discont_distance_lr_r),
            np.mean(phrase_discont_distance_rl_l), np.mean(phrase_discont_distance_rl_r)]

    stds = [np.std(phrase_discont_distance_lr_l), np.std(phrase_discont_distance_lr_r),
            np.std(phrase_discont_distance_rl_l), np.std(phrase_discont_distance_rl_r)]

    print 'Means: ', means
    print 'Stds: ', stds

    labels = ['Left2Right\nLeft', 'Left2Right\nRight', 'Right2Left\nLeft', 'Right2Left\nRight']

    plt.errorbar(np.array(range(len(means))) + .9, means, stds, marker='o', linestyle='None', \
                 ecolor='#5f9ed1', mfc='#5f9ed1', mec='None', label='Young')
    # plt.axhline(y=0, color='grey', linestyle='--', alpha=0.5)
    plt.xticks(np.array(range(len(means))) + .9, [compat.text_type(s.replace(' ', '\n')) for s in labels])
    plt.yticks(range(1,21), [str(i) for i in range(1,21)])
    plt.xlabel('Word discontinuous events')
    plt.ylabel('Distortion')

    plt.ylim((1,20))

    plt.savefig('word_discont_dist', dpi=100, bbox_inches='tight')
    plt.close()

    return True


def plot_phrase_discontinuous(vals):
    '''
    histogram of phrase discontinuous reordering events
    :param vals:
    :return:
    '''
    # vals = [counts_phrase_lr_dr, counts_phrase_lr_dl, counts_phrase_rl_dr, counts_phrase_rl_dl]
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

def plot_phrase_len_reor():
    '''
    reordering events frequency wrt German-side phrase len
    :return:
    '''
    mp = pickle.load(open('phrase_len_reor_m.p','rb'))
    sp = pickle.load(open('phrase_len_reor_s.p','rb'))
    dp = pickle.load(open('phrase_len_reor_d.p','rb'))

    m = mp.values()
    s = sp.values()
    d = dp.values()

    x = np.arange(len(mp.values()))

    ax = plt.subplot(111)
    width = 0.4
    ax.set_xticks(x + width)
    ax.set_xticklabels(['1', '2', '3', '4', '5','6','7'])
    plt.xlabel('Phrase length')
    plt.ylabel('Counts')
    mon = plt.bar(x + width * 0.5, m, width, color='#5f9ed1', edgecolor='None')
    dis = plt.bar(x + width * 0.5, d, width, color='#f26c64', edgecolor='None')
    swap = plt.bar(x + width * 0.5, s, width, color='#32a251', edgecolor='None')
    ax.legend((mon[0], dis[0], swap[0]), ('Monotone', 'Discontinuous', 'Swap'), frameon=False)
    # plt.show()
    plt.savefig('phrase_len_reor', bbox_inches='tight')
    plt.close()

    return True


def plot_phrase_len_discontinuous():
    '''
    frequency of discontinuous-to-the-left and -to-the-right wrt distortion
    :return:
    '''
    dl = pickle.load(open('phrase_discont_distance_lr_l.p','rb'))
    dr = pickle.load(open('phrase_discont_distance_lr_r.p','rb'))

    x = np.arange(len(np.bincount(dl)))

    ax = plt.subplot(111)
    width = 0.4
    # ax.set_xticks(x1 + width)
    # ax.set_xticklabels(['1', '2', '3', '4', '5','6','7'])
    plt.xlabel('Distortion')
    plt.ylabel('Counts')
    mon = plt.bar(x, np.bincount(dl), width, color='#5f9ed1', edgecolor='None')
    # dis = plt.bar(x + width * 0.5, d, width, color='#f26c64', edgecolor='None')
    # swap = plt.bar(x + width * 0.5, s, width, color='#32a251', edgecolor='None')
    # ax.legend((mon[0], dis[0], swap[0]), ('Monotone', 'Discontinuous', 'Swap'), frameon=False)
    # plt.show()
    plt.ylim((0,2500000))
    plt.savefig('phrase_dist_freq_l', bbox_inches='tight')
    plt.close()

    x = np.arange(len(np.bincount(dr)))

    ax = plt.subplot(111)
    width = 0.4
    # ax.set_xticks(x1 + width)
    # ax.set_xticklabels(['1', '2', '3', '4', '5','6','7'])
    plt.xlabel('Distortion')
    plt.ylabel('Counts')
    mon = plt.bar(x, np.bincount(dr), width, color='#5f9ed1', edgecolor='None')
    # dis = plt.bar(x + width * 0.5, d, width, color='#f26c64', edgecolor='None')
    # swap = plt.bar(x + width * 0.5, s, width, color='#32a251', edgecolor='None')
    # ax.legend((mon[0], dis[0], swap[0]), ('Monotone', 'Discontinuous', 'Swap'), frameon=False)
    # plt.show()
    plt.ylim((0,2500000))
    plt.savefig('phrase_dist_freq_r', bbox_inches='tight')
    plt.close()

    return True


if __name__ == '__main__':
    # counts_phrase_lr_m = np.sum(pickle.load(open('counts_phrase_lr_m.p', 'rb')).values())
    # counts_phrase_lr_s = np.sum(pickle.load(open('counts_phrase_lr_s.p','rb')).values())
    # counts_phrase_lr_dr = np.sum(pickle.load(open('counts_phrase_lr_dr.p','rb')).values())
    # counts_phrase_lr_dl = np.sum(pickle.load(open('counts_phrase_lr_dl.p','rb')).values())
    # counts_word_lr_m = np.sum(pickle.load(open('counts_word_lr_m.p','rb')).values())
    # counts_word_lr_s = np.sum(pickle.load(open('counts_word_lr_s.p','rb')).values())
    # counts_word_lr_dr = np.sum(pickle.load(open('counts_word_lr_dr.p','rb')).values())
    # counts_word_lr_dl = np.sum(pickle.load(open('counts_word_lr_dl.p','rb')).values())
    # counts_phrase_rl_m = np.sum(pickle.load(open('counts_phrase_rl_m.p','rb')).values())
    # counts_phrase_rl_s = np.sum(pickle.load(open('counts_phrase_rl_s.p','rb')).values())
    # counts_phrase_rl_dr = np.sum(pickle.load(open('counts_phrase_rl_dr.p','rb')).values())
    # counts_phrase_rl_dl = np.sum(pickle.load(open('counts_phrase_rl_dl.p','rb')).values())
    # counts_word_rl_m = np.sum(pickle.load(open('counts_word_rl_m.p','rb')).values())
    # counts_word_rl_s = np.sum(pickle.load(open('counts_word_rl_s.p','rb')).values())
    # counts_word_rl_dr = np.sum(pickle.load(open('counts_word_rl_dr.p','rb')).values())
    # counts_word_rl_dl = np.sum(pickle.load(open('counts_word_rl_dl.p','rb')).values())

    # loading all pickles takes too long. These values are printed at the end of main.py execution.
    counts_phrase_lr_m = 11634195
    counts_phrase_lr_s = 396519
    counts_phrase_lr_dr = 5394488
    counts_phrase_lr_dl = 1558032
    counts_word_lr_m = 2310937
    counts_word_lr_s = 101864
    counts_word_lr_dr = 1072283
    counts_word_lr_dl = 322960
    counts_phrase_rl_m = 11623374
    counts_phrase_rl_s = 397747
    counts_phrase_rl_dr = 5375148
    counts_phrase_rl_dl = 1550384
    counts_word_rl_m = 2297146
    counts_word_rl_s = 125110
    counts_word_rl_dr = 929233
    counts_word_rl_dl = 372628

    phrase_m = counts_phrase_lr_m + counts_phrase_rl_m
    phrase_s = counts_phrase_lr_s+ counts_phrase_rl_s
    phrase_d = counts_phrase_lr_dr + counts_phrase_lr_dl + counts_phrase_rl_dr + counts_phrase_rl_dl

    word_m = counts_word_lr_m + counts_word_rl_m
    word_s = counts_word_lr_s + counts_word_rl_s
    word_d = counts_word_lr_dr + counts_word_lr_dl + counts_word_rl_dr + counts_word_rl_dl

    # histogram of phrase vs word events
    vals = [phrase_m, word_m, phrase_s, word_s, phrase_d, word_d]
    plot_phrase_vs_word(vals)

    # histogram of phrase events
    vals = [phrase_m, phrase_s, phrase_d]
    plot_phrase_events(vals)

    # histogram of phrase discontinuous reordering events
    vals = [counts_phrase_lr_dr, counts_phrase_lr_dl, counts_phrase_rl_dr, counts_phrase_rl_dl]
    plot_phrase_discontinuous(vals)

    # phrase discontinuous distortion
    plot_phrase_discontinuous_distortion()

    # word discontinuous distortion
    plot_word_discontinuous_distortion()

    # reordering events frequency wrt German-side phrase len
    plot_phrase_len_reor()

    # frequency of discontinuous-to-the-left and -to-the-right wrt distortion
    plot_phrase_len_discontinuous()

    print 'end'

