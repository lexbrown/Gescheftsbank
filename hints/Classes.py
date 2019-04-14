#Classes

import numpy as np
from sklearn import neighbors
predictors = np.random.random(1000).reshape(500, 2)
target = np.around(predictors.dot(np.array([0.4, 0.6])) + np.random.random(500))
clf = neighbors.KNeighborsClassifier(n_neighbors = 10)
knn = clf.fit(predictors, target)
knn_score = knn.score(predictors, target)
print(knn_score)