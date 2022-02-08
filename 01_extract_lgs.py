#!/home/spenteco/anaconda2/envs/py3/bin/python

import glob, re, json, copy, sys
from syllabify import syllabify

#LG_LENGTH = int(sys.argv[1])
LG_LENGTH = 9

#FQ_TCP_IDS = ['A12777', 'A12778']
#FQ_TCP_IDS = ['A12778']

all_lg = []

for f_n, f in enumerate(glob.glob('/home/spenteco/0/all_lines_phonemes/*.txt')):
    
    if f_n % 1000 == 0:
        print('processing', f_n)
    
    tcp_id = f.split('/')[-1].split('.')[0]

    #if tcp_id not in FQ_TCP_IDS:
    #    continue
    
    text = open(f, 'r', encoding='utf-8').read().replace('<br/>	<br/>	<br/>	<br/>', '')
    
    paragraphs = text.split('\n\n\n')
    
    for p in paragraphs:
        
        parsed_lines = []

        lines = p.split('\n\n')
        
        if len(lines) == LG_LENGTH:
            
            p_lines = []
            p_orig = []
            p_rhyme_sounds = []
            p_rhyme_sound_types = []
            p_line_stresses = []
            p_line_phonemes = []

            good_stanza = True
            
            for l in lines:

                line_text = []
                line_orig = []
                line_pos = []
                line_phonemes = []
                line_arpabet_types = []
                line_stresses = []
                possible_rhyme_sound = None
                
                tokens = l.split('\n')
                
                for t in tokens:

                    cols = t.split('\t')

                    if len(cols) > 5:

                        line_orig.append(cols[0])
                        line_text.append(cols[1])
                        line_pos.append(cols[3])
                        line_phonemes.append(cols[4])
                        line_arpabet_types.append(cols[7])
                        line_stresses.append(cols[5])
                        
                    elif len(cols) == 4 and cols[3] == '<pc/>':

                        line_orig.append(cols[0])
                        line_text.append(cols[1])
                    
                syllables = []
                
                if len(line_phonemes) == 0:
                    good_stanza = False
                else:

                    try:
                        syllables = syllabify(line_phonemes[-1].upper().split('/'))
                    except ValueError:
                        pass

                    possible_rhyme_sound = None

                    if len(syllables) > 0:

                        possible_rhyme_sound = (' '.join(syllables[-1][1]) +  \
                                                ' ' + \
                                                ' '.join(syllables[-1][2])).strip()

                    possible_rhyme_sound_type = None

                    if possible_rhyme_sound != None:
                        type_parts = line_arpabet_types[-1].split('/')
                        type_parts.reverse()
                        selected_type_parts = type_parts[:len(possible_rhyme_sound.split(' '))]
                        selected_type_parts.reverse()
                        possible_rhyme_sound_type = ' '.join(selected_type_parts)

                    p_lines.append(' '.join(line_text))
                    p_orig.append(' '.join(line_orig))
                    p_rhyme_sounds.append(possible_rhyme_sound)  
                    p_rhyme_sound_types.append(possible_rhyme_sound_type) 
                    p_line_stresses.append(line_stresses) 
                    p_line_phonemes.append(line_phonemes)
            
            if good_stanza and 'fla' not in line_pos:

                all_lg.append({'tcp_id': tcp_id,
                                      'text': p_lines, 
                                      'orig': p_orig, 
                                      'line_phonemes': p_line_phonemes,
                                      'rhyme_sounds': p_rhyme_sounds,
                                      'rhyme_sound_types': p_rhyme_sound_types,
                                      'line_stresses': p_line_stresses})
                

f = open('all_lg.' + str(LG_LENGTH) + '.json', 'w', encoding='utf-8')
f.write(json.dumps(all_lg, indent=4, ensure_ascii=False))
f.close()

print(len(all_lg))
print(all_lg[0])
