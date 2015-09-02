"""
Module 4 Project:
"""
#-------------------------------------------------------------------------------
# Name:        Rna Sequencing
# Purpose:
#
# Author:      Kumar
#
# Created:     09/08/2015
# Copyright:   (c) Kumar 2015
# Licence:     Common Distribution License
#-------------------------------------------------------------------------------


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Consumes a set of characters and 3 scores and returns a dictionary or
    dictionaries representing a scoring matrix.
    """
    # Creating a copy of alphabets to be used as dictionary indexes
    # and adding dash as another element in the keys

    char_indexes = alphabet.copy();
    char_indexes.add('-')

    # initialize the scring matrix as an empty dictionary
    scoring_matrix = {}

    for char_index in char_indexes:
        # Initialize an empty dictionary for each of the characters

        scoring_matrix[char_index] = {}

        # Assign values to each of teh dictionaries

        for compare_index in char_indexes:

            if compare_index == '-' or char_index == '-':
               # if any of the row or col is a dash assign dash_Score
               score = dash_score

            elif compare_index == char_index:
                 # both the entries of row and col are same lies on diagonal
                 score  = diag_score

            else:
                 score = off_diag_score

            # Add score to the scoring matrix

            scoring_matrix[char_index][compare_index] = score

    return scoring_matrix


#########

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Consumes two sequences and a scoring matrix and
    returns an alignment matrix for the sequences.
    """
    dummy_m = len(seq_x)
    dummy_n = len(seq_y)


    alignment_matrix = [[0 for dummy_col in range(0, dummy_n+1)]
                           for dummy_row in range(0, dummy_m+1)]


    for idx_i in range(1, dummy_m+1):
        alignment_matrix[idx_i][0] = alignment_matrix[idx_i-1][0] + \
                                (scoring_matrix[seq_x[idx_i-1]]['-'])

        if global_flag is False and alignment_matrix[idx_i][0] < 0:
           alignment_matrix[idx_i][0] = 0


    for idx_j in range(1 , dummy_n+1):
        alignment_matrix[0][idx_j] = alignment_matrix[0][idx_j-1] + \
                                    scoring_matrix['-'][seq_y[idx_j - 1]]

        if global_flag is False and alignment_matrix[0][idx_j] < 0:
           alignment_matrix[0][idx_j] = 0

    for idx_i in range(1, dummy_m+1):
        for idx_j in range(1, dummy_n+1):
            alignment_matrix[idx_i][idx_j] = \
            max(
            # max from the iterable
                [
                     # S[iâˆ’1,jâˆ’1] + M [Xiâˆ’1,Yjâˆ’1]
                    (alignment_matrix[idx_i - 1][idx_j - 1] + \
                    scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]),

                    # S[iâˆ’1,j] + M [Xiâˆ’1,âˆ’]
                    (alignment_matrix[idx_i - 1][idx_j] + \
                    scoring_matrix[seq_x[idx_i - 1]]['-']),

                    # S[i,jâˆ’1] + M [âˆ’,Yjâˆ’1]
                    (alignment_matrix[idx_i][idx_j - 1] + \
                    scoring_matrix['-'][seq_y[idx_j - 1]])
                ]
            )
            if global_flag is False and alignment_matrix[idx_i][idx_j] < 0:
               alignment_matrix[idx_i][idx_j] = 0

    return alignment_matrix

########

# Compute Alignment

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Consumes two sequences and scoring and alignment mtrices and
    computes teh best alignment for the two sequences
    """
    #finding max in alignment matrix


    idx_i = len(seq_x)
    idx_j = len(seq_y)

    print (seq_x, idx_i)
    print (seq_y, idx_j)

    max_value = alignment_matrix[idx_i][idx_j]


    x_prime = ''
    y_prime = ''

    while idx_i != 0 and idx_j != 0:

          if alignment_matrix[idx_i][idx_j] ==                       \
                                                             \
             (alignment_matrix[idx_i - 1][idx_j - 1]                 \
                                    +                        \
             scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]):

             x_prime = seq_x[idx_i - 1] + x_prime
             y_prime = seq_y[idx_j - 1] + y_prime
             idx_i -= 1
             idx_j -= 1

          else:

               if alignment_matrix[idx_i][idx_j] ==              \
                                                         \
                  (alignment_matrix[idx_i - 1][idx_j]            \
                                      +                  \
                  scoring_matrix[seq_x[idx_i - 1]]['-']):

                  x_prime = seq_x[idx_i - 1] + x_prime
                  y_prime = '-' + y_prime
                  idx_i -= 1

               else:

                    x_prime = '-' + x_prime
                    y_prime = seq_y[idx_j - 1] + y_prime
                    idx_j -= 1


    while idx_i != 0:

          x_prime = seq_x[idx_i - 1] + x_prime
          y_prime = '-' + y_prime
          idx_i = idx_i - 1

    while idx_j != 0:

          x_prime = '-' + x_prime
          y_prime = seq_y[idx_j - 1] + y_prime
          idx_j = idx_j - 1

    return (max_value, x_prime, y_prime)

###########


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Consumes 2 sequences and scoring and alignment matrices generates a
    optimal local alignment
    """
    max_x = 0
    max_y = 0
    max_value = 0
    for index_x in range(len(alignment_matrix)):
        for index_y in range(len(alignment_matrix[0])):
            if alignment_matrix[index_x][index_y] > max_value:
                max_x = index_x
                max_y = index_y
                max_value = alignment_matrix[index_x][index_y]

    idx_i = max_x
    idx_j = max_y

    x_prime = ''
    y_prime = ''

    while idx_i != 0 and idx_j != 0:

          if alignment_matrix[idx_i][idx_j] == 0:
            return (max_value, x_prime, y_prime)

          if alignment_matrix[idx_i][idx_j] ==                       \
                                                             \
             (alignment_matrix[idx_i - 1][idx_j - 1]                 \
                                    +                        \
             scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]):

             x_prime = seq_x[idx_i - 1] + x_prime
             y_prime = seq_y[idx_j - 1] + y_prime
             idx_i -= 1
             idx_j -= 1

          else:

               if alignment_matrix[idx_i][idx_j] ==              \
                                                         \
                  (alignment_matrix[idx_i - 1][idx_j]            \
                                      +                  \
                  scoring_matrix[seq_x[idx_i - 1]]['-']):

                  x_prime = seq_x[idx_i - 1] + x_prime
                  y_prime = '-' + y_prime
                  idx_i -= 1

               else:

                    x_prime = '-' + x_prime
                    y_prime = seq_y[idx_j - 1] + y_prime
                    idx_j -= 1


    while idx_i != 0:

          x_prime = seq_x[idx_i - 1] + x_prime
          y_prime = '-' + y_prime
          idx_i = idx_i - 1

    while idx_j != 0:

          x_prime = '-' + x_prime
          y_prime = seq_y[idx_j - 1] + y_prime
          idx_j = idx_j - 1

    return (max_value, x_prime, y_prime)


### Test
##
##print (build_scoring_matrix(set(['A','T','U','G']), 10, 4, -2))
##
### Expects :
##
### {'T': {'T': 10, '-': -2, 'A': 4, 'U': 4, 'G': 4}, '-': {'T': -2, '-': -2, 'A': -2, 'U': -2, 'G': -2}, 'A': {'T': 4, '-': -2, 'A': 10, 'U': 4, 'G': 4}, 'U': {'T': 4, '-': -2, 'A': 4, 'U': 10, 'G': 4}, 'G': {'T': 4, '-': -2, 'A': 4, 'U': 4, 'G': 10}}
##print (compute_alignment_matrix("ATUG", "GUAT", \
##    (build_scoring_matrix(set(['A','T','U','G']), 10, 4, -2)), True))
##
##
##print (compute_alignment_matrix('', '',
##
##  {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
##
##   'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
##
##   '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
##
##   'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
##
##   'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True))
##
##print (compute_alignment_matrix('A', 'A',
##
##      {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
##       'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
##       '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
##       'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
##       'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True))
##
##
##print(compute_alignment_matrix('ACTACT', 'AGCTA',
## {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
##  'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
##  '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
##  'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
##  'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}, True))
##
##print(compute_alignment_matrix('A', 'A',
##  {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
##   'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
##   '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
##   'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
##   'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, False))

##print (compute_global_alignment('ACTACT', 'AGCTA', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1}, 'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1}, '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0}, 'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1}, 'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}, [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]]))
##
##print (compute_global_alignment('racecar', 'longracecartrack',
##{'-': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'a': {'-': -1, 'a': 2, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'c': {'-': -1, 'a': -1, 'c': 2, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'b': {'-': -1, 'a': -1, 'c': -1, 'b': 2, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'e': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': 2, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'd': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': 2, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'g': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': 2, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'f': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': 2, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'i': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': 2, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'h': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': 2, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'k': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': 2, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'j': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': 2, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'm': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': 2, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'l': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': 2, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'o': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': 2, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'n': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': 2, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'q': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': 2, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'p': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': 2, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 's': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': 2, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'r': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': 2, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'u': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': 2, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 't': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': 2, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'w': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': 2, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
## 'v': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': 2, 'y': -1, 'x': -1, 'z': -1},
## 'y': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': 2, 'x': -1, 'z': -1},
## 'x': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': 2, 'z': -1},
## 'z': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': 2}},
##
##  [[0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16],
##   [-1, -1, -2, -3, -4, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13],
##   [-2, -2, -2, -3, -4, -3, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10],
##   [-3, -3, -3, -3, -4, -4, -1, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7],
##   [-4, -4, -4, -4, -4, -5, -2, 1, 4, 3, 2, 1, 0, -1, -2, -3, -4],
##   [-5, -5, -5, -5, -5, -5, -3, 0, 3, 6, 5, 4, 3, 2, 1, 0, -1],
##   [-6, -6, -6, -6, -6, -6, -3, -1, 2, 5, 8, 7, 6, 5, 4, 3, 2],
##   [-7, -7, -7, -7, -7, -4, -4, -2, 1, 4, 7, 10, 9, 8, 7, 6, 5]]))


