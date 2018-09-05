import utils
import timeit
import pickle
import os


def main():

    ##### Setting up datasets #####
    # Dictionary:
    #       Dictionary -- 370k words
    # Datasets:
    # 1.    Wiki - common typos, 4453 words
    # 2.    Birkbeck - handwritten misspelled words, 34683 words (Randomly sampled at 4453 words)

    dictionary = utils.inputDictionary()

    (misspells, corrects) = utils.inputDatasets(args)
     


    ####### Implementations ########
    if args.type == 'soundex':
        """ parameters: zero or no zeros."""
        zero = True
        print("Encoding dictionary and misspells for {0} using {1}...".format(args.dataset, args.type))
        dictEncoded = utils.soundex(dictionary, zero)
        misEncoded = utils.soundex(misspells, zero)
        print("Generating suggestions...")
        suggestions = utils.phoneticsSuggestions(misEncoded, dictEncoded, dictionary, args)
        
        precision, recall, numCorrect, totalSuggestions = utils.eval(suggestions, corrects)

        resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, len(misEncoded))


    if args.type == 'metaphone':
        print("Encoding dictionary and misspells for {0} using {1}...".format(args.dataset, args.type))
        dictEncoded = utils.metaphone(dictionary)
        misEncoded = utils.metaphone(misspells)
        print("Generating suggestions...")
        suggestions = utils.phoneticsSuggestions(misEncoded, dictEncoded, dictionary, args)

        precision, recall, numCorrect, totalSuggestions = utils.eval(suggestions, corrects)
        
        resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, len(misEncoded))


    if args.type == 'dmetaphone':
        
        print("Encoding dictionary and misspells for {0} using {1}...".format(args.dataset, args.type))

        dictEncoded = utils.dMetaphone(dictionary)   
        misEncoded = utils.dMetaphone(misspells)

        assert len(dictEncoded) == len(dictionary) and len(misEncoded) == len(misspells), "Files loaded from pickles are not correct."

        print("Generating suggestions...")
        suggestions = utils.phoneticsSuggestions(misEncoded, dictEncoded, dictionary, args)

        precision, recall, numCorrect, totalSuggestions = utils.eval(suggestions, corrects)
        
        resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, len(misEncoded))





def resultsOutputStream(args, precision, recall, numCorrect, totalSuggestions, sample_size):
        handle = open("phonetics_results.txt", 'a')
        handle.write("[{0}]\n".format(args.type.upper()))   # Name of phonetic algo used
        handle.write("Datasets: {0}\n".format(args.dataset.upper()))
        handle.write("Sample Size: {0}\n\n".format(sample_size))
        handle.write("Number of correct suggestions: {0}, Total number of suggestions: {1}\n".format(numCorrect, totalSuggestions))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "-t", "--type", help = "The phonetic mechanism to be used. [soundex, metaphone, dmetaphone]")
    parser.add_argument( "-d", "--dataset", help = "The dataset to be used. (wiki or birkbeck)")
    parser.add_argument('-s', '--samplesize', help = "Sample size for the datasets.")
    
    args = parser.parse_args()
    assert (args.dataset == 'wiki' or args.dataset == 'birkbeck'), "Dataset must be wiki or birkbeck"
    assert (args.type == 'soundex' or args.type == 'metaphone' or args.type == 'dmetaphone'), "Type must be soundex, metaphone or dmetaphone."
    if args.dataset == 'birkbeck' and args.samplesize is None:
        args.samplesize = 4453
    try:
        args.samplesize = int(args.samplesize)
    except:
        print("Please enter an integer for the sample size.")



    main()


