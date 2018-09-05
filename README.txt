(1) Program files:

approxCheck.py		-- uses global edit distances to generate and evaluate the suggestions.
phoneticsCheck.py 	-- uses phonetic algorithms to generate and evaluate the suggestions.
utils.py		-- contains all helper functions used in approxCheck.py and phoneticsCheck.py


(2) Packages used:
*fuzzy
obtained from: https://pypi.org/project/Fuzzy/

*phonetics
obtained from: https://pypi.org/project/phonetics/

*editdistance
obtained from: https://pypi.org/project/editdistance/


(3) Instructions:
To use approxCheck.py, enter command in console:

python approxCheck.py -t levenshtein-limit -d wiki -l 1
--To show help, use python approxCheck.py -h

To use phoneticsCheck.py, enter command in console:

python phoneticsCheck.py -t soundex -d wiki
-- to show help, use python phoneticsCheck.py -h


(4) Brief details:
The program works by first processing the input files. 
For edit distance, the distances for all dictionary words and the misspelled word are found.
Then the appropriate suggestions based on the limits are returned. The results are evaluated with the corrections using precision and recall.
Similarly, for soundex, all the dictionary words are first encoded, then the misspelled words. The appropriate suggestions based matches are 
returned. The results are evaluted with the corrections using precision and recall.



Note:
The path to the datasets should be changed correspondingly from utils.py. Under Input Helper Functions.