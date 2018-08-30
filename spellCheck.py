import numpy as np
from ApproximateStringMatch import globalEditDistance
from ApproximateStringMatch import eval
from ApproximateStringMatch import soundex
from ApproximateStringMatch import soundexSuggestions


########################################
########## Process Input Data ##########
########################################

def processTextFiles(source):
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
    

#### Input: dictionary, for suggesting correct responses.
print ("Processing list of dictionary words...")

dictionary = processTextFiles("data\dict.txt")
print ("Number of words in dictionary: {0}".format(len(dictionary)))

#### Input: misspells, to be analysed. (wiki)
print ("Processing list of misspelled words...")

MISSPELLSWIKI_DIR = "data\wiki_misspell.txt"
misspellsWiki = processTextFiles(MISSPELLSWIKI_DIR)
print ("Number of misspelled words: {0}".format(len(misspellsWiki)))

#### Input: corrects, to be evaluated with. (wiki)
print ("Processing list of correct words...")

CORRECTSWIKI_DIR = "data\wiki_correct.txt"
correctsWiki = processTextFiles(CORRECTSWIKI_DIR)
print ("Number of correct words: {0}".format(len(correctsWiki)))

assert len(misspellsWiki) == len(correctsWiki)

##############################################
############ Global Edit Distance ############
##############################################

#print ("Generating global edit distances for all the words in the dictionary...")

#ged_All, suggestions, suggestionsList = globalEditDistance(misspellsWiki, dictionary)

####### Returning results on console. ########

#print ("\nNow returning results...\n")
#print ("\nMisspelled word : Suggestions\n")
#for key in suggestions:
#    print("{0} : {1}".format(key, suggestions[key]))


#gedPrecision, gedRecall = eval(suggestionsList, correctsWiki)
#print("Global Edit Distance Precision: {0}".format(gedPrecision))
#print("Global Edit Distance Recall: {0}".format(gedRecall))




##############################################
################# Soundex ####################
##############################################

print("\nGenerating suggestions for misspelled words using soundex...\n")
num = 0

zero = False
misspellLimit = len(misspellsWiki)
dictionaryLimit = len(dictionary)
dictionary_soundex = soundexx(dictionary, zero, dictionaryLimit)
misspellsWiki_soundex = soundexx(misspellsWiki, zero, misspellLimit)
suggestions_soundex = soundexSuggestions(misspellsWiki_soundex, dictionary_soundex, dictionary)


soundexPrecision, soundexRecall = eval(suggestions_soundex, correctsWiki)

print("Soundex Precision: {0}".format(soundexPrecision))
print("Soundex Recall: {0}".format(soundexRecall))


########## Documenting results ###########
resultHandle = open('results.txt', 'a')
import time
currentDateTime = time.asctime(time.localtime(time.time()))
resultHandle.write('['+ currentDateTime + ']\n\n')
resultHandle.write('Soundex results:\n')
resultHandle.write('Dataset used: {0}, {1} \n'.format(MISSPELLSWIKI_DIR, CORRECTSWIKI_DIR))
resultHandle.write('Number of misspell words processed: {0}\n\n'.format(misspellLimit))
resultHandle.write('Precision: {0}, Recall: {1}'.format(soundexPrecision,soundexRecall))
resultHandle.write('\n\n\n')
resultHandle.close()
