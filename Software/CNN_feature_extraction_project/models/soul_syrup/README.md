# Feature Extraction and Neural Network Training with PyTorch

## Overview
This subproject focuses on extracting features from neural signal data and using these features to train a neural network with PyTorch. The data is segmented into 0.25-second windows, and various features are extracted for each channel. The features are then converted into tensors and organized into datasets for training, validation, and testing.

## Preprocessing and Feature Extraction

### Preprocessing and Feature Extraction
This step preprocesses the neural signal data, extracts features, and saves the processed data into numpy arrays.

1. **Load the EDF file**: The neural signal data is loaded from an EDF file.
2. **Downsample the Data**: The data is downsampled to 500 Hz if the original sampling rate is 1000 Hz.
3. **Segment the Data**: The data is segmented into 0.25-second windows.
4. **Normalize the Data**: The data is normalized to the range [0, 1].
5. **Extract Features**: Various features are extracted from each segment, including peak detection, frequency bands, spectral features, and more.
6. **Save the Features**: The normalized data and extracted features are saved to numpy files.
