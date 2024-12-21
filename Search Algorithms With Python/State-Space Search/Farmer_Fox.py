'''Farmer_Fox.py
by Olivia Fang

Assignment 2, in CSE 415, Winter 2024
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name(s), uwnetid(s), and 7-digit student number(s) are given above in 
# the format shown.

# You should model your code closely after the given example problem
# formulation in HumansRobotsFerry.py

# Put your metadata here, in the same format as in HumansRobotsFerry.

#<METADATA>
SOLUTION_VERSION = "2.0"
PROBLEM_NAME = "Farmer, Fox, Chicken and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "06-APR-2021"
#<METADATA>

# Start your Common Code section here.

LEFT=0 
RIGHT=1
ITEMS=["chicken", "grain", "fox"]
NO=[["fox", "chicken"],["chicken", "grain"],["chicken", "fox"],
    ["grain", "chicken"],["fox", "chicken", "grain"],["fox", "grain", "chicken"],
    ["chicken", "fox", "grain"],["chicken", "grain", "fox"],
    ["grain", "fox", "chicken"],["grain", "chicken", "fox"]]

class State():

  def __init__(self, d=None):
    if d==None: 
      d = {'bank':[[],[]],
           'farmer':LEFT,
           'prev': ''}
    self.d = d

  def __eq__(self,s2):
    if self.d['farmer'] != s2.d['farmer']: return False
    if sorted(self.d['bank'][0]) != sorted(s2.d['bank'][0]):
      return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    p = self.d['bank']
    txt = "\n Left bank:"+str(p[LEFT])+"\n"
    txt += " Right bank:"+str(p[RIGHT])+"\n"
    side='left'
    if self.d['farmer']==1: side='right'
    txt += " farmer is on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    # hidden to protect information 

  def can_move(self, item):
    side = self.d['farmer'] 
    p = self.d['bank']
    if item not in ITEMS: return False #has to be a valid item
    item_avail = p[side]
    # hidden to protect information
    
  def move(self,item):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the ferry carrying
     h humans and r robots.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['farmer']        # where is the farmer?
    # hidden to protect information

  def can_moveAlone(self):
    side = self.d['farmer'] 
    p = self.d['bank']
    # hidden to protect information
    
  def moveAlone(self):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the ferry carrying
     h humans and r robots.'''
    news = self.copy()      # start with a deep copy.
    # hidden to protect information

def goal_test(s):
  '''If all items are on the right, then s is a goal state.'''
  p = s.d['bank']
  side = s.d['farmer']
  # hidden to protect information

def goal_message(s):
  return "Congratulations on successfully carrying all items across the river!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

# Put your INITIAL STATE section here.
CREATE_INITIAL_STATE = lambda : State(d={'bank':[["fox", "chicken", "grain"], []],
                                         'farmer':LEFT, 'prev': '' })
# Put your OPERATORS section here.

#<OPERATORS>

OPERATORS = [(Operator(
  "Cross the river with " + item,
  lambda s, item1=item: s.can_move(item1),
  lambda s, item1=item: s.move(item1) ))
  for item in ITEMS]
OPERATORS.insert(0, Operator(
  "Cross the river alone",
  lambda s: s.can_moveAlone(),
  lambda s: s.moveAlone() ))
#<OPERATORS>


# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.
GOAL_TEST = lambda s: goal_test(s)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
