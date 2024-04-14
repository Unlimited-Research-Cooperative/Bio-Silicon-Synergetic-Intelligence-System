import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from minepy import MINE
import multiprocessing
import os

# Load EEG data
EEG_data = np.load('/home/vincent/AAA_projects/MVCS/Neuroscience/eeg_data_with_channels.npy', allow_pickle=True)

# Extract EEG channel names
eeg_channel_names = ['Fp1', 'Fpz', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6',
                    'M1', 'T7', 'C3', 'Cz', 'C4', 'T8', 'M2', 'CP5', 'CP1', 'CP2', 'CP6',
                    'P7', 'P3', 'Pz', 'P4', 'P8', 'POz', 'O1', 'Oz', 'O2']

max_dim = 20  # Maximum embedding dimension to consider

def delay_embedding(data, emb_dim, delay):
    N = len(data)
    return np.array([data[i:i+emb_dim*delay:delay].flatten() for i in range(N - emb_dim * delay + 1)])

def false_nearest_neighbors(data, emb_dim, delay, R=10):
    N = len(data)
    false_neighbors = np.zeros(emb_dim)

    for d in range(1, emb_dim + 1):
        emb_data = delay_embedding(data, d, delay)
        nbrs = NearestNeighbors(n_neighbors=2).fit(emb_data[:-delay])
        distances, indices = nbrs.kneighbors(emb_data[:-delay])
        neighbor_index = indices[:, 1]
        neighbor_distance = np.abs(data[neighbor_index + delay] - data[np.arange(N - d * delay) + delay])
        false_neighbors[d - 1] = np.mean((neighbor_distance / distances[:, 1]) > R)

    return false_neighbors

# Calculate FNN for different embedding dimensions for each channel
fnn_data = {}
for channel_idx, channel_name in enumerate(eeg_channel_names):
    channel_data = EEG_data[channel_idx]
    channel_data_flat = channel_data.flatten()
    fnn = false_nearest_neighbors(channel_data_flat, emb_dim=max_dim, delay=1)
    fnn_data[channel_name] = fnn
    print(f'Channel: {channel_name}')
    for dim, fnn_value in enumerate(fnn, start=1):
        print(f'Embedding Dimension {dim}: Fraction of FNN = {fnn_value:.4f}')

# Plot the FNN as a function of embedding dimension for each channel
plt.figure()
for channel_name in eeg_channel_names:
    fnn = fnn_data[channel_name]
    plt.plot(np.arange(1, max_dim+1), fnn, label=channel_name)
plt.xlabel('Embedding Dimension')
plt.ylabel('Fraction of False Nearest Neighbors')
plt.title('Estimation of Embedding Dimension using FNN Method')
plt.legend()
plt.show()

# Save the FNN data to a file
output_filename = '/home/vincent/AAA_projects/MVCS/Neuroscience/false_nearest_neighbors.npy'
np.save(output_filename, fnn_data)
print(f'FNN data saved to {output_filename}')

def mutual_info_worker(args):
    data1, data2 = args
    mine = MINE()
    mine.compute_score(data1, data2)
    return mine.mic()

def determine_delay(data, max_delay=100, subsample_factor=10):
    subsampled_data = data[::subsample_factor]
    with multiprocessing.Pool() as pool:
        args_list = [(subsampled_data[:-i], subsampled_data[i:]) for i in range(1, max_delay+1)]
        mi_values = pool.map(mutual_info_worker, args_list)
    min_index = np.argmin(mi_values)
    return min_index + 1

# Loop through each channel for phase space reconstruction
for selected_channel in eeg_channel_names:
    channel_index = eeg_channel_names.index(selected_channel)
    channel_data = EEG_data[:, channel_index]
    
    # Determine optimal delay using mutual information with subsampling
    optimal_delay = determine_delay(channel_data, subsample_factor=50)
    
    # 2D Embedding
    emb_dim_2d = 2
    embedded_channel_data_2d = delay_embedding(channel_data, emb_dim=emb_dim_2d, delay=optimal_delay)
    
    # Save the 2D embedded data (Adjust path as needed)
    np.save(f'/home/vincent/AAA_projects/MVCS/Neuroscience/Analysis/Phase Space/2dembedding_data/2dembedded_{selected_channel}_data.npy', embedded_channel_data_2d)
      
    # Create 2D scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(embedded_channel_data_2d[:, 0], embedded_channel_data_2d[:, 1], s=0.5)
    plt.title(f'2D Phase Space Plot for Channel {selected_channel}')
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.savefig(f'/home/vincent/AAA_projects/MVCS/Neuroscience/Analysis/Phase Space/2dembedding_data/PhaseSpace_2D_{selected_channel}.png', dpi=300)
    plt.close()
    
    # 3D Embedding
    emb_dim_3d = 3
    embedded_channel_data_3d = delay_embedding(channel_data, emb_dim=emb_dim_3d, delay=optimal_delay)
    
    # Create 3D scatter plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(embedded_channel_data_3d[:, 0], embedded_channel_data_3d[:, 1], embedded_channel_data_3d[:, 2], s=0.5)
    ax.set_title(f'3D Phase Space Plot for Channel {selected_channel}')
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.set_zlabel('Dimension 3')
    plt.savefig(f'/home/vincent/AAA_projects/MVCS/Neuroscience/Analysis/Phase Space/3dembedding_data/PhaseSpace_3D_{selected_channel}.png', dpi=300)
    plt.close()


