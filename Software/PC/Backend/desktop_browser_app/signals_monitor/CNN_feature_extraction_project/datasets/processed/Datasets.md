# Datasets

# /interim/ecog_dataset_livesystem_250hz_32channel.pkl


This dataset contains preprocessed ECoG (electrocorticography) data and extracted features for a machine learning project. The data is organized into blocks, each representing a 200ms window of ECoG signals from 32 channels. 

Note: there is a corresponding dataset at 500Hz in which the only difference is that the 200ms window is sampled at 500Hz.

## Dataset Structure

The dataset is stored as a dictionary with the following keys:

- `"buckets"`: A numpy array of shape `(num_blocks, num_channels, block_size)` containing the preprocessed ECoG data divided into blocks.
- `"targets"`: A list of dictionaries, where each dictionary corresponds to a block and contains the extracted features for that block.
- `"channel_info"`: A dictionary providing information about the ECoG channels, including the channel names and the total number of channels.
- `"num_channels"`: 32

## Extracted Features

| Feature Name                                          | Dimensions                       | Description                                                                                                 |
|-------------------------------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------------------|
| `"peaks"`                                             | `(8,)`                           | Peak detection features stored in the following order: <br>1. Peak count <br>2. Average peak height <br>3. Average distance between peaks <br>4. Average prominence <br>5. Median height <br>6. Standard deviation of height <br>7. Peak distance <br>8. Prominence threshold |
| `"std"`                                               | `(num_channels,)`                | Standard deviation of each channel's signal. The values are flattened into a 1D array, with each element corresponding to a channel. |
| `"variance"`                                          | `(num_channels,)`                | Variance of each channel's signal. The values are flattened into a 1D array, with each element corresponding to a channel. |
| `"rms"`                                               | `(num_channels,)`                | Root mean square (RMS) value of each channel's signal. The values are flattened into a 1D array, with each element corresponding to a channel. |
| `"freq_bands"`                                        | `(num_channels * 4,)`            | Mean power spectral density (PSD) in different frequency bands for each channel. The values are flattened into a 1D array, with the bands ordered as follows for each channel: <br>1. Delta band <br>2. Theta band <br>3. Alpha band <br>4. Beta band |
| `"spectral_entropy"`                                  | `(num_channels,)`                | Spectral entropy of each channel's signal. The values are stored in a 1D array, with each element corresponding to a channel. |
| `"spectral_centroids"`                                | `(num_channels,)`                | Spectral centroid of each channel's signal. The values are stored in a 1D array, with each element corresponding to a channel. |
| `"spectral_edge_density"`                             | `(num_channels,)`                | Spectral edge density of each channel's signal. The values are stored in a 1D array, with each element corresponding to a channel. |
| `"phase_locking_values"`                              | `(num_channels * num_channels,)` | Phase locking values (PLV) matrix representing the synchronization between channels. The matrix is flattened into a 1D array in row-major order. |
| `"higuchi_fractal_dimension"`                         | `(num_channels,)`                | Higuchi fractal dimension of each channel's signal. The values are stored in a 1D array, with each element corresponding to a channel. If the fractal dimension cannot be computed for a channel, NaN is used as a placeholder. |
| `"zero_crossing_rates"`                               | `(num_channels,)`                | Zero crossing rate of each channel's signal. The values are stored in a 1D array, with each element corresponding to a channel. |
| `"num_empirical_mode_decomposition_imfs_per_channel"` | `(num_channels,)`                | Number of intrinsic mode functions (IMFs) obtained from empirical mode decomposition (EMD) for each channel. The values are stored in a 1D array of type object, with each element corresponding to a channel. |
| `"evolution_rate"`                                    | `(num_channels,)`                | Evolution rate of each channel's signal. The values are stored in a 1D array, with each element corresponding to a channel. |

## Example Usage

```python
import pickle

# Load the dataset
with open("/interim/ecog_dataset_livesystem_250hz_32channel.pkl", "rb") as file:
    dataset = pickle.load(file)

# Access the dataset components
buckets = dataset["buckets"]
targets = dataset["targets"]
channel_info = dataset["channel_info"]

# Get the number of blocks in the dataset
num_blocks = len(buckets)

# Select a specific block index
block_index = 42

# Get the selected block and its associated targets
selected_block = buckets[block_index]
selected_targets = targets[block_index]

# Access specific features from the selected targets
peak_count = selected_targets["peaks"][0]
average_peak_height = selected_targets["peaks"][1]
average_distance_between_peaks = selected_targets["peaks"][2]
average_prominence = selected_targets["peaks"][3]
median_height = selected_targets["peaks"][4]
std_height = selected_targets["peaks"][5]
peak_distance = selected_targets["peaks"][6]
prominence_threshold = selected_targets["peaks"][7]

spectral_entropy = selected_targets["spectral_entropy"]
plv_matrix = selected_targets["phase_locking_values"].reshape((channel_info["num_channels"], channel_info["num_channels"]))