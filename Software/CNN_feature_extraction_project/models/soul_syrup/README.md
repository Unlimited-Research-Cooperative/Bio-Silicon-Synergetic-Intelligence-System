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
7. **Create Tensors**: 
7. **Define Custom Activation Functions**
8. **Train Test Eval Split and Prep**
9. **Neural Net Design**
10. **Neural Net Architecture Visualisation**
11. **Weight and Activation Quantisation**
12. **Feature Quantisation**
13. **Performance Eval**
14. **Channel-wise Eval**


## Custom Activation Functions

In addition to traditional activation functions like ReLU or Sigmoid, custom activation functions based on external data are implemented:

1. **AmplitudeEnvelopeActivation**
2. **AverageDistanceActivation**
3. **AveragePeakHeightActivation**
4. **AverageProminenceActivation**
5. **BanachManifoldActivation**
6. **BernoulliSchemeActivation**
7. **BoxCountingDimensionActivation**
8. **ComplexManifoldActivation**
9. **CumulativeSumsActivation**
10. **EhresmannConnectionActivation**
11. **EntropyActivation**
12. **FFTResultsActivation**
13. **FrechetManifoldActivation**
14. **FrequenciesActivation**
15. **GeodesicGaussianCurvatureActivation**
16. **GaussianActivation**
17. **GrowthMeasureActivation**
18. **HarmonicOscillatorActivation**
19. **HarmonicsDetectionActivation**
20. **HarmonicsLyapunovActivation**
21. **HermitianManifoldActivation**
22. **HomomorphismActivation**
23. **HolographicInformationActivation**
24. **HyperbolicActivation**
25. **InfinitesimalGeneratorActivation**
26. **JacobianActivation**
27. **KakutaniActivation**
28. **KatzFractalDimensionActivation**
29. **KolmogorovSinaiActivation**
30. **LaplaceTransformActivation**
31. **LieGroupActivation**
32. **LorentzActivation**
33. **LyapunovActivation**
34. **LyapunovDimensionActivation**
35. **LyapunovStabilityActivation**
36. **LyapunovVectorsActivation**
37. **MatrixLieGroupActivation**
38. **MinkowskiActivation**
39. **MultipartiteConcurrenceActivation**
40. **PeakCountsActivation**
41. **PeakHeightActivation**
42. **PhaseSpaceActivation**
43. **PhaseSpaceCentroidsActivation**
44. **PhasesActivation**
45. **PolynomialActivation**
46. **PositiveFFTResultsActivation**
47. **PositiveFrequenciesActivation**
48. **PSDActivation**
49. **PyragasActivation**
50. **QuantumActivation**
51. **QuaternionicManifoldActivation**
52. **RelativisticVelocityActivation**
53. **ResonanceFrequencyActivation**
54. **RiemannCurvatureActivation**
55. **RiemannianActivation**
56. **RMSActivation**
57. **SampleEntropyActivation**
58. **SincActivation**
59. **SoulActivation**
60. **SpaceCurvatureActivation**
61. **SpectralEdgeDensityActivation**
62. **SpectralEntropyActivation**
63. **StdDevActivation**
64. **SymplecticActivation**
65. **ThresholdsActivation**
66. **TopologicalActivation**
67. **TotalPowersActivation**
68. **UMAPActivation**
69. **VectorBundleActivation**
70. **VarianceActivation**
71. **WaveletActivation**
72. **WaveletFractalActivation**
73. **WeightedUndirectedNetworkActivation**
74. **PhaseSpaceCentroidsActivation**
75. **MultipartiteConcurrenceActivation**
76. **LaplaceTransformActivation**
77. **SymplecticActivation**
78. **HyperbolicActivation**
79. **GeodesicGaussianCurvatureActivation**
80. **TheoremaEgregiumActivation**
81. **RiemannianActivation**
82. **RiemannCurvatureActivation**
83. **JacobianActivation**
84. **LyapunovVectorsActivation**
85. **LyapunovStabilityActivation**
86. **LyapunovDimensionActivation**
87. **OGYActivation**
88. **KolmogorovSinaiActivation**
89. **AmplitudeEnvelopeActivation**
90. **PyragasActivation**
91. **SoulActivation**
92. **GrowthMeasureActivation**
93. **BernoulliSchemeActivation**
94. **KakutaniActivation**
95. **MinkowskiActivation**
96. **RelativisticVelocityActivation**
97. **SpaceCurvatureActivation**
98. **LieGroupActivation**
99. **MatrixLieGroupActivation**
100. **ComplexManifoldActivation**
101. **QuaternionicManifoldActivation**
102. **HermitianManifoldActivation**
103. **BanachManifoldActivation**
104. **FrechetManifoldActivation**
105. **HomomorphismActivation**
106. **InfinitesimalGeneratorActivation**
107. **EhresmannConnectionActivation**
108. **VectorBundleActivation**
109. **HolographicInformationActivation**
110. **GaussianActivation**
111. **SincActivation**
112. **PolynomialActivation**
113. **WaveletActivation**
114. **QuantumActivation**
115. **LorentzActivation**
116. **EntropyActivation**
117. **HarmonicOscillatorActivation**
118. **HarmonicsDetectionActivation**

These custom activation functions allow for incorporating external information into the neural network's activation process, potentially enhancing its performance and interpretability.
