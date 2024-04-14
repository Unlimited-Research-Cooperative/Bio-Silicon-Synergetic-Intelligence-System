import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import umap.umap_ as umap
from geomstats.geometry.special_orthogonal import SpecialOrthogonal
import geomstats.learning.frechet_mean as frechet_mean
import geomstats.geometry.hypersphere as hypersphere
from geomstats.learning.frechet_mean import FrechetMean
from geomstats.geometry.euclidean import Euclidean

# Assuming the file contains continuous data recorded at 500 Hz from 32 channels
file_path = 'ecog_data_last_24h.npy'
ECoG_data = np.load(file_path)

# Preprocessing steps (filtering, detrending, artifact removal) are assumed to be done prior
# This example focuses on the analysis part
# Apply UMAP for dimensionality reduction to 3D for better visualization and further analysis
reduced_data_umap = umap.UMAP(n_components=3).fit_transform(ECoG_data)
# Apply t-SNE for comparison
reduced_data_tsne = TSNE(n_components=3).fit_transform(ECoG_data)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(reduced_data_umap[:, 0], reduced_data_umap[:, 1], s=1)
plt.title('UMAP Reduction')
plt.subplot(1, 2, 2)
plt.scatter(reduced_data_tsne[:, 0], reduced_data_tsne[:, 1], s=1)
plt.title('t-SNE Reduction')
plt.show()

sphere = hypersphere.Hypersphere(dim=2)
point_a, point_b = sphere.random_point(), sphere.random_point()
distance = sphere.metric.dist(point_a, point_b)

# Frechet Mean on Hypersphere
points = sphere.random_point(n_samples=10)
frechet_mean_sphere = FrechetMean(metric=sphere.metric)
frechet_mean_sphere.fit(points)
mean_sphere = frechet_mean_sphere.estimate_

so3 = SpecialOrthogonal(n=3, point_type='vector')
points_so3 = so3.random_point(n_samples=10)
frechet_mean_so3 = FrechetMean(metric=so3.metric)
frechet_mean_so3.fit(points_so3)
mean_so3 = frechet_mean_so3.estimate_

# Partitioning the reduced space into 4 regions as an example
quantiles = np.quantile(reduced_data_umap, [0.25, 0.5, 0.75], axis=0)

def partition_phase_space(data, quantiles):
    symbols = np.zeros(data.shape[0], dtype=int)
    for i, point in enumerate(data):
        if point[0] < quantiles[0][0]:
            symbols[i] = 0
        elif point[0] < quantiles[1][0]:
            symbols[i] = 1
        elif point[0] < quantiles[2][0]:
            symbols[i] = 2
        else:
            symbols[i] = 3
    return symbols

symbols = partition_phase_space(reduced_data_umap, quantiles)

plt.figure(figsize=(6, 6))
for i in range(4):
    plt.scatter(reduced_data_umap[symbols == i, 0], reduced_data_umap[symbols == i, 1], s=1, label=f'Partition {i}')
plt.title('Symbolic Dynamics Partitioning (UMAP)')
plt.legend()
plt.show()
