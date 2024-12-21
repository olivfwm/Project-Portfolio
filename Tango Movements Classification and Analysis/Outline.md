# Statistics Honors Individual Study

This contains the individual research I did with my supervisor, Emanuela Furfaro, to fulfill the requirement of being a part of the statistical honors program.

**Background**

I will analyze data collected from three sensors attached to a tango dancer. This phase will be crucial for understanding and quantifying the variability of the dancer's movements, even when the same movements are repeated.

Building on the insights gained from the data analysis step, I will apply and perhaps refine the classification methods discussed in previous scholar articles to effectively identify and categorize different dance movements. Hierarchical clustering is also utilized to identify latent patterns or anomalies, in order to improve generalizability of the movement classifying algorithm.

### Autumn 2024 Focus

The sensors provided measurements of movements from three perspectives: gyroscope, acceleration, and euler, recorded on all three axes. We started by only looking at the acceleration first, as we believe it gives most information about identifying a dance movement. After carefully examining the features with various visualizations, including interactive ones, we gained clearer understanding about the behaviors of the data, which helped us to decide specific methodologies to perform model training and prediciting.

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

