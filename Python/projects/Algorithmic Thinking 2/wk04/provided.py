"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
# import urllib2
from urllib.request import urlopen

if DESKTOP:
    import matplotlib.pyplot as plt
    import rna_analysis as student
else:
    import simpleplot
    import userXX_XXXXXXX as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urlopen(filename)
    ykeys = str(scoring_file.readline(), 'utf-8')
    print (ykeys)
    ykeychars = ykeys.split()
    print (ykeychars)
    for line in scoring_file.readlines():
        line = str(line,'utf-8')
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urlopen(filename)
    protein_seq = str(protein_file.read(),'utf-8')
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urlopen(filename)

    # read in files as string
    words = str(word_file.read(),'utf-8')

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print ("Loaded a dictionary with", len(word_list), "words")
    return word_list


# Question 1:

HUMAN_SEQ = read_protein(HUMAN_EYELESS_URL)
FRUIT_SEQ = read_protein(FRUITFLY_EYELESS_URL)
PAM50_MARIX = read_scoring_matrix(PAM50_URL)
ALGN_MATRIX = student.compute_alignment_matrix(HUMAN_SEQ, FRUIT_SEQ, PAM50_MARIX, False)
print (student.compute_local_alignment(HUMAN_SEQ, FRUIT_SEQ, PAM50_MARIX, ALGN_MATRIX))

# Question 2:
