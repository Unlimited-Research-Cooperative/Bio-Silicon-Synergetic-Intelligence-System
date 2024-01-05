import sys
print(sys.path)
from flask import Flask
from api_routes import setup_routes

app = Flask(__name__, static_folder='static', template_folder='templates')

setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



