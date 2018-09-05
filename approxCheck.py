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
        (misspells, corrects) = utils.inputDatasets(args)
    elif args.dataset == 'birkbeck':
        (misspells, corrects) = utils.inputDatasets(args)   

    # ged-analyse is for analysing using different parameters for global edit distance.
    if args.type == 'ged-analyse':
        m = int(args.params[0])
        i = int(args.params[1])
        d = int(args.params[2])
        r = int(args.params[3])
        params = (m, i, d, r) # match, insert, delete, replace
        # number closer to 0 suggests its more likely for the characters in comparison to be more likely to be a match

        resultHandle = open("ged-analyse.txt", 'a')
        resultHandle.write("[{0}]\n".format(args.type.upper()))
        resultHandle.write("Datasets: {0}\n".format(args.dataset.upper()))
        resultHandle.write("Sample size: {0}\n".format(len(misspells)))
        resultHandle.write("[m, i, d, r] = {0}\n\n".format(params))


        limit = int(args.limit)            # Set ged limit
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
            #resultHandle.write("{0} : {1}\n".format(misspell, suggests))  #  (misspell: suggests) to file.   



        precision, recall, numCorrect, totalSuggestions = utils.eval(suggestsCol, corrects)


        resultHandle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        resultHandle.close()

    if args.type == 'levenshtein-dynamic':
        print("Note: Generates suggestions based on minimum levenshtein distance possible for the misspelled word.")
        suggestions = utils.levenshtein_minDist(misspells, dictionary)
        precision, recall, numCorrect, totalSuggestions = utils.eval(suggestions, corrects)

        resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, len(misspells))

    if args.type == 'levenshtein-limit':
        
        assert args.limit is not None, "Please enter limit."
        limit = int(args.limit)
        suggestions = utils.levenshtein_limit(misspells, dictionary, limit)
        
        precision, recall, numCorrect, totalSuggestions = utils.eval(suggestions, corrects)

        resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, len(misspells), str(limit))




def resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, sample_size, limit='none'):
        handle = open("approx_results.txt", 'a')
        handle.write("[{0}]\n".format(args.type.upper()))
        handle.write("Datasets: {0}\n".format(args.dataset.upper()))
        handle.write("Sample size: {0}\n".format(sample_size))
        handle.write("Limit: {0}\n\n".format(limit))
        handle.write("numCorrect: {0}, totalSuggestions: {1}\n".format(numCorrect, totalSuggestions))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', help = "Type of Approximate String Matching to be used.\n [levenshtein-limit, levenshtein-dynamic, ged-analyse]")
    parser.add_argument('-l', '--limit', help ="Limit of ged to make the suggestions.")
    parser.add_argument('-d', '--dataset', help = "Dataset to be used. (wiki or birkbeck)")
    parser.add_argument('-s', '--samplesize', help = "Sample size for the datasets.")
    parser.add_argument('-p', '--params', help = "Parameters for ged analyse [m, i, d, r]")

    args = parser.parse_args()
    assert (args.dataset == 'wiki' or args.dataset == 'birkbeck'), "Dataset must be wiki or birkbeck"
    assert (args.type == 'levenshtein-limit' or args.type == 'levenshtein-dynamic' or args.type == 'ged-analyse'), "Type must be levenshtein-limit, levenshtein-dynamic or ged-analyse."
    if args.dataset == 'birkbeck' and args.samplesize is None:
        args.samplesize = 4453
    try:
        args.samplesize = int(args.samplesize)
    except:
        print("Please enter an integer for the sample size.")
    
    if args.type == 'ged-analyse':
        assert len(args.params) == 4 and args.limit is not None, "Please enter parameters and limit for ged-analyse."


    main()
