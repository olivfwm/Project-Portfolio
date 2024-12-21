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

(below is still being updated)

**Materials**

- data
  - 

### Winter 2025 Focus (ip)

Continue to work on clustering and movements classification


### Individual Contributions

- 
### Learning Outcomes


