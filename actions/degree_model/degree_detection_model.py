from dataset import dataset

import tensorflow_hub as hub
import tensorflow_text as text

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

import pickle

from bert_model import get_sentence_embedding

# Splitting into sentences and labels
sentences, labels = zip(*dataset)

# Assigning values to X and y
X = list(sentences)
y = list(labels)

x_train_embedding, x_test_embedding, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify = y)

x_train_embedding = get_sentence_embedding(x_train_embedding)
x_test_embedding = get_sentence_embedding(x_test_embedding)

# Reshape x_train_embedding
x_train_embedding = np.array(x_train_embedding).reshape(-1, 768)

# Define the parameter grid for grid search
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto']
}

# Create an SVM classifier with grid search
svm = SVC()
grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy')

# Fit the classifier to the training data
grid_search.fit(x_train_embedding, y_train)

# Get the best SVM classifier from grid search
best_svm = grid_search.best_estimator_

# Fit the SVM classifier with training data
best_svm.fit(x_train_embedding, y_train)

# Save the SVM model to a file
with open('svm_model.pkl', 'wb') as file:
    pickle.dump(best_svm, file)