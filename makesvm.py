import pickle
import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split, GridSearchCV


df = pd.read_csv("data5x5.csv")
y = df["idx"]
X = df.drop("idx", axis="columns")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True)

# Define the parameter grid for the SVM
param_grid = {
    'C': [0.1, 1, 10, 1000],
    'kernel': ['poly'],
    'degree': [3, 5, 7, 9, 10, 11, 12, 13, 14, 15],
    'n_jobs': [-1]
}

# Perform grid search to find the best parameters
grid_search = GridSearchCV(svm.SVC(), param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Get the best parameters and the corresponding model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Fit the best model on the training data
best_model.fit(X_train, y_train)
predicted = best_model.predict(X_test)
# Save the best model
pickle.dump(best_model, open("best_model.pkl", 'wb'))

# clf = svm.SVC(kernel="poly", degree=14)
# clf.fit(X_train, y_train)
# predicted = clf.predict(X_test)


accuracy = metrics.accuracy_score(y_test, predicted)
print("Accuracy:", accuracy)