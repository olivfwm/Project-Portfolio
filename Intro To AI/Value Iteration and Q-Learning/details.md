This assignment was one of the assignments done in the Intro to AI course I took at UW.

It not only offers an opportunity to implement the Value Iteration algorithm, but also an opportunity to see how reinforcement learning techniques can be applied to problem solving of the sort we studied earlier with state-space search.

The interactions between a problem-solving agent and its problem-domain environment are modeled probabilistically using the technique of Markov Decision Processes. Within this framework, 
the assignment focuses on two approaches to having the agent maximize its expected utility: (A) by a form of planning, in which we assume that the parameters of the MDP (especially the transition model 
T and the reward function R are known, 
which takes the form of Value Iteration, and (B) by an important form of reinforcement learning, called Q-learning, in which we assume that the agent does not know the MDP parameters.

The particular MDPs we are working with in this assignment are variations of a “TOH World”, meaning Towers-of-Hanoi World. We can think of an agent as trying to solve a TOH puzzle instance by wandering around in the state space that corresponds to that puzzle instance. If it solves the puzzle, it will get a big reward. Otherwise, it might get nothing, or perhaps a negative reward for wasting time. 

All search files shows the partial code implemented.
