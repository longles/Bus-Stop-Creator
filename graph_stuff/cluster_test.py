"""testing for KMeans"""
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

from city_classes import City


def testing(lst: list, city: City, n_clusters: int):
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
    coords = [(19, 15), (16, 12), (11, 12), (1, 13), (7, 13), (4, 3), (6, 5), (11, 9), (3, 13),
              (9, 10), (2, 11), (8, 1), (18, 13), (16, 17), (3, 13), (7, 2), (17, 8), (18, 12),
              (14, 13), (14, 10)]
    toronto = City()
    num_clusters = 5
    testing(coords, toronto, num_clusters)



