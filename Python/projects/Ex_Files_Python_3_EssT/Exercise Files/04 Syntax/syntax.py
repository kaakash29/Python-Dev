#!/usr/bin/python3

# syntax.py by Kumar Aakash

# Some Notes :
# Everything IN Python 3 is an object variable functions and even code
# Every object has an ID and a type and a value
# ID is a unique idetifier that identifies a unique object (cannor change for asingle object)
# Type is the CLASS ofthe object (canno change for teh life)
# Value is teh data contained inside teh object.
# Since every thing is an object their can be function calls even using Varible as objects eg var.xmfnc1()

# mutable objects can change their value immutable objects cannot
# variables in python are immutable obects though they might seem to be changinh values
# actually they do not
# Variables in Python are actually refrences to objects and whenver a new value is assigned to a variable
# the refrence is changed to a diffrent address
# If we reasssign the old value of teh variable again the refrence changes to the old refrence again
# thus python vriables are immutable objects.
# Most duncdatmental types in Python are immutable
# ists dictionaries and other objects are mutable

# simple class definition
class Egg:
    # constructor of a class
    # it is usually a good idea to anme an objct variable as
    # _Varname reminds that this is an object variable.
    # Although we can use these variables directly (outside the class)
    # it is always a good idea to write getters and setters for each
    # class variable (private access)
    def __init__(self, kind="fried "):
        self._kind = kind

    # Function definition of a class
    def Whatkind(self):
        return self._kind + "egg"

# Another moe better way of creating object variables is using
# keyword arguements or hashmaps.

class Egg2:
    def __init__(self, **kwargs):
        self.variables = kwargs
        print(self.variables)

    def getVariable(self, varname):
        return self.variables[varname]

    def setVariables(self, varname, value = None):
        self.variables[varname] = value;

    def describe(self):
        print("We are talking about an egg from a ",self.getVariable('type'),
              "which is ",self.variables['time'], "days old and is ", self.variables['kind'])

class Animal:
    def talk(self):
        print("Animal Talking")
    def walk(self):
        print("Animal Walking")

class Dog(Animal):
    #@Override
    def talk(self):
        print("Dog Talking")
    def walk(self):
        print("Dog Walking")

class Cat(Animal):
    #@Override
    def walk(self):
        super().walk()
        print("Cat is walking")

class Monkey(Animal):
    pass

# Polymorphism is something that Python is exceptionally
# good at.

class Duck:
    def quack(self):
        print("Dicks Quack")

    def walk(self):
        print("Ducks can both walk and swim")

class Hen:
    def quack(self):
        print("hens don't quack")

    def walk(self):
        print("Hens can walk and Fly")

# though by the name it expects a Hen but both of the hen and
# the duck can be supplied without an error to this function
# becoz both are implementing teh same interface and have the same
# fnctions.
def some_func(Hen):
    print("Here expecting a hen")

# Creating Generator Classes:
class inclusive_Range:
    def __init__(self, *args):

        nm = len(*args)
        if nm < 1:
            raise TypeError("Atlest one arguement is required")
        elif nm == 1:
            self.start = 0
            self.end = args[0]
            self.step=1
        elif nm == 2:
            (self.start, self.end) = args
            self.step = 1
        elif nm == 3:
            (self.start, self.end, self.step) = args
        else:
            raise TypeError ("TOo msny atguements")

    def __itr__(self):
        i = self.start
        while(i <= self.end):
            yield i
            i += 1

#-------------------

# main method
def main():

    #Inheritance in Python

    for i in inclusive_range(0, 25, 5):
        print(i)

    inclusive_range()

    inclusive_range(1,2,3,4,5,6)

    bruno = Dog()
    mycat = Cat()

    bruno.walk()
    bruno.talk()

    mycat.walk()
    mycat.talk()

    pukpuk = Hen()
    chapchap = Duck()

    # Runtime Polymorphism only teh implementation of same interface is
    # required to call the same function of any two objects.

    some_func(pukpuk)
    some_func(chapchap)

    smEgg2 = Egg2(kind = 'fried', type='Chicken', time=2)
    smEgg2.describe()
    # Simple assignment
    a, b = 0,1

    # For and while Loops
    while a < b:
        print("In a while ... ")
        a += 1

    # For loop introduces an iterator and can work with containers
    # aggregator
    fh = open("lines.txt")
    for i in fh.readlines():
        print(i)

    # print() adds an extra newline but to prevent that we
    # can use the function end = ''
    # For loops can be used with
    for i in "Somestring":  #strings
        print(i)

    for i in (1, 2, 3, 4, 5):   #tuple
        print(i)

    for i in [1, 2, 3, 4, 5]:   #lists
        print(i)

    # For loops may sometimes need an enumerator or a
    # couter variable to keep track of what is going on
    # this feature is also present in python
    for index, i in enumerate("This is a string"):
        print(index ,i)
        if index == 3: print("@ third index ", i)
        if i == 'a': print("A is found at ", index)

    # Break and Continue in for
    for i in "This is a String":
        if i == 's': continue
        print(i)
        #if i == 'n': break
    else:
        print("Action performaed af ter the loop is \n"
              "done ... only executed if the loop condition fails \n"
              "can be done by commenting out the break above \n")

    # ranges are non inclusive the last item is not included
    for i in range(0, 10): print(i)

    # Divmod Function gives the result of both divison and modulo
    # in the same operation

    # SLICE operations
    print ("Slice Operation")
    l = [1 , 2,  3,  4,  5,  6,  7,  8,  9,  0,
         11, 22, 33, 44, 55, 66, 77, 88, 99, 00,
         111,222,333,444,555,666,777,888,999,000]

    print(l[0:10])  # elements from 0 to 10
    print(l[0:10:3]) # every third elemnts from 0 to 10
    print(l[5:10])  # elements from 5 to 10
    l[1:3] = [99 , 99, 99]
    print (l)

    # Regular Expressions in Python
    import re
    print("====REGEXES====\n")
    rfh = open("raven.txt")
    for line in rfh:
        print(re.sub('len[a-z]{,}', "###", line))

    # Can also be done with
    # note that a new file handle is needed because
    # teh previous one already reached teh EOF

    print("******PART 2******")

    pattern = re.compile('(len|Neverm)ore', re.IGNORECASE)
    rfh2 = open("raven.txt")
    for line1 in rfh2:
        match1 = re.search(pattern, line1)
        if match1:
            print(line1.replace(match1.group(), '###'))
            # or
            print(pattern.sub('###', line), end='')
    print("========")

    # Data Types
    # there are two different types of numbers in Python
    # integers and floats
    x = 34.001
    y = 34 / 5
    z = 34 // 5   # ignores the deciaml part
    z1 = round(34 / 5, 3)  # rounds teh result to given preision
    print("A is a ", type(a), a)
    print("X is a ", type(x), x)
    print("Y is a ", type(y), y)
    print("Z is a ", type(z), z)
    print("Z1 is a ", type(z1), z1)

    # Typecast in Python
    m = int(2.334343) # Constructor for int clasa parameter passed is 2.33
    n = float(23)
    print("m is a ", type(m), m)
    print("n is a ", type(n), n)

    # Strings are one of teh most strong features of Python
    # Both double and simgle quotes strings are allowed
    s = "This is a test string"
    print(s)
    s1 = "This is a string in \n 2 lines"
    print(s1)
    s2 = r"This is a raw string in \n 2 lines"
    print(s2)
    s3 = "This is a string with {} number inseted".format(n)
    print(s3)
    s4 = '''\
    this is another way of
    descripbing a string where we can describe
    a string line after line after
    line it is a really great way of writing'''
    print(s4)

    # Tuples and Lists
    p = {0, 1, 2} # a tuple is immutable cannot append or insert
    print(type(p), p)

    q = [{0,1}, {2,3}, {4, 5}] # a list of tuples
    print(type(q), q)
    q.append(5)
    print("After appending", type(q), q)
    q.insert(2, 10) # inserting 10 at location 2
    print("After inserting", type(q), q)
    # We can see the individual elements of a sequential type by doing
    print("List Element", q[1])

    # string is also a sequential type of data
    str = 'qwerty'
    print(str[1])
    print(str[1:4])  # this is called slicing

    # using the sequential data types as a loop works
    # for tuple and lists too
    for i in str:
        print(i)

    # Another aggregator type is called a DICTIONARY and is pretty similar
    # to HASH in other languages like JAVA and C++
    di = {1:"one" , 2:"two" , 3:"three", 4:"four", 5:"five"}
    print(di)

    # traversing a dictionary
    for k in di:
        print(k , di[k])
    # notice that the print is in no
    # particular order therefor to sort it according to keys
    # we can have the sorted method called on the key object of
    # dict

    # sorting by Keys
    for k in sorted(di.keys()):
        print(k, di[k])

    # sorting by Values
    for k in sorted(di.values()):
        print(k)

    # also support multiple kinds
    d2 = dict(
        one = 1 , two = 2 , three = 3
        )

    d2['six'] = "Six"
    for k in sorted(d2.keys()):
        print(k, d2[k])

    # the "is" operator is used for comparing instances but = is
    # used for comparing values ... if two variales (more like pointers)
    # point to same location they can be compared using x is y
    # they are immutable objects
    # Mutable objects such as list and dict cannot be compared using
    # IS operator.

    # True and False are immutable objects of the Class Bool

    # A conditional statement similar to swith case in Python is not
    # present but that essentially is not a weakness in the language
    # rather it is a different outlook of looking at things

    choices = dict(
        one = "One",
        two = 2,
        three = "three",
        four = 4
    )
    # So now instead of needing a special conruct we can
    # easily select the value based on the key using the
    # dictionary
    print("=====")
    print(choices['one'])
    print(choices['two'])
    print(choices['three'])
    print(choices['four'])

    # However this might lead to an error if something that is not
    # in the dict is searched, to overcome this problem a get method
    # teh dictionary is provided
    # will print Other as Nine is not present in key
    print(choices.get('nine', 'other'))
    print("=====")

    # creating object
    smegg1 = Egg()
    print("Kind Egg1 = {}".format(smegg1.Whatkind()))
    smegg2 = Egg("scrambled")
    print("Kind Egg2 = {}".format(smegg2.Whatkind()))

    # multiple assignment
    a, b = b, a     # Swap is simple
    print("A = {} B = {}".format(a, b))

    # conditional block
    if a < b:
        print("A is less")
    elif a > b:
        print("A is greater")
    else:
        print("Both are equal")

    # conditional expression/value
    s = "a less" if (a < b) else "a not less"
    print(s)
    print("This is the syntax.py file.")

    # Function Calls
    # takes default arguement
    func()
    # overwrites the default arguement
    func(3)
    # Passing 3 values to func with 4 args
    func_none(1, 2, 3)
    # Calling function with unknown number
    # of arguements
    func_ua(1,2,3,4,5,6,7,8,9,0)
    # Functions can also be called using named (key value) pairs
    func_kwa(one=1 , two=2, three=3)

    # Exceptions Handling in Python
    # Try Catch Else
    try:
        nfh = open("xlines.txt")
    except IOError as e:
        print("Exception Occured While Opoening teh File to read")
        print("Error : ", e)
    else:
        for i in nfh.readlines():
            print(i)

    # raising your own exceptions
    try:
        for i in readfile("files.doc"):
            print(i)
    except IOError as ex:
            print("IO Exception Raised", ex)
    except ValueError as err:
            print("Error : ", err)

    # A generator function is any function that returns an iterator object
    # inclusive_range() here returns an iterator object
    for i in inclusive_range(25):
        print(" ", i ,end='')

# ---------------------

# in iterator function similar to range but inclusive
def inclusive_range(*args):
    if len(args) < 1:
        raise TypeError("inclusive_range requires atleast one arguement")
    elif len(args) == 1:
        start = 0
        end = args[0]
        step = 1
    elif len(args) == 2:
        (start, end) = args
        step = 1
    elif len(args) == 3:
        (start, end, step) = args
    else:
        raise TypeError("inclusive range can have maximum of three arguements")

    i = start
    while(i <= end):
        yield i  # returns i but keeps execution inside the function body
        i += step

# functio nreceiving key value pairs essentially dictionaries
# also known as key word arguements
def func_kwa(**kwargs):
    print(kwargs)
    print(kwargs['one'])
    print(kwargs['two'])
    print(kwargs['three'])

# All kinds of arguements can also be mixed barring one small restriction
# teh order should be Number Args -> Tuple Args -> Dict Args

# Function with unknown number of arguements
def func_ua(a1, a2, a3, *args):
    print(a1);
    print(a2);
    print(a3);
    print(*args);

# functions which have x number of args
# can be called with y number of arguements
# if x-y arguements are asssigned to None

def func_none(a1, a2, a3, a4 = None):
    print(a1);
    print(a2);
    print(a3);
    print(a4);

# function which does not have any lines in it
def test_pass():
    pass   # essentially a NO Operation statement
           # makes ur fnction syntactically correct.

# returns the filehandle iterator
def readfile(filename):
    if(filename.endswith(".txt")):
        smfh = open(filename)
        return smfh.readlines()
    else:
        raise ValueError("Filename must end in a txt")

# example for function definition
def func(a = 7):
    print("We are n func")
    for i in range(a, 10):
        print(i)
    print("Leving the func")

# allows us to run the script in any order that we want and
# does not make it manadatory to define a function before use.
# or evn a definitio nf a main function
if __name__ == "__main__": main()
# or
# main() would also have th e same effect the above code is generall
# useful in modules where it specifies which function is going to
# execute for this module
