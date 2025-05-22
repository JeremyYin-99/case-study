from flask import Flask
from flask_cors import CORS
from src.backend.runner import agent


app = Flask(__name__)
CORS(app)

# Route for the root URL (/)
@app.route('/')
def index():
    """ Returns basic response """
    return "All Good"

app.route('/chat', methods=['POST'])(agent)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)