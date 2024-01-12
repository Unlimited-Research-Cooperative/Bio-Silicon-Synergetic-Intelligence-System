from flask import jsonify
from data_acquisition import start_board, stop_board
from my_data_processing import process_data

board = start_board()

def setup_routes(app):

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/data')
    def data():
        try:
            raw_data = board.get_current_board_data(256)  # Fetch latest data
            if raw_data.size == 0:
                raise ValueError("No data available from the board.")
            processed_data = process_data(raw_data)  # Process the data
            return jsonify(processed_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/stop')
    def stop():
        stop_board(board)
        return 'Stream stopped and session released', 200
