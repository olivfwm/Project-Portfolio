# Data Science Events and Competitions
This folder contains work particularly for the data science events I participated in.

## Datafest 2024 by ASA at UW
Link to data and notebook: https://drive.google.com/drive/folders/1d0SRBWL9ZlpgCDOEFQDVu_dZ6Do-ylCU?usp=sharing

Background

We were provided a few raw datasets from CourseKata, a statistical learning platform, with the performance of the students using this platform. The data included student's self ratings on various aspects, time spent on the pages across different chapters and books, retry attempts, time the student did not interact with the platform, and the EOC, which is some score the student gets after completing the checkpoints.

Our goal was to analyze the student behaviors and provide insights and recommendations to CourseKata, which aims to improve their understandings of how to help students maximize their potential.

Materials
- Team report and presentation
- Unsupervised learning notebook by me

Individual Constributions
- Data processing across several dataset such as page_views, EOC, pulse_ratings
- K-means clustering on the data to find hidden patterns of student performance measured by EOC
    - cluster students into 4 main clusters and looked at the spread of their data for some selected columns, such as number of retry attempts, engagement time, off-page duration, etc. These columns were determined according to their correlation with EOC score
- Focused on both all book chapters, as well as specific hard chapters, that were determined by visualizations from my team mates
- Provided recommendations supported by my clustering result

Outcome
- Best Visualization Award for informative data visualizations that provided supported our recommendations made to CourseKata

## 5th DubsTech Datathon

Link to event webpage: https://doc.clickup.com/26455927/p/h/t7bvq-3331/ff33c7b7c866f02/t7bvq-3331

Background

We were given the choices to perform data analysis, data visualization, or machine learning on the given data. The data we were provided with focused on three different aspects:

- Retail: Accelerating the Sales of Urban Edge Apparel
- Government: Analyzing and Predicting Inbound Crossings for the U.S.-Canada and the U.S.-Mexico border
- Health: Drug Overdose in USA

My team chose to work on all of data analysis, data visualization, and machine learning, as we believe this is really one whole process. The topic we chose to analyze was Drug Overdose, as we believe this is a serious issue in the US, and any contributions to the field with our statistics knowledge can be meaningful.

I was particularly interested in machine learning, as it is a great aspect of my current area of study, so we split the work, and my work specifically was on using machine learning models to estimate the deaths caused by drug overdose, across different time periods, demographies, ages, etc.

Materials
- Report of my team's combined work
- Work notebook on random forest modeling by me

Individual Contribution
- Careful data carpentry such as dropping unnecessary columns, converting categorical variables originially encoded ordinally, but really should have been nominal
- Using the one-hot encoded data to fit random forest models
- Performed grid search for best hyperparameters
- Compare results of train/test data across different models
- Use the best model to predict the rows that had missing estimate of deaths
- Examined the predicted estimates with the rest of the dataset through visualizations

Outcome
- 4th Place in Best Machine Learning Model Out of 19 Teams

