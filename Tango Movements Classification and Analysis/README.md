# Movements Classification For Statistics Honors Individual Study

This contains the individual research I did with my supervisor, Emanuela Furfaro, to fulfill the requirement of being a part of the statistical honors program.

**Background**

Movement data is collected from three sensors attached to a tango dancer repeating each movement over a fixed time period. We will start with analyzing the move 'ocho'. The analysis phase will be crucial for understanding and quantifying the variability of the dancer's movements.

Building on the insights gained from the data analysis step, classification methods discussed in previous scholar articles will be applied to identify and categorize different dance movements. Hierarchical clustering is also utilized to identify latent patterns or anomalies, in order to improve generalizability of the movement classifying algorithm.

The goal we have now is to be able to classify these dance movements based on the given motion data, and be able to generalize the classification even when the data is collected from different dancers and the movement is done slightly differently from time to time.

### Autumn 2024 Focus

The sensors provided measurements of movements from three perspectives: gyroscope, acceleration, and euler, recorded on all three axes. We started by only looking at the acceleration first, as we believe it gives most information about identifying a dance movement. After carefully examining the features with various visualizations, including interactive ones, we spot unexpected patterns and outliers. This is good news, since we gained clearer understanding about the behaviors of the data, and it helped us to decide on which specific methodologies to perform model training and prediciting.

We believe that it is hard to tell by eyeballing, which data points are actually different from other data points, so we can use hierarchical clustering to cluster the data before continuing to classifying movements. Currently, we found that we may create a huge cluster and some small clusters by directly applying euclidean average linkage clustering. Our next step is to experiment with more techniques to make more sense out of the clustering.

**Materials**

- acc.csv
  - processed dataframe containing 6 columns of acceleration on x, y, z axis, recorded for left and right foot
- tango_acc.ipynb
  - data analysis phase
- tango_clustering.ipynb
  - hierarchical clustering step (in progress)
- observable interactive notebook
  - contains more explorable and flexible visualizations of the movement data
  - https://observablehq.com/d/38532e2bf6f924d5

### Spring 2025 Focus (future)

Continue to work on clustering and movements classification


### Individual Contributions

- Meeting each week to present individual work over the week and brainstorm with supervisor solutions and next step
- Conducted all the data analysis, visualizations, coding individually
- Demonstrate work and give feedbacks to other members of the honors program 

### Learning Outcomes

One of my first individual research experience. At this point, I have already had some prior research experience from WXML, the math research lab. However, it was in a team, and on a different research topic. I felt more challenged and more excited about this opportunity. Though my supervisor gave me guidance and suggestions, I was the main person making decisions during the research. There are both pros and cons working individually, but either way, my knowledge and experience has been further enriched, and I enjoyed navigating challenges with my own way.

