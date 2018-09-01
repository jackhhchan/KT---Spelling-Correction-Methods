import utils
import timeit


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


    ####### Implementations ########
    if args.type == 'soundex':
        """ parameters: zero or no zeros."""
        zero = True
        print("Encoding dictionary and misspells for {0} using {1}...".format(args.dataset, args.type))
        dictEncoded = utils.soundex(dictionary, zero)
        misEncoded = utils.soundex(misspells, zero)
        print("Generating suggestions...")
        suggestions = utils.phoneticsSuggestions(misEncoded, dictEncoded, dictionary)
        
        precision, recall = utils.eval(suggestions, corrects)

        handle = open("phonetics_results.txt", 'a')
        handle.write("[{0}]\nzero stay = {1}\n".format(args.type.upper(), str(zero)))
        handle.write("Datasets: {0}\n\n".format(args.dataset.upper()))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()

    if args.type == 'metaphone':
        print("Encoding dictionary and misspells for {0} using {1}...".format(args.dataset, args.type))
        dictEncoded = utils.metaphone(dictionary)
        misEncoded = utils.metaphone(misspells)
        print("Generating suggestions...")
        suggestions = utils.phoneticsSuggestions(misEncoded, dictEncoded, dictionary)

        precision, recall = utils.eval(suggestions, corrects)
        
        handle = open("phonetics_results.txt", 'a')
        handle.write("[{0}]\n\n".format(args.type.upper()))
        handle.write("Datasets: {0}\n\n".format(args.dataset.upper()))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()

    if args.type == 'dmetaphone':
        print("Encoding dictionary and misspells for {0} using {1}...".format(args.dataset, args.type))
        dictEncoded = utils.dmetaphone(dictionary)
        misEncoded = utils.dmetaphone(misspells)
        print("Generating suggestions...")
        suggestions = utils.phoneticsSuggestions(misEncoded, dictEncoded, dictionary)

        precision, recall = utils.eval(suggestions, corrects)
        
        handle = open("phonetics_results.txt", 'a')
        handle.write("[{0}]\n\n".format(args.type.upper()))
        handle.write("Datasets: {0}\n\n".format(args.dataset.upper()))
        handle.write("Precision = {0}, Recall = {1}\n\n\n".format(precision, recall))
        handle.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "-t", "--type", help = "The phonetic mechanism to be used.")
    parser.add_argument( "-d", "--dataset", help = "The dataset to be used. (wiki or birkbeck)")
    args = parser.parse_args()
    assert (args.dataset == 'wiki' or args.dataset == 'birkbeck'), "Dataset must be wiki or birkbeck"

    main()