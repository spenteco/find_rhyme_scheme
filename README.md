# Notes from 1/3/22 #

If you've come from the memo of 1/3/22, then:

To check the rhymes and report the results, I run **01_extract_lgs.py** (it reads the all_lines_phonemes data and writes all_lg.9.json, which contains one hash for every 9 line stanza in FQ), then **13_try_phonk.py** (it reads all_lg.9.json and writes a bunch of messages to stdout, which I redirect to OUT.txt).

Then I **grep, sed, etc OUT.txt** to get numbers, isolate examples, etc.  E.g.,

<pre>
grep 'no match' OUT.txt | wc -l
grep 'phonk' OUT.txt | wc -l
grep 'exact' OUT.txt | wc -l
grep 'last_matching' OUT.txt | wc -l

grep '###' OUT.txt | grep 'no match' | wc -l
grep '###' OUT.txt | grep 'phonk' | wc -l
grep '###' OUT.txt | grep 'exact' | wc -l
grep '###' OUT.txt | grep 'last_matching' | wc -l
</pre>

all_lg.9.json contains 3,653 stanzas.  The process correctly identifies 2,872 (78.6%) as ababbcbcc.

These numbers are interesting (there are 32,877 lines of verse in the data):

*  We resolved 17,895 lines using sight rhyme and original spellings; only 68 were incorrectly resolved.  Note that when computing the percentage of lines resolved by sight, your demoninator should be 29,224 (3,653 * 8; first lines don't figure here); 60% of rhymes in FQ are resolvable by sight alone.
*  10,897 times, the line did not rhyme with any preceeding line (sometimes because it's the first line); 325 of these findings were wrong.  Some of these are my bugs.  Some are Spenser's.
*  We matched on exact phonemes only 2,648 times.  A shockingly small number.
*  phonk was used 1,437 times.  350 were incorrect.  However, please note that those 350 are the cost of fixing 1,087 other problems, so for now, they're worth it.


