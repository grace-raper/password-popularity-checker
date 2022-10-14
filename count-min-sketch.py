# Count-Min Sketch Project - CSE 312

# Instructor    : Alex Tsun
# Group Members : James Swartwood, Grace Raper, Long Thành
# UW Emails     : jamesms@uw.edu, graper@uw.edu, long1104@uw.edu

""" Import necessary package(s) """
import numpy as np
import mmh3

""" Unimportant startup sequence """
def startup():
    """
    :return: Integer to represent the mode selected.

    Prints information about this project and asks the
    user what mode they would like to select to run the
    program.
    """
    print("<System> Welcome to a Count-Min Sketch program. Printing relevant data...")
    print("")
    print("Count-Min Sketch Project - CSE 312")
    print("Instructor: Alex Tsun")
    print("Group: James Swartwood, Grace Raper, Long Thành")
    print("")
    print("<System> What mode would you like to run? (1:manual, 2:automatic)")
    while True:
        mode = input(f"<User Input> ")
        try:
            mode = int(mode)
            if mode == 1 or mode == 2:
                break
            else:
                print("<System> That is not a valid option. Please try again. Valid options: {1,2}")
        except ValueError:
            print("<System> Only integers are accepted. Please try again. Valid options: {1,2}")
    print("<System> Mode selected. Starting program...")
    print("")
    return mode

""" Creates Count-Min Sketch Class """
class CountMinSketch:
    def __init__(self, size:int = 1000, number:int = 10):
        """
        :param size: Size of the hash functions (length of each row).
        :param number: The number of hash functions (rows).

        Initializes the hash functions to all zeros as a two
        dimensional array that keeps track of integer counts.
        """
        self.size = size
        self.number = number
        self.counts = np.zeros((size, number), dtype=int)

    def hash(self, x, i:int) -> int:
        """
        :param x: The element x to be hashed.
        :param i: Which hash function to use, for i=0,...,self.k-1.
        :return: h_i(x) the ith hash function applied to x.
        
        We take the hash value and mod it by our table size.
        This hash "theoretically" should give a uniform random
        integer from 0 to self.m - 1.
        """
        return mmh3.hash(str(x), i) % self.size

    def add(self, data, quantity:int = 1):
        """
        :param data: The data being added to the counts.
        :param quantity: The quantity of the data.

        Adds data to the count-min sketch.
        """
        for i in range(self.number):
            self.counts[self.hash(data,i)][i] += quantity

    def getCount(self, data):
        """
        :param data: The element to check the count of.
        :return: Integer value that represents the lowest value
        associated with the data stored in the count-min sketch.

        Checks the count of the data in question. This is an
        estimate that will either be the true count or higher,
        due to hashing collisions.
        """
        min = 100**100
        for i in range(self.number):
            count = self.counts[self.hash(data,i)][i]
            if count < min:
                min = count
        return min

if __name__ == '__main__':
    # Starts the program and asks the user what mode they would like to run.
    mode = startup()

    # Create a new count-min sketch structure.
    cms = CountMinSketch(size=1000, number=10) # 10 hash functions of size 100

    if mode == 2: # If the automatic mode is selected
        print("<System> From what text file would you like to load the data?")
        filename = input("<User Input> Filename: ")
        print("<System> Adding items...")
        data = np.genfromtxt(filename, dtype='str')
        for item in data:
            cms.add(item)
            assert cms.getCount(item) > 0 # After adding the item, at least one should be stored in the counts
    
    print("<INFO> Valid commands: help, add, count, exit")
    while True:
        command = input("Command: ") # Takes user input to get a command
        if command == "add":
            data = input("Data: ")
            cms.add(data)
            print("<INFO> Added data.")
        elif command == "count":
            data = input("Data: ")
            n = cms.getCount(data)
            print(f"<INFO> Count of data: {n}")
        elif command == "exit":
            break
        elif command == "help":
            print("<INFO> Valid commands: help, add, count, exit")
        else: # When any other command is entered
            print("<INFO> That is not a valid command. Use the help command for a list.")

    print("")
    print("<System> Stopping program...")
    print("<System> Thank you!")

# End of code

"""
From PSet 3 (checking false positive rate of BF):
    print("Computing False Positive Rate (FPR) on 10000 Unseen URLs")
    # Check contains on 10000 different URLs to see what percentage
    # incorrectly are marked as being contained.
    fpr = 0
    test_urls = np.genfromtxt('/home/data/test_urls.txt', dtype='str')
    for test_url in test_urls:
        if bf.contains(test_url): # Should ideally return False
            fpr += 1
    fpr /= len(test_urls)
    print("FPR: {}".format(fpr))
"""
