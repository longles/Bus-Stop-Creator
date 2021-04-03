"""testing for KMeans"""
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

from city_classes import City

toronto = City()

toronto.add_place((0, 0))
toronto.add_place((3, 4))
toronto.add_place((10, 15))
toronto.add_place((9, 0))
toronto.add_place((0, 7))


temp = [list(x) for x in toronto.get_all_places()]
df = pd.DataFrame(temp, columns=['x', 'y'])

km = KMeans(n_clusters=2, init='k-means++')
km.fit_predict(df)
centers = km.cluster_centers_

df.plot(x='x', y='y', kind='scatter', c='blue', s=50)
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=15)

plt.show()
