"""
Collection of Approximate String Matching Methods:
    
    # Neighbourhood Search
    # Global Edit Distance
    # N-gram Distance
"""

alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def neighbourhoodSearch(string, dict, k):
    """ Return a list of all k neighbours of string found in reference dictionary. """

    neighbours = list()
    string = list(string)
    
    # Generate all neighbours of string with k changes.
    inserts = list()

    for i in range(len(string)+1):
        for alphabet in alphabets:
            string.insert(i, alphabet)
            inserts.append(string)
            string.pop(i)
    
    print (inserts)
    print (len(inserts))


def globalEditDistance(misspells, dictionary, num = 0, numBreak=20):
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
    try:
        assert type(misspells) == list
        assert type(dictionary) == list
    except AssertionError:
        print ("Misspells or/and Dictionary is/are not list/s.")

    
    ged_All = list()    # Initiate list to store edit distances for all misspelled words.
    suggestions = dict()

    for i, misspell in enumerate(misspells):
        ged = list()
        for w, word in enumerate(dictionary):
            # Evaluate the GED for misppelled word to all the words in dictionary
            ged.append(editdistance.eval(misspell, word))
        # Store misspell word's geds in row.
        ged_All.append(ged)

        num += 1
        if num == numBreak:
            break

    ################### Suggestions ###################

    suggestions = dict()
    suggestionsList = list()
    for i, globalEditDistances in enumerate(ged_All):

        #print ("\nString of interest: {0}".format(misspellsWiki[i]))

        minDistance = min(globalEditDistances)          # Obtain minimum global distance for SOI


        suggestionsIndex = list()
        for d, distance in enumerate(globalEditDistances):
            if distance == minDistance:
                suggestionsIndex.append(d)               # Generate suggestions list of indices corresponding to dictionary words.
    
        suggestion = list()
        for index in suggestionsIndex:
            suggestion.append(dictionary[index])
    
        suggestions[misspells[i]] = suggestion          # misspelled word : suggestions
        suggestionsList.append(suggestion)

    return ged_All, suggestions, suggestionsList


def eval(suggestions, corrections):
    # Calculate precision and recall.
    numCorrect = 0
    totalPrecision = 0
    for i, suggestion in enumerate(suggestions):
        if corrections[i] in suggestion:
            numCorrect += 1
        totalPrecision += len(suggestion)

    # Precision = number of correct suggestions (numPrecision) / total number of suggestions (totalPrecision).
    precision = float(numCorrect) / float(totalPrecision)
    # Recall = number of correct suggestions (numCorrect) / total number of misspelled words.
    recall = float(numCorrect) / float(len(suggestions))
    return precision, recall


def soundex(collection, zero=False, limit=9999999):
    """
    Returns a soundexed encoded version of the collection.
    """

    from phonetics import soundex

    try:
        assert type(collection) == list
    except AssertionError:
        print("Input collection is not a list.")

    collectionEncoded = list()
    num = 0
    for i, word in enumerate(collection):
        wordEncoded = soundex(word)
        if not zero:    # Optional: remove 0s.
            wordEncoded = wordEncoded.strip('0')
        collectionEncoded.append(wordEncoded)
        num += 1
        if num == limit: # Optional: limit for no. element to be encoded.
            break

    
        
    return collectionEncoded

def soundexSuggestions(misspells_soundex, dictionary_soundex, dictionary):
    """
    Returns soundex suggestions for the misspelled words from the dictionary.
    """

    suggestions_all = list()
    for misspells in misspells_soundex:
        suggestions = list()
        for i, word in enumerate(dictionary_soundex):
            if misspells == word:
                suggestions.append(dictionary[i])
        suggestions_all.append(suggestions)

    return suggestions_all