from PySide6.QtWidgets import QMessageBox

def show_message(msg_type: str, msg: str):
    message_box = QMessageBox()
    message_box.setWindowTitle("BSSIS Unified Software")
    message_box.setText(msg)

    types = ["error", "warn", "info"] 

    if msg_type == "error":
        message_box.setIcon(QMessageBox.Icon.Critical)
    elif message_box == "warn":
        message_box.setIcon(QMessageBox.Icon.Warning)
    elif message_box == "info":
        message_box.setIcon(QMessageBox.Icon.Information)
    elif msg_type not in types:
        raise Exception(f"Invalid message type: {msg_type}")
    
    message_box.show()
    message_box.exec()
