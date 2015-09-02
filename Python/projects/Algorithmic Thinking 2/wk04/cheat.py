"""
Algorithmic Thinking - Module 4
10-19-2014
Dynamic Programming and Sequence Alignment
Applications to genomics and beyond
Application File
"""
import math
import random
# import urllib2
from urllib.request import urlopen
import matplotlib.pyplot as plt
import rna_analysis as prj4



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
    ykeys = str(scoring_file.readline(),'utf-8')
    ykeychars = ykeys.split()
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
    protein_seq = str(protein_file.read(), 'utf-8')
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
    words = str(word_file.read(), 'utf-8')

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print ("Loaded a dictionary with", len(word_list), "words")
    return word_list


def question_one():
    """
    Compute local alignments and sequences of Human Eyeless Protein and Fruitfly Eyeless Protein
    """
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    human_seq = read_protein(HUMAN_EYELESS_URL)
    fly_seq = read_protein(FRUITFLY_EYELESS_URL)
    align_matrix = prj4.compute_alignment_matrix(human_seq, fly_seq, scoring_matrix, False)
    result = prj4.compute_local_alignment(human_seq, fly_seq, scoring_matrix, align_matrix)
    return result

def question_two():
    """
    Compute comparison of two human and fruitfly local alignment sequences and return percentage of matches between both.
    """
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    local_results = question_one()
    pax_seq = read_protein(CONSENSUS_PAX_URL)
    dash, new_human, new_fly = "-", "", ""
    percentages = []

    #remove dashes from human and fruit fly sequences
    for char in local_results[1]:
        if char != dash:
            new_human += char
    print ("Old human seq: " + local_results[1])
    print ("New human seq: " + new_human)
    for char in local_results[2]:
        if char != dash:
            new_fly += char
    print ("Old fly seq: " + local_results[2])
    print ("New fly seq: " + new_fly)

    #compute alignment matrices and calculate global alignments between human, fruit and pax
    print ("Computing alignment matrices and global alignments...")
    align_matrix = prj4.compute_alignment_matrix(new_human, pax_seq, scoring_matrix, True)
    result_human_comp = prj4.compute_global_alignment(new_human, pax_seq, scoring_matrix, align_matrix)
    #print result_human_comp
    align_matrix = prj4.compute_alignment_matrix(new_fly, pax_seq, scoring_matrix, True)
    result_fly_comp = prj4.compute_global_alignment(new_fly, pax_seq, scoring_matrix, align_matrix)
    #print result_fly_comp

    #calculate percantage of matches between human, fruit, and pax
    matches = 0
    for index in range(len(result_human_comp[2])):
        if result_human_comp[1][index] == result_human_comp[2][index]:
            matches += 1
    percentages.append(matches / float(len(result_human_comp[2])))
    matches = 0
    for index in range(len(result_fly_comp[2])):
        if result_fly_comp[1][index] == result_fly_comp[2][index]:
            matches += 1
    percentages.append(matches / float(len(result_fly_comp[2])))

    #return the two percentages in a list
    return percentages


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Generates distribution of local alignment sequences stochastically
    """
    distribution = {}

    #loop through num trials to calculation local alignments of random sequences
    for trial in range(num_trials):
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = "".join(rand_y)
        align_matrix = prj4.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = prj4.compute_local_alignment(seq_x, rand_y, scoring_matrix, align_matrix)
        if score[0] in distribution:
            distribution[score[0]] += 1
        else:
            distribution[score[0]] = 1

    #return unnormalized distribution of scores
    return distribution

def question_fourfive():
    """
    Create bar graph of distribution of random local alignments
    """
    #initial variables for sequences and scoring matrix
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    human_seq = read_protein(HUMAN_EYELESS_URL)
    fly_seq = read_protein(FRUITFLY_EYELESS_URL)
    num_trials = 100
    xvals, yvals = [], []
    total = 0
    previously_calc_score = 875 #local alignment score previously calculated in quesiton one

    #calculate distrubtion
    print ("Creating distribution...")
    distribution = generate_null_distribution(human_seq, fly_seq, scoring_matrix, num_trials)
    for score in distribution:
        xvals.append(score)
        yvals.append(distribution[score] / float(num_trials))
        total += (score * distribution[score])

    #plot results
    print (xvals, yvals)
    p1 = plt.bar(xvals, yvals)
    plt.xlabel("Scores of Local Alignments")
    plt.ylabel("Distribution of scores")
    plt.title("Normal Distr. of Random Sequence Local Alignment Scores")
    plt.show()

    #calculate standard deviation and z score
    mean = total / float(num_trials)
    total = 0
    for score in distribution:
        for value in range(distribution[score]):
            total += (score - mean) ** 2
    variance = total / float(num_trials)
    stddev = math.sqrt(variance)
    z_score = (previously_calc_score - mean) / stddev

    return mean, stddev, z_score

#print (question_one())
#print (question_two())
print (question_fourfive())