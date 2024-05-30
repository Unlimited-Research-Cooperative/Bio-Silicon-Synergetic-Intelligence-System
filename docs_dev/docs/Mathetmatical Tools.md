# Mathematical Tools

## Detect Peaks:

\[
\begin{align*}
\text{Median Height} &= \text{median}(\text{flattened\_signals}) \\
\text{Standard Deviation of Height} &= \text{std}(\text{flattened\_signals}) \\
\text{Height Threshold} &= \text{Median Height} + \text{Standard Deviation of Height} \\
\text{Peak Distance} &= \text{len}(\text{flattened\_signals}) \times 0.05 \\
\text{Prominence Threshold} &= \text{Standard Deviation of Height} \times 0.5 \\
\text{Peak Count} &= \text{len}(\text{peaks}) \\
\text{Average Peak Height} &= \text{mean}(\text{properties}["peak\_heights"]) \\
\text{Average Distance Between Peaks} &= \text{mean}(\text{np.diff}(\text{peaks})) \\
\text{Average Prominence of Peaks} &= \text{mean}(\text{properties}["prominences"])
\end{align*}
\]

## Calculate Variance and Standard Deviation:

\[
\begin{align*}
\text{Variance} &= \text{var}(\text{signals}, \text{axis}=1) \\
\text{Standard Deviation} &= \text{std}(\text{signals}, \text{axis}=1)
\end{align*}
\]

## Calculate RMS:

\[
\text{RMS} = \sqrt{\text{mean}(\text{signals}^2, \text{axis}=1)}
\]

Where,
\begin{align*}
\text{RMS} &= \text{Root Mean Square} \\
\text{signals} &= \text{Array containing the input signals} \\
\text{axis} &= \text{Axis along which the mean is computed, typically axis=1 for row-wise mean}
\end{align*}

## Frequency Bands:

\[
\begin{align*}
\text{Band Features}[i, j] &= \text{mean}(\text{psd}[\text{idx}]) \quad \text{if} \quad \text{np.any}(\text{idx}) \\
& \quad \quad \quad \text{else} \quad 0.0
\end{align*}
\]

Where,
\begin{align*}
\text{Band Features}[i, j] &= \text{Mean power spectral density (PSD) in band } (i, j) \\
\text{psd} &= \text{Power Spectral Density} \\
\text{idx} &= \text{Indices of frequencies within band } (i, j) \\
\text{np.any}(\text{idx}) &= \text{Check if any indices are present in the band} \\
\end{align*}

## Calculate Spectral Entropy:

\[
\text{Spectral Entropy} = -\sum_{i=1}^{n} p_i \log_2(p_i)
\]

Where,
\begin{align*}
\text{Spectral Entropy} &= \text{Entropy of the power spectral density (PSD)} \\
p_i &= \text{Normalized power in frequency bin } i \\
n &= \text{Number of frequency bins}
\end{align*}

## Spectral Centroids:

\[
\text{Spectral Centroid} = \frac{\sum_{i=1}^{N} f_i \cdot |X(i)|}{\sum_{i=1}^{N} |X(i)|}
\]

Where,
\begin{align*}
\text{Spectral Centroid} &= \text{Average frequency weighted by the magnitude spectrum} \\
f_i &= \text{Frequency of bin } i \\
X(i) &= \text{Magnitude of the Fourier transform at bin } i \\
N &= \text{Number of frequency bins}
\end{align*}

## Spectral Edge Density:

\[
\text{Spectral Edge Density} = \text{Frequency}\left[\text{argmax}\left(\text{cumulative\_sum} \geq \text{threshold}\right)\right]
\]

Where,
\begin{align*}
\text{cumulative\_sum} &= \text{Cumulative Sum of Power Spectral Density (PSD)} \\
\text{threshold} &= \text{User-defined threshold}
\end{align*}
