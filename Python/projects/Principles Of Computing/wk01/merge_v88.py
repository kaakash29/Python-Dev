"""
Merge function for 2048 game.
"""

def slid_nz_front(line):
    """
    Consumes a line and slides all the non-zero
    elements of teh line infront and returns a 
    list
    """
    newline = [0 for elm in range(len(line))]
    
    index = 0
    for elm in range(0, len(line)):
        if(line[elm] != 0):
            newline[index] = line[elm]
            index += 1
    
    return newline    	
    
def merge_two(line):
    """
    Merges teh two consecutive elements of a 
    list and replaces them by double and 0
    """
    nuline = line
    for elm in range (0, len(line) - 1, 1):
        if line[elm] == line[elm + 1]:
            nuline[elm] = 2* line[elm]
            nuline[elm + 1] = 0
        else:
            nuline[elm] = line[elm]
            nuline[elm+1] = line[elm + 1]
            
    return nuline
           
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    list1 = slid_nz_front(line)
    # list after sliding
    list2 = merge_two(list1)
    # list after merging
    list3 = slid_nz_front(list2)
    # list after sliding again
    
    return list3

print "1",merge([2, 0, 2, 4])
print "2",merge([0, 0, 2, 2])
print "3",merge([2, 2, 0, 0])
print "4",merge([2, 2, 2, 2, 2])
print "5",merge([8, 16, 16, 8])
