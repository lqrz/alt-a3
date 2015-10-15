__author__ = 'root'

from phrases import extract_phrases
from phrases import alignments2Words
import codecs
import time
import sys
from collections import defaultdict
from collections import Counter
from operator import div
import pickle


def dec(f):
    def helper(a, b):
        if b == 0:
            return 0.0
        else:
            return f(a, b)

    return helper


def compute_probs(counts_lr_m, counts_lr_s, counts_lr_dl, counts_lr_dr,
                      counts_rl_m, counts_rl_s, counts_rl_dl, counts_rl_dr,
                      total_lr, total_rl, phrase_str):

    p1 = dec(div)(counts_lr_m[phrase_str], float(total_lr[phrase_str]))
    p2 = dec(div)(counts_lr_s[phrase_str], float(total_lr[phrase_str]))
    p3 = dec(div)(counts_lr_dl[phrase_str], float(total_lr[phrase_str]))
    p4 = dec(div)(counts_lr_dr[phrase_str], float(total_lr[phrase_str]))
    p5 = dec(div)(counts_rl_m[phrase_str], float(total_rl[phrase_str]))
    p6 = dec(div)(counts_rl_s[phrase_str], float(total_rl[phrase_str]))
    p7 = dec(div)(counts_rl_dl[phrase_str], float(total_rl[phrase_str]))
    p8 = dec(div)(counts_rl_dr[phrase_str], float(total_rl[phrase_str]))

    return p1,p2,p3,p4,p5,p6,p7,p8


def save_to_file(f_out,p1,p2,p3,p4,p5,p6,p7,p8,phrase):
    sep = '|||'
    probs_str = map(str, [p1, p2, p3, p4, p5, p6, p7, p8])
    f_out.write(' '.join([phrase[0], sep, phrase[1], sep] + probs_str + ['\n']))

    return True


if __name__=='__main__':

    start = time.time()

    # debug file paths
    en_filepath = 'prueba.en'
    de_filepath = 'prueba.de'
    align_filepath = 'prueba.aligned'
    output_filepath = 'prueba.output'

    if len(sys.argv) == 5:
        en_filepath = sys.argv[1]
        de_filepath = sys.argv[2]
        align_filepath = sys.argv[3]
        output_filepath = sys.argv[4]
    elif len(sys.argv) > 1:
        print 'Error in params'
        exit()

    # max phrase length
    max_phrase_len = 7

    # file objects
    f_en = codecs.open(en_filepath, 'rb', encoding='utf-8')
    f_de = codecs.open(de_filepath, 'rb', encoding='utf-8')
    f_align = open(align_filepath, 'rb')
    f_out_phrase = codecs.open('phrase_'+output_filepath, 'wb', encoding='utf-8')
    f_out_word = codecs.open('word_'+output_filepath, 'wb', encoding='utf-8')

    counts_phrase_lr_m = Counter()
    counts_phrase_lr_s = Counter()
    counts_phrase_lr_dr = Counter()
    counts_phrase_lr_dl = Counter()

    total_phrase_lr = Counter()

    counts_word_lr_m = Counter()
    counts_word_lr_s = Counter()
    counts_word_lr_dr = Counter()
    counts_word_lr_dl = Counter()

    total_word_lr = Counter()

    counts_phrase_rl_m = Counter()
    counts_phrase_rl_s = Counter()
    counts_phrase_rl_dr = Counter()
    counts_phrase_rl_dl = Counter()

    total_phrase_rl = Counter()

    counts_word_rl_m = Counter()
    counts_word_rl_s = Counter()
    counts_word_rl_dr = Counter()
    counts_word_rl_dl = Counter()

    total_word_rl = Counter()

    phrase_discont_distance_lr_l = []
    phrase_discont_distance_lr_r = []
    phrase_discont_distance_rl_l = []
    phrase_discont_distance_rl_r = []

    word_discont_distance_lr_l = []
    word_discont_distance_lr_r = []
    word_discont_distance_rl_l = []
    word_discont_distance_rl_r = []

    phrase_len_reor_m = defaultdict(int)
    phrase_len_reor_s = defaultdict(int)
    phrase_len_reor_d = defaultdict(int)

    print 'Iterating sentences'
    # iterate sentences
    start_sent = time.time()
    for i, line_en in enumerate(f_en):
        if (i+1) % 1000 == 0:
            print 'Sentences processed: ', i+1, time.time()-start_sent
            start_sent = time.time()
        line_de = f_de.readline()
        line_align = f_align.readline()
        phrases_str, phrases, data_alignments, de_alignment_dict, en_alignment_dict, phrases_begin, phrases_end = extract_phrases(line_en, line_de, line_align, max_phrase_len)

        for pos_de, pos_en in phrases:

            # get possible next phrase
            nexts = [t for t in phrases_begin[pos_en[-1]+1] if pos_de[-1] not in t[0]] # for l-r

            lr_phrase_monotone = [(p_de,p_en) for p_de,p_en in nexts if p_de[0] == pos_de[-1]+1]
            n_lr_phrase_monotone = len(lr_phrase_monotone)

            # lr_word_monotone = [(p_de,p_en) for p_de,p_en in nexts if p_en[0] in de_alignment_dict.__getitem__(pos_de[-1]+1)]
            # n_lr_word_monotone = len(lr_word_monotone)
            n_lr_word_monotone = int(pos_en[-1]+1 in de_alignment_dict.__getitem__(pos_de[-1]+1))

            lr_phrase_swap = [(p_de,p_en) for p_de,p_en in nexts if p_de[-1] == pos_de[0]-1]
            n_lr_phrase_swap = len(lr_phrase_swap)

            # lr_word_swap = [(p_de,p_en) for p_de,p_en in nexts if p_en[0] in de_alignment_dict.__getitem__(pos_de[0]-1)]
            # n_lr_word_swap = len(lr_word_swap)
            n_lr_word_swap = int(pos_en[-1]+1 in de_alignment_dict.__getitem__(pos_de[0]-1))

            lr_phrase_discontinuous = [t for t in nexts if (t not in lr_phrase_monotone and t not in lr_phrase_swap)]
            n_lr_phrase_discontinuous_l = len([(p_de,p_en) for p_de,p_en in lr_phrase_discontinuous if pos_de[0] > p_de[-1]])
            n_lr_phrase_discontinuous_r = len(lr_phrase_discontinuous) - n_lr_phrase_discontinuous_l

            # #TODO: remove
            # if 4 in [p_de[0] - pos_de[-1] -1 for p_de,p_en in lr_phrase_discontinuous if pos_de[-1] < p_de[0]]:
            #     print 'stop'

            # stats
            phrase_discont_distance_lr_l.extend([pos_de[0] - p_de[-1] -1 for p_de,p_en in lr_phrase_discontinuous if pos_de[0] > p_de[-1]])
            phrase_discont_distance_lr_r.extend([p_de[0] - pos_de[-1] -1 for p_de,p_en in lr_phrase_discontinuous if pos_de[-1] < p_de[0]])

            # lr_word_discontinuous = [t for t in nexts if (t not in lr_word_monotone and t not in lr_word_swap)]
            # n_lr_word_discontinuous_l = len([(p_de,p_en) for p_de,p_en in lr_word_discontinuous if pos_de[-1] < p_de[0]])
            # n_lr_word_discontinuous_r = len(lr_word_discontinuous) - n_lr_word_discontinuous_l
            en_al = en_alignment_dict.__getitem__(pos_en[-1] + 1)
            n_lr_word_discontinuous_r = int(any([x > pos_de[-1]+2 for x in en_al]))
            n_lr_word_discontinuous_l = int(any([x < pos_de[0]-2 for x in en_al]))

            #stats
            if any([x > pos_de[-1]+2 for x in en_al]):
                word_discont_distance_lr_r.append(min([x - pos_de[-1] -1 for x in en_al if x > pos_de[-1]+2]))
            if any([x < pos_de[0]-2 for x in en_al]):
                word_discont_distance_lr_l.append(min([pos_de[0] - x -1 for x in en_al if pos_de[0]-2 > x]))

            previous = [t for t in phrases_end[pos_en[0]-1] if pos_de[0] not in t[0]] # r-l

            rl_phrase_monotone = [(p_de,p_en) for p_de,p_en in previous if p_de[-1] == pos_de[0]-1]
            n_rl_phrase_monotone = len(rl_phrase_monotone)

            # rl_word_monotone = [(p_de,p_en) for p_de,p_en in previous if p_en[-1] in de_alignment_dict.__getitem__(pos_de[0]-1)]
            # n_rl_word_monotone = len(rl_word_monotone)
            n_rl_word_monotone = int(pos_en[0]-1 in de_alignment_dict.__getitem__(pos_de[0]-1))

            rl_phrase_swap = [(p_de,p_en) for p_de,p_en in previous if p_de[0] == pos_de[-1]+1]
            n_rl_phrase_swap = len(rl_phrase_swap)

            # rl_word_swap = [(p_de,p_en) for p_de,p_en in previous if p_en[0] in de_alignment_dict.__getitem__(pos_de[-1]+1)]
            # n_rl_word_swap = len(rl_word_swap)
            n_rl_word_swap = int(pos_en[0]-1 in de_alignment_dict.__getitem__(pos_de[-1]+1))

            rl_phrase_discontinuous = [t for t in previous if (t not in rl_phrase_monotone and t not in rl_phrase_swap)]
            n_rl_phrase_discontinuous_l = len([(p_de,p_en) for p_de,p_en in rl_phrase_discontinuous if pos_de[-1] < p_de[0]])
            n_rl_phrase_discontinuous_r = len(rl_phrase_discontinuous) - n_rl_phrase_discontinuous_l

            phrase_discont_distance_rl_l.extend([p_de[0]-pos_de[-1]-1 for p_de,p_en in rl_phrase_discontinuous if pos_de[-1] < p_de[0]])
            phrase_discont_distance_rl_r.extend([pos_de[0]-p_de[-1]-1 for p_de,p_en in rl_phrase_discontinuous if pos_de[0] > p_de[-1]])

            # rl_word_discontinuous = [t for t in previous if (t not in rl_word_monotone and t not in rl_word_swap)]
            # n_rl_word_discontinuous_l = len([(p_de,p_en) for p_de,p_en in rl_word_discontinuous if pos_de[0] > p_de[-1]])
            # n_rl_word_discontinuous_r = len(rl_word_discontinuous) - n_rl_word_discontinuous_l

            en_al = en_alignment_dict.__getitem__(pos_en[0]-1)
            # n_rl_word_discontinuous_l = int(en_al < pos_de[0]) if en_al else 0
            # n_rl_word_discontinuous_r = int(en_al > pos_de[-1]) if en_al else 0
            n_rl_word_discontinuous_r = int(any([x < pos_de[0]-2 for x in en_al]))
            n_rl_word_discontinuous_l = int(any([x > pos_de[-1]+2 for x in en_al]))

            #stats
            if any([x < pos_de[0]-2 for x in en_al]):
                word_discont_distance_rl_r.append(min([pos_de[0]-x-1 for x in en_al if pos_de[0]-2 > x]))
            if any([x > pos_de[-1]+2 for x in en_al]):
                word_discont_distance_rl_l.append(min([x-pos_de[-1]-1 for x in en_al if x > pos_de[-1]+2]))

            phrase_str = alignments2Words((pos_de, pos_en), line_de.strip().split(), line_en.strip().split())

            counts_phrase_lr_m[phrase_str] += n_lr_phrase_monotone
            counts_phrase_lr_s[phrase_str] += n_lr_phrase_swap
            counts_phrase_lr_dr[phrase_str] += n_lr_phrase_discontinuous_r
            counts_phrase_lr_dl[phrase_str] += n_lr_phrase_discontinuous_l

            total_phrase_lr[phrase_str] += n_lr_phrase_monotone + n_lr_phrase_swap + n_lr_phrase_discontinuous_r + n_lr_phrase_discontinuous_l

            counts_word_lr_m[phrase_str] += n_lr_word_monotone
            counts_word_lr_s[phrase_str] += n_lr_word_swap
            counts_word_lr_dr[phrase_str] += n_lr_word_discontinuous_r
            counts_word_lr_dl[phrase_str] += n_lr_word_discontinuous_l

            total_word_lr[phrase_str] += n_lr_word_monotone + n_lr_word_swap + n_lr_word_discontinuous_r + n_lr_word_discontinuous_l

            counts_phrase_rl_m[phrase_str] += n_rl_phrase_monotone
            counts_phrase_rl_s[phrase_str] += n_rl_phrase_swap
            counts_phrase_rl_dr[phrase_str] += n_rl_phrase_discontinuous_r
            counts_phrase_rl_dl[phrase_str] += n_rl_phrase_discontinuous_l

            total_phrase_rl[phrase_str] += n_rl_phrase_monotone + n_rl_phrase_swap + n_rl_phrase_discontinuous_r + n_rl_phrase_discontinuous_l

            counts_word_rl_m[phrase_str] += n_rl_word_monotone
            counts_word_rl_s[phrase_str] += n_rl_word_swap
            counts_word_rl_dr[phrase_str] += n_rl_word_discontinuous_r
            counts_word_rl_dl[phrase_str] += n_rl_word_discontinuous_l

            total_word_rl[phrase_str] += n_rl_word_monotone + n_rl_word_swap + n_rl_word_discontinuous_r + n_rl_word_discontinuous_l

            german_len = len(pos_de)
            phrase_len_reor_m[german_len] += n_lr_phrase_monotone + n_rl_phrase_monotone
            phrase_len_reor_s[german_len] += n_lr_phrase_swap + n_rl_phrase_swap
            phrase_len_reor_d[german_len] += n_lr_phrase_discontinuous_r + n_lr_phrase_discontinuous_l + \
                n_rl_phrase_discontinuous_r + n_rl_phrase_discontinuous_l

    print 'Computing probabilities'
    # for phrase in counts.keys():
    for phrase in counts_phrase_lr_m.keys():
        p1,p2,p3,p4,p5,p6,p7,p8 = compute_probs(counts_phrase_lr_m, counts_phrase_lr_s, counts_phrase_lr_dl, counts_phrase_lr_dr,
                      counts_phrase_rl_m, counts_phrase_rl_s, counts_phrase_rl_dl, counts_phrase_rl_dr,
                      total_phrase_lr, total_phrase_rl, phrase)

        save_to_file(f_out_phrase,p1,p2,p3,p4,p5,p6,p7,p8,phrase)

        p1,p2,p3,p4,p5,p6,p7,p8 = compute_probs(counts_word_lr_m, counts_word_lr_s, counts_word_lr_dl, counts_word_lr_dr,
                      counts_word_rl_m, counts_word_rl_s, counts_word_rl_dl, counts_word_rl_dr,
                      total_word_lr, total_word_rl, phrase)

        save_to_file(f_out_word,p1,p2,p3,p4,p5,p6,p7,p8,phrase)

    f_out_phrase.close()
    f_out_word.close()

    print 'Pickling structures'
    pickle.dump(counts_phrase_lr_m, open('counts_phrase_lr_m.p','wb'))
    pickle.dump(counts_phrase_lr_s, open('counts_phrase_lr_s.p','wb'))
    pickle.dump(counts_phrase_lr_dr, open('counts_phrase_lr_dr.p','wb'))
    pickle.dump(counts_phrase_lr_dl, open('counts_phrase_lr_dl.p','wb'))
    pickle.dump(counts_word_lr_m, open('counts_word_lr_m.p','wb'))
    pickle.dump(counts_word_lr_s, open('counts_word_lr_s.p','wb'))
    pickle.dump(counts_word_lr_dr, open('counts_word_lr_dr.p','wb'))
    pickle.dump(counts_word_lr_dl, open('counts_word_lr_dl.p','wb'))
    pickle.dump(counts_phrase_rl_m, open('counts_phrase_rl_m.p','wb'))
    pickle.dump(counts_phrase_rl_s, open('counts_phrase_rl_s.p','wb'))
    pickle.dump(counts_phrase_rl_dr, open('counts_phrase_rl_dr.p','wb'))
    pickle.dump(counts_phrase_rl_dl, open('counts_phrase_rl_dl.p','wb'))
    pickle.dump(counts_word_rl_m, open('counts_word_rl_m.p','wb'))
    pickle.dump(counts_word_rl_s, open('counts_word_rl_s.p','wb'))
    pickle.dump(counts_word_rl_dr, open('counts_word_rl_dr.p','wb'))
    pickle.dump(counts_word_rl_dl, open('counts_word_rl_dl.p','wb'))
    pickle.dump(total_phrase_lr, open('total_phrase_lr.p','wb'))
    pickle.dump(total_word_lr, open('total_word_lr.p','wb'))
    pickle.dump(total_phrase_rl, open('total_phrase_rl.p','wb'))
    pickle.dump(total_word_rl, open('total_word_rl.p','wb'))
    pickle.dump(phrase_discont_distance_lr_l, open('phrase_discont_distance_lr_l.p','wb'))
    pickle.dump(phrase_discont_distance_lr_r, open('phrase_discont_distance_lr_r.p','wb'))
    pickle.dump(phrase_discont_distance_rl_l, open('phrase_discont_distance_rl_l.p','wb'))
    pickle.dump(phrase_discont_distance_rl_r, open('phrase_discont_distance_rl_r.p','wb'))

    pickle.dump(word_discont_distance_rl_r, open('word_discont_distance_rl_r.p','wb'))
    pickle.dump(word_discont_distance_rl_l, open('word_discont_distance_rl_l.p','wb'))
    pickle.dump(word_discont_distance_lr_r, open('word_discont_distance_lr_r.p','wb'))
    pickle.dump(word_discont_distance_lr_l, open('word_discont_distance_lr_l.p','wb'))

    pickle.dump(phrase_len_reor_m, open('phrase_len_reor_m.p','wb'))
    pickle.dump(phrase_len_reor_s, open('phrase_len_reor_s.p','wb'))
    pickle.dump(phrase_len_reor_d, open('phrase_len_reor_d.p','wb'))

    print 'Elapsed time: ', time.time()-start

    print sum(counts_phrase_lr_m.values())
    print sum(counts_phrase_lr_s.values())
    print sum(counts_phrase_lr_dr.values())
    print sum(counts_phrase_lr_dl.values())
    print sum(counts_word_lr_m.values())
    print sum(counts_word_lr_s.values())
    print sum(counts_word_lr_dr.values())
    print sum(counts_word_lr_dl.values())
    print sum(counts_phrase_rl_m.values())
    print sum(counts_phrase_rl_s.values())
    print sum(counts_phrase_rl_dr.values())
    print sum(counts_phrase_rl_dl.values())
    print sum(counts_word_rl_m.values())
    print sum(counts_word_rl_s.values())
    print sum(counts_word_rl_dr.values())
    print sum(counts_word_rl_dl.values())