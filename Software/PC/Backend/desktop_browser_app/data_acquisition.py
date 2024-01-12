from brainflow import BoardShim, BrainFlowInputParams, BoardIds
import time

def start_board():
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    time.sleep(1)  # Allow the board to accumulate some data
    return board

def stop_board(board):
    board.stop_stream()
    board.release_session()
