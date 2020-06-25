import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

df = pd.read_csv("C:/Users/Devna Chaturvedi/Desktop/Summer Semester - Python/Lesson 6/Python_Lesson6/CC.csv")
df.head()
print(df.head())
df = df.drop('CUST_ID', axis = 1)

df.head(2)

print(str(df.shape))
print(df.isnull().sum().sum())
df = df.dropna(how = 'any')
print(str(df.shape))
df.fillna(method ='ffill', inplace = True)


# to Standardize data
scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)

# to Normalizing the Data
normalized_df = normalize(scaled_df)

# Converting the numpy array into a pandas DataFrame
normalized_df = pd.DataFrame(normalized_df)

# Reducing the dimensions of the data
pca = PCA(n_components=2)
X_principal = pca.fit_transform(normalized_df)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']

X_principal.head(2)
print(X_principal.head(2))
sse = {}
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(X_principal)
    sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
plt.figure()
plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.show()
silhouette_scores = []

for n_cluster in range(2, 8):
    silhouette_scores.append(
        silhouette_score(X_principal, KMeans(n_clusters=n_cluster).fit_predict(X_principal)))


# Plotting a bar graph to compare the results
k = [2, 3, 4, 5, 6, 7]
plt.bar(k, silhouette_scores)
plt.xlabel('Number of clusters', fontsize=10)
plt.ylabel('Silhouette Score', fontsize=10)
plt.show()
kmeans = KMeans(n_clusters=3)
kmeans.fit(X_principal)
print(kmeans.fit(X_principal))
# Visualizing the clustering
plt.scatter(X_principal['P1'], X_principal['P2'],c = KMeans(n_clusters = 3).fit_predict(X_principal), cmap =plt.cm.winter)
plt.show()
# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .01
# point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = X_principal['P1'].min() - 1, X_principal['P1'].max() + 1
y_min, y_max = X_principal['P2'].min() - 1, X_principal['P2'].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
# Obtain labels for each point in mesh. Use last trained model.

Z = kmeans.predict(np.array(list(zip(xx.ravel(), yy.ravel()))))

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.winter,
           aspect='auto', origin='lower')

plt.plot(X_principal['P1'], X_principal['P2'], 'k.', markersize=1)
# Plot the centroids as a red X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],marker='o', s=10, linewidths=3,color='r', zorder=10)
plt.title('K-means clustering on the credit card dataset (PCA-reduced data)\n'
'Centroids are marked with red circle')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.show()
