import utils
from tqdm import tqdm

from utils import globalEditDistance

def main():

    ##### Setting up datasets #####
    # Dictionary:
    #       Dictionary -- 370k words
    # Datasets:
    # 1.    Wiki - common typos, 4453 words
    # 2.    Birkbeck - handwritten misspelled words, 34683 words

    dictionary = utils.inputDictionary()
    if args.dataset == 'wiki':
        (misspells, corrects) = utils.inputDatasets('wiki')
    elif args.dataset == 'birkbeck':
        (misspells, corrects) = utils.inputDatasets('birkbeck')   


    if args.type == 'ged-analyse':
        params = (0, 1, 1, 1) # match, insert, delete, replace
        # number closer to 0 suggests its more likely for the characters in comparison to be more likely to be a match

        resultHandle = open("globaleditdistance_analysis.txt", 'a')
        resultHandle.write("\n[Global Edit Distance Results] \n\n\n")
        resultHandle.write("[m, i, d, r] = {0}\n".format(params))


        limit = 1            # Set ged limit
        resultHandle.write("Limit used = {0}\n\n".format(limit))
        suggestsCol = list()    # Initiate suggestion collection list
        for misspell in tqdm(misspells):
            suggests = list()
            for i, word in enumerate(dictionary): 
                if word[0] != misspell[0]:                          # Skip the dictionary word if first character does not match.
                    continue
                ged = globalEditDistance(misspell, word, params)   # find ged between misspell and dict word
                if ged <= limit:
                    suggests.append(word)                           # suggest dict word if ged < gedLimit

            if len(suggests) == 0:
                suggests = ["N/A"]
            suggestsCol.append(suggests)
            resultHandle.write("{0} : {1}\n".format(misspell, suggests))  #  (misspell: suggests) to file.   



        precision, recall = utils.eval(suggestsCol, corrects)
        resultHandle.write("[Precision: {0}, Recall: {1}]\n\n".format(precision, recall))
        resultHandle.close()

    if args.type == 'levenshtein-dynamic':
        print("Note: This uses levenshtein distance and suggests based on min from all of ged")
        suggestions = utils.levenshtein_minDist(misspells, dictionary)
        precision, recall = utils.eval(suggestions, corrects)

        handle = open("approx_results.txt", 'a')
        handle.write("[{0}]\n".format(args.type.upper()))
        handle.write("Datasets: {0}\n\n".format(args.dataset.upper()))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()

    if args.type == 'levenshtein-limit':
        
        assert args.limit is not None, "Please enter limit."
        limit = int(args.limit)
        suggestions = utils.levenshtein_limit(misspells, dictionary, limit)
        
        precision, recall = utils.eval(suggestions, corrects)


        handle = open("approx_results.txt", 'a')
        handle.write("[{0}]\nLimit = {1}".format(args.type.upper(), args.limit))
        handle.write("Datasets: {0}\n\n".format(args.dataset.upper()))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', help = "Type of Approximate String Matching to be used.")
    parser.add_argument('-l', '--limit', help ="Limit of ged to make the suggestions.")
    parser.add_argument('-d', '--dataset', help = "Dataset to be used. (wiki or birkbeck)")


    args = parser.parse_args()
    assert (args.dataset == 'wiki' or args.dataset == 'birkbeck'), "Dataset must be wiki or birkbeck"

    main()
