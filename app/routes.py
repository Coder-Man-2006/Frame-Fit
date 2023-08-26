from flask import render_template, request, jsonify
from PIL import Image, ImageDraw
from flask_socketio import SocketIO
import io
import base64
from algorithm.thealgo import FaceAnalyzer

from app import app

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    print('webcam active: true')
    return 'Python code executed successfully'

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data_url = request.form['frame']
    header, encoded = data_url.split(",", 1)
    binary_data = base64.decodebytes(encoded.encode())
    
    try:
        image = Image.open(io.BytesIO(binary_data))
        print("Image format:", image.format)
    except Exception as e:
        print("Error opening image:", e)
        return jsonify({'error': 'Failed to process the image.'})
    
    try:
        face_analyzer = FaceAnalyzer()
        processed_image = face_analyzer.process_single_image(image)
    except Exception as e:
        print("Error processing image:", e)
        return jsonify({'error': 'Failed to process the image.'})

    try:
        buffered = io.BytesIO()
        processed_image.save(buffered, format="PNG")
        processed_base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print("Error encoding image:", e)
        return jsonify({'error': 'Failed to encode the image.'})
    print("Returning image)")
    return jsonify({'processed_image': f'data:image/png;base64,{processed_base64_image}'})

@socketio.on('connect')
def handle_connect():
    print('WebSocket client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('WebSocket client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
