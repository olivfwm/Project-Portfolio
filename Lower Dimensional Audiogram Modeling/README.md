# Audiogram Modeling With Speech And Hearing Lab

This contains the individual research I did with the UW Speech Hearing Lab, specifically supervised by Dr. Shen. We aimed to apply ML techniques to achieve more accessible hearing test.

**Background**

An audiogram measures a person's hearing ability by testing their sensitivity to different frequencies (pitches) and intensities (loudness). Frequencies range from 250 Hz to 8000 Hz, and intensities are measured in decibels (dB), indicating the softest sound detectable at each frequency. The test requires specialized equipment, a soundproof room, and a trained professional to conduct the test, which is not something people get done daily, and clearly can't be done at home.

Our idea is that, how can we provide people with more accessible hearing test and decently accurate audiogram, so patients will be aware of their hearing lost. We want to make use of the digit in noise hearing test, which is a test where a person listens to numbers spoken in background noise to assess their ability to recognize speech in noisy environments. Unlike the audiogram, this can be easily calibrated, and doesn't require a professional or professional equipments.

Then we want to ask, in additional to the DIN (digit in noise) score, and other features one can easily input, such as gender and age, what other few features can we put into our model to improve that accuracy?

### Autumn 2024 Focus

Since we have 16 features to predict (the 16 measurements in the audiogram) and only 3-5 predictors (age, gender, din, and depending on how these are inputed), we face a common problem in ML, where the dimension of the variable being predicted is larger than the dimension of the predictor. We naturally went to dimension reduction as our first step, starting with PCA. Since the y variables have moderate correlations with their neighbors, only a small number of principal components could preserve the majority variability.

Our next step was to experiment and find the most appropriate ML models, beginning with linear regression, to predict the audiogram measurements reduced to principal components. The linear regression model was able to achieve a MSE of 14 dB on a 0-110 dB scale.

We begin to see the main questions to answer right now: how to reduce the dimensions of Y, and which machine learning algorithm would most suit the situation here.

Naturally, we experimented with other popular methods to answer these questions. The next step we took was applying cross-decompositional techniques, such as partial least squares regression, to achieve reduction in dimension while not losing important features with small variance.

Currently we are exploring addition of other measurements as predictors to further minimize error and assessing non-linear dimensionality reduction techniques and machine learning models


**Materials**

- data
  - audiogram.csv: raw data
  - **audiogram_cca.csv**: cleaned data used for cca
  - audiogram_clean.csv: cleaned data for exploratory analysis and cv
  - audiogram_interest.csv: raw data containing columns of interest
  - audiogram_x.csv: cleaned data used for pca practice

- Google collab notebooks (order matters)
  - sphsc_exploratory.ipynb: Contains exploratory data analysis on the raw data, including visualizations and preliminary statistical analysis to understand data distributions and relationships. Demonstrates plausibility of dimensional reduction on the audiogram measurements.
  - sphsc_pca.ipynb: Implements PCA for dimensionality reduction on audiogram measurements, detailing the variance explained by the principal components and their implications for the data structure.
  - sphsc_cv.ipynb: Focuses on cross-validation techniques to evaluate the predictive performance and stability of pca applied to the data.
  - sphsc_cca_byhand.ipynb: This notebook manually performs Canonical Correlation Analysis (CCA) with gender, age, DIN as X variables, and audiogram measurements as Y variables. Exploring direct implementation and interpretation of the canonical correlations between sets of variables without using built-in functions.
  - sphsc_cca.ipynb: Automates CCA using sklearn's CCA implementation.


### Winter 2025 Focus (Gap on the research)

Refining the analytical process by cleaning up code, renaming variables for clarity, and thoroughly documenting each file and function. In-code annotations were added to explain variable purposes and complex code operations. Additionally, comments were included to reflect the thought process and observations at each analytical step.

Moving forward, the plan is to leverage the high correlation among audiogram measurements to improve prediction accuracy. We aim to identify which predictions are most accurate and adjust other features based on these reliable predictions. Despite the initial lack of performance improvement with additional predictors, further validation is necessary to ensure the model is accurately learning and representing the underlying relationships.


### Individual Contributions

All work in the notebooks reflects individual contributions, with ideas brainstormed with Dr. Shen. This includes implementing statistical models, coding, and interpreting results.

### Learning Outcomes

- Multivariate Predicting: Techniques like CCA and PCA help in predicting relationships between multiple variables.
- Dimensional Reduction: PCA and manual analysis in notebooks show how to reduce the number of variables while preserving essential information.
- Cross Validation: Evaluate model reliability and performance across different subsets of data.
