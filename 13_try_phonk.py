#!/home/spenteco/anaconda2/envs/py3/bin/python

import glob, re, json, sys, random
from phonk.rhymescore import RhymeComp
from collections import Counter

# RUN LIKE TO GET TEST DATA  
  
#   ./12_try_phonk.py | grep 'grep_sed_etc_test_data' | sed -E 's/.+test_data //g' | sed -E 's/$/,/g' > grep_sed_test_two.json

# FOLLOWED BY LIGHT EDITING OF grep_sed_test_data.json (or whatever)

# ----------------------------------------------------------------------

def divide_phones(phones):
    
    v = []
    c = []
    for p in phones:
        if re.sub('[AEIOUY]', '', p) == p:
            c.append(p)
        else:
            v.append(p)
            
    return ''.join(v), ''.join(c)
    
# ----------------------------------------------------------------------

def is_a_d_t_match(rhyme_phones_a, rhyme_phones_b):
    
    result = False
    
    sorted_rhymes = sorted([rhyme_phones_a, rhyme_phones_b])
    
    if sorted_rhymes[0].endswith(' D') and sorted_rhymes[1].endswith(' T') and \
        sorted_rhymes[0][:-1] == sorted_rhymes[1][:-1]:
            
        print('sorted_rhymes COOL', sorted_rhymes)
            
        result = True
    
    return result

def find_rhymes(all_lg, 
                ALL_A_RHYME=False,
                RULES_TO_TRY=['exact_phones', 'sight_rhyme', 'phonk']):

    EXPECTED_RHYME = 'ababbcbcc'

    for lg_n, lg in enumerate(all_lg):
        
        if ALL_A_RHYME:
            overide_rhyme = []
            for l in lg['text']:
                overide_rhyme.append('a')
            EXPECTED_RHYME = ''.join(overide_rhyme)
            
        debug_details = []

        terminal_words = [re.sub('\s+', 
                                    ' ', 
                                    re.sub('[^a-z]', ' ', l.lower()).strip()).split(' ')[-1]
                            for l in lg['text']]

        terminal_orig = [re.sub('\s+', 
                                    ' ', 
                                    re.sub('[^a-z]', ' ', l.lower()).strip()).split(' ')[-1]
                            for l in lg['orig']]
        
        has_bad_sound = False
        for r in lg['rhyme_sounds']:
            if r == None:
                has_bad_sound = True
        if has_bad_sound:
            continue

        rhyme_results = [-1 for l in lg['text']]
        rhyme_n = -1

        for a in range(0, len(lg['rhyme_sounds'])):

            rhyme_matches_index = -1
                
            b = a
                
            while True:
                    
                b = b - 1
                if b == -1:
                    break
                    
                rhyme_solved = False
                
                for rule in RULES_TO_TRY:
                
                    if rhyme_solved == False and rule == 'exact_phones': 
                        
                        clean_a = re.sub('[^ A-Z]', '', lg['rhyme_sounds'][a]).strip()
                        clean_b = re.sub('[^ A-Z]', '', lg['rhyme_sounds'][b]).strip()
                        
                        if clean_b == clean_a:
                                    
                            debug_details.append([str(lg_n), str(a),
                                            'exact', 
                                            terminal_words[a], terminal_words[b]])
                                            
                            rhyme_matches_index = b
                            rhyme_solved = True
                    
                    if rhyme_solved == False and rule == 'sight_rhyme': 
                    
                        word_a = [c for c in terminal_orig[a]]
                        word_a.reverse()
                        
                        word_b = [c for c in terminal_orig[b]]
                        word_b.reverse()
                        
                        last_matching_i = -1
                        last_matching_c = ''
                        
                        for i in range(0, len(word_a)):
                            if i < len(word_b):
                                if word_a[i] == word_b[i]:
                                    last_matching_i = i
                                    last_matching_c = word_a[i]
                                else:
                                    break
                                    
                        if last_matching_i >= 1 and last_matching_c in 'aeiouy':
                                
                            debug_details.append([str(lg_n), str(a), 
                                            'last_matching_i', str(last_matching_i), 
                                            terminal_orig[a], terminal_orig[b]])
                                            
                            rhyme_matches_index = b
                            rhyme_solved = True
                        
                    if rhyme_solved == False and rule == 'phonk': 
                            
                        clean_a = re.sub('[^ A-Z]', '', lg['rhyme_sounds'][a]).strip()
                        clean_b = re.sub('[^ A-Z]', '', lg['rhyme_sounds'][b]).strip()
                            
                        va, ca = divide_phones(clean_a.split(' '))
                        vb, cb = divide_phones(clean_b.split(' '))
                        
                        merged_b = ''.join(sorted([ca, cb]))
                        
                        if ca == cb:
                        
                            score = 666
                        
                            try:
                                score = RhymeComp([va], [vb]).get_score()
                            except KeyError:
                                print('KeyError', va, vb)
                            
                            merged_v = ''.join(sorted([c for c in va + vb]))
                            unique_v = ''.join(sorted(list(set(va + vb))))
                                
                            if len(merged_v) > len(unique_v):
                            
                                debug_details.append([str(lg_n), str(a),
                                                'phonk score', str(score), str(sorted([va, vb])),
                                                str(len(merged_v)), str(len(unique_v)),
                                                merged_v,
                                                unique_v,
                                                terminal_words[a], terminal_words[b]])
                                
                                rhyme_matches_index = b
                                rhyme_solved = True
                    
                if rhyme_solved:
                    break
                            
            if rhyme_matches_index == -1:
                
                if a == 2:
                                
                    debug_details.append([str(lg_n), str(a),
                                    'no match', 
                                    terminal_words[a],
                                    terminal_orig[a],
                                    lg['rhyme_sounds'][a], 
                                    terminal_words[0],
                                    terminal_orig[0],
                                    lg['rhyme_sounds'][0]])
                    
                else:
                                
                    debug_details.append([str(lg_n), str(a),
                                    'no match', 
                                    terminal_words[a],
                                    lg['rhyme_sounds'][a], 
                                    str(terminal_words),
                                    str(lg['rhyme_sounds']),
                                    str(terminal_orig)])
                                    
                rhyme_n += 1
                rhyme_results[a] = rhyme_n
            else:
                rhyme_results[a] = rhyme_results[rhyme_matches_index]
                    
        # --------------------------------------------------------------
        # REPORTING THE RESULTS
        # --------------------------------------------------------------

        letters = 'abcdefghijklmnop'

        rhyme_results_letters = ''.join([letters[a] for a in rhyme_results])
        error = 'OK   '
        if rhyme_results_letters != EXPECTED_RHYME:
            error = 'ERROR'
                    
        # --------------------------------------------------------------
        
        print()
        print(error, lg_n, rhyme_results_letters, terminal_words, lg['rhyme_sounds'])
        print()
        
        #if error == 'ERROR':
        if True:


            terminal_words = [re.sub('\s+', 
                                    ' ', 
                                    re.sub('[^a-z]', ' ', l.lower()).strip()).split(' ')[-1]
                            for l in lg['text']]
                            
            expected_letter_words = {}
            for c in EXPECTED_RHYME:
                expected_letter_words[c] = []
        
            first_problem_a = -1
        
            print()
            for a in range(0, len(rhyme_results_letters)):
                
                flag = ' '
                if rhyme_results_letters[a] != EXPECTED_RHYME[a]:
                    
                    flag = EXPECTED_RHYME[a]
                    
                    if first_problem_a == -1:
                        first_problem_a = a
                    
                expected_letter_words[EXPECTED_RHYME[a]].append([rhyme_results_letters[a],
                                                                        terminal_words[a],
                                                                        lg['rhyme_sounds'][a],
                                                                        terminal_orig[a]])
                
                print('\tLINE', rhyme_results_letters[a],
                        flag, EXPECTED_RHYME[a],
                        '\t', lg['text'][a])
                        
            print()
            print('\t', 'expected_letter_words')
            print()
            for letter, words in expected_letter_words.items():
                print('\t\t', letter, len(words), words)
            print()
            
            the_actual_letter_words = {}
            
            for letter, words in expected_letter_words.items():
                for w in words:
                    if w[0] not in the_actual_letter_words:
                        the_actual_letter_words[w[0]] = []
                    the_actual_letter_words[w[0]].append(w)
                        
            print()
            print('\t', 'the_actual_letter_words')
            print()
            for letter, words in the_actual_letter_words.items():
                print('\t\t', letter, len(words), words)
            print()
            
            expected_letters = ''.join(set(EXPECTED_RHYME))
            
            for letter, words in the_actual_letter_words.items():
                if letter in expected_letters:
                    
                    if letter == 'a' and len(words) != 2 or \
                        letter == 'b' and len(words) != 4 or \
                        letter == 'c' and len(words) != 3:
                            
                        print   ('\tCAUSES', 'lg_n', lg_n, 
                                '>> unexpected n words <<', 
                                'letter', letter,
                                'len(words)', len(words),
                                'words', words)
                else:
                    print   ('\tCAUSES', 'lg_n', lg_n, 
                            '>> the_actual_letter_words not in EXPECTED_RHYME <<', 
                            'letter', letter,
                            'words', words)
            
            for letter in list(expected_letter_words.keys()):
                
                actual_letters = [word[0] for word in expected_letter_words[letter]]
                actual_letters = sorted(list(set(actual_letters)))
                
                if len(actual_letters) == 1:
                    if letter != actual_letters[0]:
                        print   ('\tCAUSES', 'lg_n', lg_n, 
                                '>> dropped a letter << ', 
                                'len(actual_letters)',len(actual_letters),
                                'letter', letter,
                                'expected_letter_words', expected_letter_words[letter])
                else:
                    print('\tCAUSES', 'lg_n', lg_n, 
                            '>> missed rhyme <<', 
                            'len(actual_letters)',len(actual_letters),
                            'letter', letter,
                            'expected_letter_words', expected_letter_words[letter])
                        
            print()
            for dn, d in enumerate(debug_details):
                
                flag = '   '
                if dn == first_problem_a:
                    flag = '###'
                
                print('\t\tDEBUG', flag, ' '.join(d))
            
if __name__ == "__main__":

    LG_LENGTH = 9

    all_lg = json.load(open('all_lg.' + str(LG_LENGTH) + '.json', 'r', encoding='utf-8'))
    find_rhymes(all_lg, RULES_TO_TRY=['sight_rhyme', 'exact_phones', 'phonk'])
    #find_rhymes(all_lg, RULES_TO_TRY=['sight_rhyme', 'exact_phones'])
    #find_rhymes(all_lg)

    #all_lg = json.load(open('grep_sed_test_data.json', 'r', encoding='utf-8'))
    #find_rhymes(all_lg, ALL_A_RHYME=True)
