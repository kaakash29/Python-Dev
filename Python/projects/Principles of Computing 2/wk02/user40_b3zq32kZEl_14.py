"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(100)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(working_list):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result_list = []
    for idx in range(len(working_list)):
        if not working_list[idx] in result_list:
            result_list.append(working_list[idx])
        else:
            pass

    return result_list  # shud return a 
                        # sorted list here 
                        # call 2 merge sort required

######
# test
######
#print remove_duplicates([1,5,2,2,4,5,5,6,7,8,9,5,5,4,1,0])


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result_list = []
    for elem in list1:
        if elem in list2:
            result_list.append(elem)
        
    return result_list

######
# test
######
#print intersect([1,5,2,2,4,5,5,6,7,8,9,5,5,4,1,0], 
#                [1,5,2,4,6,7,8,9,0,10])

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    
    index_i = 0 
    index_j = 0 
    result_list = []
    
    while index_i < len(list1) and index_j < len(list2):
        if list1[index_i] < list2[index_j]:
            result_list.append(list1[index_i])
            index_i += 1
        else:
            result_list.append(list2[index_j])
            index_j += 1
        
    # time for cleaning up whatever was left
    
    if index_i < len(list1):
        result_list += list1[index_i: len(list1)]
    
    if index_j < len(list2):
        result_list += list2[index_j: len(list2)]
        
    return result_list
    
    
######
# test
###### 
#print merge([-1, 3, 4], [0, 1, 2])


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    wlist = [elm for elm in list1]
    
    if len(wlist) < 2:
        return wlist
    else:
        mid = len(wlist)/2
        left_list = wlist[0 : mid]
        right_list = wlist[mid : len(wlist)]

        return merge(merge_sort(left_list), merge_sort(right_list))

######
# test
######
#print merge_sort([-1, -3, 0,0, 2, 0])


def insert_at_all_pos(aword, charc):
    """
    Consumes a word and a character 
    inserts the character at each location of 
    the word and returns the list of resulting words
    """
    result_list = []
    for pos in range(len(aword) + 1):
        new_word = aword[:pos]+charc+aword[pos:]
        result_list.append(new_word)
    
    return result_list
        
print insert_at_all_pos("DY","A")

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    working_word = str(word)
       
    if not word:
        return ['']
    else:
        rest = working_word[1:]              
        combination_list = gen_all_strings(rest)
        
        return_list = [] 
        for aword in combination_list:
            low = insert_at_all_pos(aword, working_word[0])
            return_list += low
        
    return gen_all_strings(rest) + return_list

#######
# Tests 
#######
#dummy_var = "DAY"
#dummy_lis = gen_all_strings(dummy_var)
#print dummy_lis
#print "Number of combinations generated = ", len(dummy_lis)


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    #data = netfile.read()
    result = []
    for line in netfile.readlines():
        result.append(line[:-1])
        
    return result


def run():
    """
    Run game.
    """
    
    words = load_words(WORDFILE)
       
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
