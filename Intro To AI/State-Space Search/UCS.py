""" UCS.py

Uniform Cost Search of a problem space.
 Steve Tanimoto, Univ. of Washington.
 Refactored to support autograding by Prashant Rangarajan.
 Paul G. Allen School of Computer Science and Engineering
 April 6, 2021.

 Usage:
 python3 UCS.py FranceWithCosts
This implementation does not reconsider a state once it has
been put on CLOSED list.  If this implementation is extended
to implement A*, and it is to work will all heuristics,
including non-admissible ones, then when a state is regenerated
that was already put on the CLOSED list, it may need reconsideration
if the new priority value is lower than the old one.

Most of the print statements have been commented out, but can be
useful for a closer look at execution, or if preparing some
debugging infrastructure before adding extensions, such as for A*.

"""

import sys
import importlib
from PriorityQueue import My_Priority_Queue


class UniformCostSearch:
    """
    Class that implements Uniform-Cost Search for any problem space (provided in the required format)
    """
    def __init__(self, problem):
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded.
        self.MAX_OPEN_LENGTH = None  # How long OPEN ever gets.
        self.PATH = None  # List of states from initial to goal, along lowest-cost path.
        self.PATH_LENGTH = None  # Number of states from initial to goal, along lowest-cost path.
        self.TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
        self.BACKLINKS = {}  # Predecessor links, used to recover the path.
        self.OPEN = None  # OPEN list
        self.CLOSED = None  # CLOSED list
        self.VERBOSE = True  # Set to True to see progress; but it slows the search.

        # The value g(s) represents the cost along the best path found so far
        # from the initial state to state s.
        self.g = {}  # We will use a hash table to associate g values with states.

        print("\nWelcome to UCS.")

    def runUCS(self):
        """This is an encapsulation of some setup before running
        UCS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.UCS(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

        # print("The CLOSED list is: ", ''.join([str(s)+' ' for s in CLOSED]))

    def UCS(self, initial_state):
        """Uniform Cost Search: This is the actual algorithm."""
        self.CLOSED = []
        self.BACKLINKS[initial_state] = None
        # The "Step" comments below help relate UCS's implementation to
        # those of Depth-First Search and Breadth-First Search.

        # STEP 1a. Put the start state on a priority queue called OPEN
        self.OPEN = My_Priority_Queue()
        self.OPEN.insert(initial_state, 0)
        # STEP 1b. Assign g=0 to the start state.
        self.g[initial_state] = 0.0

        # STEP 2. If OPEN is empty, output “DONE” and stop.
        # hidden to protect information
 
    def backtrace(self, S):
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path


def print_state_queue(name, q):
    """
    Prints the states in queue q
    """
    print(f"{name} is now: ", end='')
    print(str(q))


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
        Problem = "FranceWithCosts"
    else:
        Problem = sys.argv[1]
    UCS = UniformCostSearch(Problem)
    UCS.runUCS()
    print(UCS.PATH)
