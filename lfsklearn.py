import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Define a function that runs clustering on a df and returns the clusters for each row in df
def Cluster(df, numClusters):
    # Create a k-means clusterer.  
    kmeans = KMeans(init='random', n_clusters=numClusters, n_init=10, max_iter=10)

    # Train it
    kmeans.fit(df)

    # Make some predictions about which cluster each sample belongs to
    clusters = kmeans.predict(df)
    
    return clusters


# Generalise to a function
def ClusterScatter(df, xFeature, yFeature, clusterFeature):
    #Plot the clusters obtained using k means
    plt.figure()
    scatter = plt.scatter(df[xFeature],df[yFeature],c=df[clusterFeature],s=50)
    plt.title('K-Means Clustering')
    plt.xlabel(xFeature)
    plt.ylabel(yFeature)


def PCAPlot(df, numClusters):
    # Visualize the results on PCA-reduced data
    reduced_data = PCA(n_components=2).fit_transform(df[df.columns[:64]])
    kmeans = KMeans(init='k-means++', n_clusters=numClusters, n_init=10)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()
