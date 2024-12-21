## Files and their contents

*Note*: These are not the only files to achieve the expected outcomes

- solver_utils.py
  - contains key functions for implementing reinforcement learning algorithms
    - Value Iteration Function: iteratively updates the value table to find optimal policies
    - Extract Policy Function: extracts the optimal policy from a given Q-value table
    - Q-Update Function: performs a single update to the Q-value table based on a transition observed from the environment, which includes the current state, action taken, reward received, and the new state
    - Extract Value Table from Q-Value Table: derives a value table from the Q-value table by extracting the maximum Q-value for each state
