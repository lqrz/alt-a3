__author__ = 'root'

from phrases import extract_phrases
from phrases import alignments2Words
import codecs
import time
import sys
from collections import defaultdict
from collections import Counter
from operator import div

def dec(f):
    def helper(a, b):
        if b == 0:
            return 0.0
        else:
            return f(a, b)

    return helper


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
    f_out = codecs.open(output_filepath, 'wb', encoding='utf-8')

    #TODO: instantiate counters
    counts = defaultdict(lambda :defaultdict(lambda :defaultdict(int)))
    total_lr = Counter()
    total_rl = Counter()

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
            # nexts = [(p_de,p_en) for p_de,p_en in phrases if p_en[0] == pos_en[-1]+1] # for l-r
            nexts = phrases_begin[pos_en[-1]+1] # for l-r

            # lr_phrase_monotone = [(p_de,p_en) for p_de,p_en in phrases if p_en[0] == pos_en[-1]+1 and p_de[0] == pos_de[-1]+1]
            lr_phrase_monotone = [(p_de,p_en) for p_de,p_en in nexts if p_de[0] == pos_de[-1]+1]
            n_lr_phrase_monotone = len(lr_phrase_monotone)

            # lr_word_monotone = [(p_de,p_en) for p_de,p_en in phrases if p_en[0] == pos_en[-1]+1 and p_en[0] in de_alignment_dict.__getitem__(pos_de[-1]+1)]
            lr_word_monotone = [(p_de,p_en) for p_de,p_en in nexts if p_en[0] in de_alignment_dict.__getitem__(pos_de[-1]+1)]
            n_lr_word_monotone = len(lr_word_monotone)

            # lr_phrase_swap = [(p_de,p_en) for p_de,p_en in phrases if p_en[0] == pos_en[-1]+1 and p_de[-1] == pos_de[0]-1]
            lr_phrase_swap = [(p_de,p_en) for p_de,p_en in nexts if p_de[-1] == pos_de[0]-1]
            n_lr_phrase_swap = len(lr_phrase_swap)

            # lr_word_swap = [(p_de,p_en) for p_de,p_en in phrases if p_en[0] == pos_en[-1]+1 and p_en[0] in de_alignment_dict.__getitem__(pos_de[0]-1)]
            lr_word_swap = [(p_de,p_en) for p_de,p_en in nexts if p_en[0] in de_alignment_dict.__getitem__(pos_de[0]-1)]
            n_lr_word_swap = len(lr_word_swap)

            lr_phrase_discontinuous = [t for t in nexts if (t not in lr_phrase_monotone and t not in lr_phrase_swap)]
            n_lr_phrase_discontinuous_l = len([(p_de,p_en) for p_de,p_en in lr_phrase_discontinuous if pos_de[-1] < p_de[0]])
            n_lr_phrase_discontinuous_r = len(lr_phrase_discontinuous) - n_lr_phrase_discontinuous_l

            lr_word_discontinuous = [t for t in nexts if (t not in lr_word_monotone and t not in lr_word_swap)]
            n_lr_word_discontinuous_l = len([(p_de,p_en) for p_de,p_en in lr_word_discontinuous if pos_de[-1] < p_de[0]])
            n_lr_word_discontinuous_r = len(lr_word_discontinuous) - n_lr_word_discontinuous_l

            # previous = [(p_de,p_en) for p_de,p_en in phrases if p_en[-1] == pos_en[0]-1] # for r-l
            previous = phrases_end[pos_en[0]-1] # for r-l

            # rl_phrase_monotone = [(p_de,p_en) for p_de,p_en in phrases if p_en[-1] == pos_en[0]-1 and p_de[-1] == pos_de[0]-1]
            rl_phrase_monotone = [(p_de,p_en) for p_de,p_en in previous if p_de[-1] == pos_de[0]-1]
            n_rl_phrase_monotone = len(rl_phrase_monotone)

            # rl_word_monotone = [(p_de,p_en) for p_de,p_en in phrases if p_en[-1] == pos_en[0]-1 and p_en[-1] in de_alignment_dict.__getitem__(pos_de[0]-1)]
            rl_word_monotone = [(p_de,p_en) for p_de,p_en in previous if p_en[-1] in de_alignment_dict.__getitem__(pos_de[0]-1)]
            n_rl_word_monotone = len(rl_word_monotone)

            # rl_phrase_swap = [(p_de,p_en) for p_de,p_en in phrases if p_en[-1] == pos_en[0]-1 and p_de[0] == pos_de[-1]+1]
            rl_phrase_swap = [(p_de,p_en) for p_de,p_en in previous if p_de[0] == pos_de[-1]+1]
            n_rl_phrase_swap = len(rl_phrase_swap)

            # rl_word_swap = [(p_de,p_en) for p_de,p_en in phrases if p_en[-1] == pos_en[0]-1 and p_en[0] in de_alignment_dict.__getitem__(pos_de[-1]+1)]
            rl_word_swap = [(p_de,p_en) for p_de,p_en in previous if p_en[0] in de_alignment_dict.__getitem__(pos_de[-1]+1)]
            n_rl_word_swap = len(rl_word_swap)

            rl_phrase_discontinuous = [t for t in previous if (t not in rl_phrase_monotone and t not in rl_phrase_swap)]
            n_rl_phrase_discontinuous_l = len([(p_de,p_en) for p_de,p_en in rl_phrase_discontinuous if pos_de[0] > p_de[-1]])
            n_rl_phrase_discontinuous_r = len(rl_phrase_discontinuous) - n_rl_phrase_discontinuous_l

            rl_word_discontinuous = [t for t in previous if (t not in rl_word_monotone and t not in rl_word_swap)]
            n_rl_word_discontinuous_l = len([(p_de,p_en) for p_de,p_en in rl_word_discontinuous if pos_de[0] > p_de[-1]])
            n_rl_word_discontinuous_r = len(rl_word_discontinuous) - n_rl_word_discontinuous_l

            #TODO: update counters
            phrase_str = alignments2Words((pos_de, pos_en), line_de.strip().split(), line_en.strip().split())

            # update counter lr
            counts[phrase_str]['lr']['m'] += n_lr_phrase_monotone + n_lr_word_monotone
            counts[phrase_str]['lr']['s'] += n_lr_phrase_swap + n_lr_word_swap
            counts[phrase_str]['lr']['dr'] += n_lr_phrase_discontinuous_r + n_lr_word_discontinuous_r
            counts[phrase_str]['lr']['dl'] += n_lr_phrase_discontinuous_l + n_lr_word_discontinuous_l

            total_lr[phrase_str] += (n_lr_phrase_monotone + n_lr_word_monotone + \
                                     n_lr_phrase_swap + n_lr_word_swap + \
                                     n_lr_phrase_discontinuous_r + n_lr_word_discontinuous_r + \
                                     n_lr_phrase_discontinuous_l + n_lr_word_discontinuous_l)

            # update counter rl
            counts[phrase_str]['rl']['m'] += n_rl_phrase_monotone + n_rl_word_monotone
            counts[phrase_str]['rl']['s'] += n_rl_phrase_swap + n_rl_word_swap
            counts[phrase_str]['rl']['dr'] += n_rl_phrase_discontinuous_r + n_rl_word_discontinuous_r
            counts[phrase_str]['rl']['dl'] += n_rl_phrase_discontinuous_l + n_rl_word_discontinuous_l

            total_rl[phrase_str] += (n_rl_phrase_monotone + n_rl_word_monotone + \
                                     n_rl_phrase_swap + n_rl_word_swap + \
                                     n_rl_phrase_discontinuous_r + n_rl_word_discontinuous_r + \
                                     n_rl_phrase_discontinuous_l + n_rl_word_discontinuous_l)

    print 'Computing probabilities'
    sep = '|||'
    for phrase in counts.keys():
        p1 = dec(div)(counts[phrase]['lr']['m'], float(total_lr[phrase]))
        p2 = dec(div)(counts[phrase]['lr']['s'], float(total_lr[phrase]))
        p3 = dec(div)(counts[phrase]['lr']['dl'], float(total_lr[phrase]))
        p4 = dec(div)(counts[phrase]['lr']['dr'], float(total_lr[phrase]))
        p5 = dec(div)(counts[phrase]['rl']['m'], float(total_lr[phrase]))
        p6 = dec(div)(counts[phrase]['rl']['s'], float(total_lr[phrase]))
        p7 = dec(div)(counts[phrase]['rl']['dl'], float(total_lr[phrase]))
        p8 = dec(div)(counts[phrase]['rl']['dr'], float(total_lr[phrase]))

        probs_str = map(str,[p1,p2,p3,p4,p5,p6,p7,p8])

        f_out.write(' '.join([phrase[0],sep,phrase[1],sep]+probs_str+['\n']))

    f_out.close()

    print 'Elapsed time: ', time.time()-start