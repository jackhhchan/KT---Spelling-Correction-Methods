import utils

dictionary = utils.inputDictionary()
(misspells_wiki, corrects_wiki) = utils.inputDatasets('wiki')
(misspells_birk, corrects_birk) = utils.inputDatasets('birkbeck')   

"""
Prints on console, the pairs of non-matching first letter in the misspelled and the correct word,
for the Wiki & Birkbeck dataset.
"""

num = 0
for i, misspell in enumerate(misspells_wiki):
    if misspell[0] != corrects_wiki[i][0]:
        num += 1

percentage = float(num)/float(len(misspells_wiki))
print("For wiki, pairs of non-matching first letter: {0}, thus percentage: {1}".format(num, percentage*100))

num = 0
for i, misspell in enumerate(misspells_birk):
    if misspell[0] != corrects_birk[i][0]:
        num += 1

percentage = float(num)/float(len(misspells_birk))
print("For birkbeck, pairs of non-matching first letter: {0}, thus percentage: {1}".format(num, percentage*100))