"""testing for KMeans"""
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import random

from city_classes import City


def testing(lst: set, city: City, n_clusters: int):
    for p in lst:
        city.add_place(p)
    temp = [list(x) for x in city.get_all_places()]
    df = pd.DataFrame(temp, columns=['x', 'y'])

    km = KMeans(n_clusters=n_clusters, init='k-means++')
    km.fit_predict(df)
    centers = km.cluster_centers_

    df.plot(x='x', y='y', kind='scatter', c='blue', s=50)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=15)

    plt.show()


if __name__ == '__main__':
    coords = {(random.randint(0, 25), random.randint(0, 25)) for _ in range(10)}
    toronto = City()
    num_clusters = 3
    testing(coords, toronto, num_clusters)



