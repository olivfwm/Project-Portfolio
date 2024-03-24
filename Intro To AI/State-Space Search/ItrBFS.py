#!/usr/bin/python3
""" ItrBFS.py
Student Names: Olivia Fang
UW NetIDs: olivfwm
CSE 415, Winter, 2024, University of Washington

This code contains my implementation of the Iterative BFS algorithm.

Usage:
 python ItrBFS.py HumansRobotsFerry
"""

import sys
import importlib


class ItrBFS:
    """
    Class that implements Iterative BFS for any problem space (provided in the required format)
    """

    def __init__(self, problem):
        """ Initializing the ItrBFS class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded
        self.MAX_OPEN_LENGTH = None  # Maximum length of the open list
        self.PATH = None  # Solution path
        self.PATH_LENGTH = None  # Length of the solution path
        self.BACKLINKS = None  # Predecessor links, used to recover the path
        print("\nWelcome to ItrBFS")

    def runBFS(self):
        """This is an encapsulation of some setup before running
        BFS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.IterativeBFS(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

    def IterativeBFS(self, initial_state):
        # Comment out the line below when this function is implemented.
        # raise NotImplementedError

        # STEP 1. Put the start state on a list OPEN
        OPEN = [initial_state]
        CLOSED = []
        self.BACKLINKS[initial_state] = None

        # STEP 2. If OPEN is empty, output “DONE” and stop.
        # hidden to protect information
        
def print_state_list(lst_name, lst):
    """
    Prints the states in lst with name lst_name
    """
    print(f"{lst_name} is now: ", end='')
    # hidden to protect information


def report(opn, closed, count):
    """
    Reports the current statistics:
    Length of open list
    Length of closed list
    Number of states expanded
    """
    print(f"len(OPEN)= {len(opn)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")

if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "TowersOfHanoi"
    else:
        Problem = sys.argv[1]
    BFS = ItrBFS(Problem)
    BFS.runBFS()
