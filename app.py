from flask import Flask, request, jsonify
from flask_cors import CORS
from src.backend.runner import chat_with_agent  # Updated import

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'response': 'route established'}), 200

@app.route('/chat', methods=['POST'])
async def chat():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = await chat_with_agent(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)