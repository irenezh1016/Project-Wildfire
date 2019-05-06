# TDI_Challenge

# Project: Analyzing US wildfire 
## Motivation: 
Wildfire is one of the most destructive disasters that are often caused by human. Averagely, there are more than 100,000 wildfires in the US every year, clearing 4 to 5 million acres of land and causing huge economic loss. However, naturally occurred wildfires play an important role in the ecosystem. This project aims at providing insights on wildfire, its causes and behavior, therefore helps to make useful recommendations to increase public safety, minimize economic damage from future wildfires.
Some empirical work on wildfire modelling has been done in academia and multiple machine learning models on predicting wildfires have been tested and analyzed. This project will focus on transferring academic knowledge into practical use, especially on applying it to the case of United States. The project aims at providing an easy-to-understand web app which can help non-technical background people to learn more about how machine learning models can deepen general public’s understanding on wildfires and reduce future risks.

## Targeted problems: 
1)	Firefighting is expensive.
Analyzing the geographical information on where and when the wildfires occurred could provide useful information to identify high-risk areas that are vulnerable to wildfires, therefore help making better strategies on where fire-fighting forces are located and how to improve respond time to wildfires.
2)	Reasons for many destructive wildfires are not identified.
Reasons for lot of wildfires that burned millions of acres are missing or unidentified. Knowing the reasons for these wildfires could be crucial for future preventive measures on human-caused wildfires. 
This project aims at providing insightful information from analyzing historical data and utilizing appropriate machine learning techniques to solve above problems.

## Finishing product:
A web application that contains: 
1)	Interactive page where users can select a state and view relevant statistical analysis and data visualizations on historical data. 
2)	Prediction of the causes on historically unidentified wildfires.
3)	Useful recommendations on future improvements and potential preventive measures.

## Structure of the project:
### Section I: Preparing Data
This section will focus on preparing data (including merging other necessary weather or geographical data to the main dataset), cleaning data, and generating necessary variables to the following exploratory analysis and data visualization. 
The main dataset for this project is from USDA Forest Service: [link](https://www.fs.usda.gov/rds/archive/Product/RDS-2013-0009.4/)
One caveat is that weather information is missing from the main dataset. Adding weather information could be very useful to analyze and predict wildfire causes. There are multiple sources for daily weather records by location published by NOAA [link](https://www.ncdc.noaa.gov/cdo-web/) and earth observation data published by NASA [link](https://earthdata.nasa.gov/earth-observation-data). Based on the fire date and location information in the main dataset, other information can be matched to each entry of the wildfire in the main dataset. In order to provide a deeper understanding on why wildfires occurred, geographical and weather information will be added based on data availability.

### Section II: Exploratory Analysis and Data Visualization
This section will focus on conducting statistical analysis on historical data to provide insights on when, where, and why wildfires occurred. This section will also identify the most destructive wildfires in the sample period and analysis their reasons, location, burning time, and, other environmental/geographical factors (e.g. weather, temperature, nearby camping sites, residential areas). This will provide a deeper understanding on where the most destructive wildfires are most likely to happen. 
Potential questions to answer:
-	Did most destructive wildfires happen on days with low humidity and high temperature?
-	What factor contributes the most to the burning time of a wildfire? (firefighting resources, fire size, or close to residential areas ??)
-	What kind of environment is most likely to trigger a wildfire? (especially human-caused wildfires)

### Section III: Modeling Wildfires
This section aims at exploring different machine learning techniques to:
-	Classify the causes of historically unclassified wildfires through other available information (weather, date, burning time, and so on).
o	K Nearest Neighbors (kNN)
o	Clustering: K-means, hierarchical clustering
-	Construct algorithms to model the causes and predict probability of wildfires in the US. 
o	Linear regression
o	Logistic regression
o	Decision Tree
o	Random Forest
o	Boosting regression trees (BRT)
o	Support Vector Machines (SVM)
o	And other appropriate techniques.
-	Test models and optimize processes.

### Section IV: Summary and Recommendations
This section will summarize the previous findings and give top 3 recommendations on:
1)	Lessons learnt from the past human-caused wildfires.
2)	What’s the best strategy to allocate firefighting resources for a potential destructive wildfire?
3)	What can be done to minimize risks and potential damage?

In addition, this section will also give limitations of this project and point out areas for future research and improvement.




