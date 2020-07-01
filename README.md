# Fico-Challenge
Explainable Machine Learning Challenge

This is the second place winning submission for the FICO Explainable Machine Learning Challenge created by Oscar Gomez and Steffen Holter. By combining instance level explanations and a general global model interpretation we have created an interactive application to visualize the logic behind each of the model’s decisions.

### Individual Explanation
The local explanation visualizes each individual sample by showing the comparative values of each feature and their relative density distribution across the data set. Each explanation highlights the key features that the model used to make the decision. In addition, where applicable the solution suggests the necessary changes needed to reverse the decision. 

### Global Explanation
The global explanation acts as a way to aggregate the individual results across the whole data set. By either choosing to examine the key features or the necessary changes, the interactive hierarchy creates a comprehensive overview. Each click reveals an additional level of depth within the solution revealing more information.

<br/>

#### Results Announcement
https://www.fico.com/en/newsroom/fico-announces-winners-of-inaugural-xml-challenge

#### Available Online at
http://oscargomezq.pythonanywhere.com/intro
<br/>
http://nyuvis-web.poly.edu/projects/fico/intro

#### To run locally
* Install python 3.6 or above
* Pip install pandas, flask, numpy, scipy, sklearn
* Open Webapp folder
* Run hello.py
* Open in localhost:5005

#### Suggested Specifications
* Open on Mac or PC
* Latest version of Google Chrome
* Screen size of at least 13 inches

Contact us at sh3628@nyu.edu or oag229@nyu.edu for any questions regarding the tool
