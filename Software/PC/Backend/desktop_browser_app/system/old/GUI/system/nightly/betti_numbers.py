import numpy as np
import gudhi as gd

# Assuming `reduced_data_umap` is your dimensionality-reduced data from the previous steps

def compute_persistence_diagrams(data):
    """
    Compute the persistence diagrams for a given dataset using Vietoris-Rips complex.
    :param data: Input dataset, assumed to be the output of a dimensionality reduction method.
    :return: Persistence diagrams for the dataset.
    """
    rips_complex = gd.RipsComplex(points=data, max_edge_length=2)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
    persistence = simplex_tree.persistence()
    return persistence

def plot_persistence_diagrams(persistence):
    """
    Plot the persistence diagrams.
    :param persistence: Persistence diagrams.
    """
    gd.plot_persistence_diagram(persistence)
    plt.show()

def calculate_betti_numbers(persistence):
    """
    Calculate Betti numbers from the persistence diagrams.
    :param persistence: Persistence diagrams.
    :return: Betti numbers (b0, b1, b2) counting the number of connected components, loops, and voids respectively.
    """
    betti_numbers = {i: 0 for i in range(3)}  # Assuming we're only interested in dimensions 0, 1, and 2
    for interval in persistence:
        if interval[0] < 3:  # Filter out infinite persistence intervals
            betti_numbers[interval[0]] += 1
    return betti_numbers['b0'], betti_numbers['b1'], betti_numbers['b2']

# Compute Persistence Diagrams
persistence = compute_persistence_diagrams(reduced_data_umap)

# Plot Persistence Diagrams
plot_persistence_diagrams(persistence)

# Calculate Betti Numbers
betti_numbers = calculate_betti_numbers(persistence)
print("Betti Numbers:", betti_numbers)
