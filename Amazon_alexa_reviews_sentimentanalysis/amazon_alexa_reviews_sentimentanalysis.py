# -*- coding: utf-8 -*-
"""Amazon_Alexa_Reviews_SentimentAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yEUgQJiflEkEaU2ZYNiXtvQOmUSzH1bW

The sentiment analysis has to be performed for a Amazon product that is Alexa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import re

# Load data
data= pd.read_csv('/content/amazon_alexa.tsv',delimiter = '\t', quoting = 3, encoding ='ISO-8859-1')

data.shape

data.head()

#Column names
print(f"Column names : {data.columns.values}")

data= data.rename(columns={'ï»¿rating': 'Rating'})

#Column names
print(f"Column names : {data.columns.values}")

data.isnull().sum()

#Getting the record where 'verified_reviews' is null

data[data['verified_reviews'].isna() == True]

# dropping the column as it has no review written in body
data.dropna(inplace=True)

data.isnull().sum()

data.shape

data.head()

data['Rating'].value_counts()

data['feedback'].value_counts()

#Extracting the 'verified_reviews' value for one record with feedback = 0

review_0 = data[data['feedback'] == 0].iloc[1]['verified_reviews']
print(review_0)

#Extracting the 'verified_reviews' value for one record with feedback = 1

review_1 = data[data['feedback'] == 1].iloc[1]['verified_reviews']
print(review_1)

"""The above analysis suggest that if:
 feedback--> 0 : It is negative review
 feedback-->1: It is positive review

Now we will see the corresponding rating to these positive and negative feedbacks
"""

#Feedback = 0
data[data['feedback'] == 0]['Rating'].value_counts()

#Feedback = 1
data[data['feedback'] == 1]['Rating'].value_counts()

"""Now there a field for neutral revirew is missing so we create a new column in which:
If the rating is 1 or 2, assign -1 as the feedback value.
If the rating is 3, assign 0 as the feedback value.
If the rating is 4 or 5, assign 1 as the feedback value.
"""

def map_feedback(Rating):
    if Rating in [1, 2]:
        return -1
    elif Rating == 3:
        return 0
    elif Rating in [4, 5]:
        return 1

# Apply the function to create a new column 'new_feedback' based on 'rating'
data['new_feedback'] = data['Rating'].apply(map_feedback)

print(data)

data[data['new_feedback'] == 1]['Rating'].value_counts()

data[data['new_feedback'] == 0]['Rating'].value_counts()

data[data['new_feedback'] == -1]['Rating'].value_counts()

data.head()

"""Preprocessing
Stemming: The process of reducing a word to its root word
eg. act is root word for actor, acting.
"""

port_stem = PorterStemmer()

def stemming(content):
  stemmed_content= re.sub('[^a-zA-Z]',' ',content)
  stemmed_content= stemmed_content.lower()
  stemmed_content= stemmed_content.split()
  stemmed_content= [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content = ' '.join(stemmed_content)

  return stemmed_content

data['stemmed_content']= data['verified_reviews'].apply(stemming)

data.head()

data['stemmed_content']

data['new_feedback']

data.head()

# dropping the feedback column since we have created a new_feedback column
data.drop(columns=['feedback'], inplace=True)

"""Before goining towards training and model selection, we plot the dataset to see the new_feedback column insights"""

#Bar graph to visualize the total counts of each feedback

data['new_feedback'].value_counts().plot.bar(color = 'blue')
plt.title('Feedback distribution count')
plt.xlabel('Feedback')
plt.ylabel('Count')
plt.show()

#seperating the data and label

X= data['stemmed_content'].values
Y= data['new_feedback'].values

print(X)

print(Y.tolist())

"""Now splitting the dataset into training and test data"""

X_train, X_test, Y_train, Y_test= train_test_split(X,Y, test_size=0.4, stratify= Y, random_state= 2)

print(X.shape, X_train, X_test.shape)

#feature extraction(converting textual data to numerical data)
vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

print(X_test)

"""Training the machine learning model

Logistic regression
"""

model= LogisticRegression(max_iter=2000)

model.fit(X_train, Y_train)

"""Model Evaluation

Accuracy Score
"""

#accuracy score on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy= accuracy_score(Y_train, X_train_prediction)

print('Accuracy score on training data: ', training_data_accuracy)

#accuracy score on test data
X_test_prediction = model.predict(X_test)
test_data_accuracy= accuracy_score(Y_test, X_test_prediction)
print(X_test_prediction)

print('Accuracy score on testing data: ', test_data_accuracy)

"""Model accuracy = 88.09%

Saving the Trained Model into a pickle file
"""

filename = 'amazon_product_trained_model.pkl'
pickle.dump(model, open(filename,'wb'))

"""Model Testing"""

#loading the saved model
loaded_model = pickle.load(open('/content/amazon_product_trained_model.pkl','rb'))

X_new= X_test[14]
print(Y_test[14])

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==-1):
  print('Negative review')

if(prediction[0]==0):
  print('Neutral review')

else:
  print('Positive review')

X_new= X_test[29]
print(Y_test[29])

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==-1):
  print('Negative review')

if(prediction[0]==0):
  print('Neutral review')

if(prediction[0]==1):
  print('Neutral review')
