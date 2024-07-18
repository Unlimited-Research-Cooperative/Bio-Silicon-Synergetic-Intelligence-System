# Datasets

# /shuffleboard/

## normalized_dataset_500hz_500ms_consecutive_buckets.npz

Contains 500ms worth of 32 channel signal data in which two consecutive blocks of 250ms signal data were concatenated. 

## (feature)_labels_500ms_500hz_tensor.pt

Contains binary labels denoting whether or not the feature value has increased or decreased when comparing two consecutive 250ms blocks of signal data. 


## Example Usage

```python
import torch
import numpy as np

# Load signal data
signal_data = np.load('../datasets/processed/shuffleboard/normalized_dataset_500hz_500ms_consecutive_buckets.npz')
X = torch.tensor(signal_data['data'], dtype=torch.float32)

# Load labels for a specific feature (e.g., 'rms')
feature_name = 'rms'
y = torch.load(f'../datasets/processed/shuffleboard/{feature_name}_labels_250ms_500hz_tensor.pt')

print(f"Signal data shape: {X.shape}")
print(f"Labels shape: {y.shape}")

# Signal data shape: torch.Size([7591, 32, 250])
# Labels shape: torch.Size([7591])






