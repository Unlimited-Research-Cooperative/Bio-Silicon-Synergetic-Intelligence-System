from data_processing.higuchi_fractal_dimension import compute_hfd_for_live_data

def process_data(raw_data):
    """
    Process raw data using the Higuchi Fractal Dimension calculation.

    :param raw_data: Raw data from BrainFlow API, expected to be a 2D numpy array.
    :return: Processed data as a list of Higuchi Fractal Dimension values.
    """
    # Call the compute_hfd_for_live_data function from higuchi_fractal_dimension.py
    # You might need to adjust this call based on the actual data format and requirements
    processed_data = compute_hfd_for_live_data(raw_data)

    return processed_data