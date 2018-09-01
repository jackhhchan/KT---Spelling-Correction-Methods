"""
Collection of utility methods.
    
1. Approximate String Matching:
    # Neighbourhood Search
    # Global Edit Distance
    # N-gram Distance

2. Phonetics:
    # Soundex
    # Metaphone
    # Double Metaphone

3. Evaluation
4. Data Input helper functions
"""

from tqdm import tqdm
alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

####################################################
########### Approximate String Matching ############
####################################################
"""
Contains:
    1. Levenshtein
    2. Global Edit Distance (allow for different params)
"""

def levenshtein_minDist(misspells, dictionary):
    """
    Returns 
        1. ged_All, list of edit distances of misspelled words to all dictionary words.
    
        Row = misspell word, Column = dictionary word.
        i.e. gedAll[0][1] = misspells[0]'s ged to dictionary[1].

        2. suggestions, dictionary of misspelled word: suggestions

    Arguments:
    misspells        -- list of misspelled words, each separated by a new line.
    dictionary       -- list of dictionary words, each separated by a new line.
    num, numBreak    -- manual number entered to limit the number of 
                        misspelled words processed in misspells.
    """


    ################### Edit Distance ###################

    import editdistance     # Uses Levenshtein distance
    assert type(misspells) == list and type(dictionary) == list ,"Misspells or/and Dictionary is/are not list/s."
    
    print("Generating edit distances for a misspell words with all words in dictionary...")
    ged_All = list()    # Initiate list to store edit distances for all misspelled words.
    for misspell in tqdm(misspells):
        ged = list()
        for word in dictionary:
            # Evaluate the GED for misppelled word to all the words in dictionary
            ged.append(editdistance.eval(misspell, word))
        # Store misspell word's geds in row.
        ged_All.append(ged)


    ################### Suggestions ###################
   
    print("Generating suggestions...")
    suggestions = list()
    for i, globalEditDistances in enumerate(ged_All):

        minDistance = min(globalEditDistances)                 # Obtain minimum global distance for SOI

        suggestion = list()
        for d, distance in enumerate(globalEditDistances):
            if distance == minDistance:
                suggestion.append(dictionary[d])               # Generate suggestions list of indices corresponding to dictionary words.
    
        suggestions.append(suggestion)

    return suggestions

def levenshtein_limit(misspells, dictionary, limit):

    import editdistance

    suggestsCol = list()
    for misspell in tqdm(misspells):
        suggests = list()
        for i, word in enumerate(dictionary):
            ged = editdistance.eval(misspell, word)
            if ged <= limit:
                suggests.append(word)

        if len(suggests) == 0:
            suggests = ["N/A"]
        suggestsCol.append(suggests)

    return suggestsCol

def globalEditDistance(stringOne, stringTwo, params):
    

    assert len(params) == 4 and type(params) == tuple
    m, i, d, r = params
    # Match is smaller or equal to insert, delete or replace.
    assert m <= i or m <= d or m <= r

    # Length of misspell and dictionary word.
    stringOneLength = len(stringOne) + 1
    stringTwoLength = len(stringTwo) + 1
    matrixDim = (stringOneLength, stringTwoLength)

    # Initialize matrix
    import numpy as np
    A = np.zeros(matrixDim)
    for j in range(stringOneLength): A[j][0] = j*i
    for k in range(stringTwoLength): A[0][k] = k*d


    # Algorithm to turn string into global edit distance.
    for j in range(1, stringOneLength):
        for k in range(1, stringTwoLength):
            insertion = A[j][k-1] + i
            deletion = A[j-1][k] + d
            replace = A[j-1][k-1] + m if (stringOne[j-1] == stringTwo[k-1]) else A[j-1][k-1] + r
            A[j][k] = min(insertion, deletion, replace)
    
    return A[stringOneLength-1][stringTwoLength-1]


####################################################
############### Phonetics Functions ################
####################################################
"""
Contains:
    1. Soundex
    2. Metaphone
"""

def soundex(collection, zero=False):
    """
    Returns a soundexed encoded version of the collection.
    """

    from phonetics import soundex

    try:
        assert type(collection) == list
    except AssertionError:
        print("Input collection is not a list.")

    collectionEncoded = list()
    for i, word in enumerate(tqdm(collection)):
        wordEncoded = soundex(word)
        if not zero:    # Optional: remove 0s.
            wordEncoded = wordEncoded.strip('0')
        collectionEncoded.append(wordEncoded)
    
        
    return collectionEncoded

def metaphone(collection):
    """
    Returns a list of metaphone encoded collection.
    
    Arguments:
    collection  -- the list of words to be encoded using metaphone.
    limit       -- the limit to the words.
    """
    
    try:
        assert type(collection) == list or type(collection) == str
    except AssertionError:
        print("The collection for metaphone is not a string or a list.")

    from phonetics import metaphone

    if type(collection) == str:
        return metaphone(collection)
 
    collectionEncoded = list()
    for word in collection:
        wordEncoded = metaphone(word)
        collectionEncoded.append(wordEncoded)
        

    return collectionEncoded

def dMetaphone(collection):
    """
    Returns a list of metaphone encoded collection.
    
    Arguments:
    collection  -- the list of words to be encoded using metaphone.
    limit       -- the limit to the words.
    """
    
    try:
        assert type(collection) == list or type(collection) == str
    except AssertionError:
        print("The collection for metaphone is not a string or a list.")

    from phonetics import dmetaphone

    if type(collection) == str:
        return dmetaphone(collection)
 
    collectionEncoded = list()
    for word in collection:
        wordEncoded = dmetaphone(word)
        collectionEncoded.append(wordEncoded)
        

    return collectionEncoded

def phoneticsSuggestions(misEncoded, dictEncoded, dictionary):
    """
    Returns suggestions from dictionary where misEncoded = dictEncoded.

    Arguments:
    misEncoded      -- misspelled words encoded by the phonetic algo.
    dictEncoded     -- dictionary words encoded by the phonetic algo.
    dictionary      -- original dictionary words to return in the suggestions.
    """

    suggestions_all = list()
    for misspell in tqdm(misEncoded):
        suggestions = list()
        for i, word in enumerate(dictEncoded):
            if misspell == word:
                suggestions.append(dictionary[i])
        suggestions_all.append(suggestions)

    return suggestions_all


####################################################
################### Evaluation #####################
####################################################


def eval(suggestions, corrections):
    """
    Returns the precision and recall of suggestions.
    
    Arguments:
    suggestions     -- list of suggestions
    corrections     -- list of corrections
    """

    # Calculate precision and recall.
    numCorrect = 0
    totalPrecision = 0
    for i, suggestion in enumerate(tqdm(suggestions)):
        if corrections[i] in suggestion:
            numCorrect += 1
        totalSuggestions += len(suggestion)

    # Precision = number of correct suggestions (numPrecision) / total number of suggestions (totalPrecision).
    precision = float(numCorrect) / float(totalSuggestions)
    # Recall = number of correct suggestions (numCorrect) / total number of misspelled words.
    recall = float(numCorrect) / float(len(suggestions))
    
    return precision*100, recall*100


####################################################
########### Data Input Helper Functions ############
####################################################

# Paths to input files, misspelledWiki, correctWiki, dictionary
DICTIONARY_DIR = "data/dict.txt"
MISSPELLSWIKI_DIR = "data/wiki_misspell.txt"
CORRECTSWIKI_DIR = "data/wiki_correct.txt"
BIRKBECKMISSPELLS_DIR = "data/birkbeck_misspell.txt"
BIRKBECKCORRECTS_DIR = "data/birkbeck_correct.txt"


def processTextFiles(source):
    """
    Returns the document processed into a list.
    
    Argument:
    source      -- path to the document.
    """
    try:
        handle = open(source)

        document = list()
        for word in handle:
            document.append(word.strip())

    except FileNotFoundError:
        print ("Directory not found for one of the inputs.")
    except AttributeError:
        print ("Content in handle are not strings.")
    
    return document

def inputDictionary(dictionaryPath = DICTIONARY_DIR):
    """
    Returns dictionary

    Argument:
    dictionaryPath      -- path to the dictionary
    """
    
    dictionary = processTextFiles(dictionaryPath)
    print ("Number of words in dictionary: {0}".format(len(dictionary)))

    return dictionary

def inputDatasets(dataset):
    """
    Returns (misspells, corrections) in lists.

    Arguments:
    dataset     -- the dataset used.
    """
    if dataset == 'birkbeck':
        misspellsPath = BIRKBECKMISSPELLS_DIR
        correctsPath = BIRKBECKCORRECTS_DIR
    elif dataset == 'wiki':
        misspellsPath = MISSPELLSWIKI_DIR
        correctsPath = CORRECTSWIKI_DIR


    misspells = processTextFiles(misspellsPath)
    print ("Number of misspelled words: {0}".format(len(misspells)))

    corrects = processTextFiles(correctsPath)
    print ("Number of correct words: {0}".format(len(corrects)))

    assert len(misspells) == len(corrects), "Number of misspelled words != correct words!"

    return (misspells, corrects)

