from flask import jsonify
from data_acquisition import get_live_data
from my_data_processing import process_data  # make sure to import process_data if you're using it

def setup_routes(app):

    @app.route('/data')
    def data():
        try:
            raw_data = get_live_data(256)  # Fetch latest data
            if raw_data.size == 0:
                raise ValueError("No data available from the simulated board.")
            processed_data = process_data(raw_data)  # Process the data
            return jsonify(processed_data.tolist())  # Convert numpy array to list before jsonify
        except Exception as e:
            return jsonify({"error": str(e)}), 500
