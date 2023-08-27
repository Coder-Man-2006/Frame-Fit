from flask import Flask, render_template, request
from app import app
from PIL import Image, ImageDraw
from flask_socketio import SocketIO

@app.route('/', methods=['GET', 'POST'])
def index():
    img_path = None

    if request.method == 'POST':
        number = int(request.form['number'])
        
        img = Image.new('RGB', (100, 30), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), str(number), fill=(255, 255, 0))

        img_path = "static/images/number.png"
        img.save(f"app/{img_path}")
        
    return render_template('index.html', img_path=img_path)

@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    print('webcam active: true')
    return 'Python code executed successfully'


app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('WebSocket client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('WebSocket client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
    
    
    
    
    
    
    
<<<<<<< HEAD
    
=======
    
>>>>>>> parent of 0e012dd (integrated frontend and backend)
