from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-detection', methods=['POST'])
def start_detection():
    # Run the YOLO detection script as a subprocess
    subprocess.Popen(["python", "helmet_detection_system.py"])
    return "Detection Program Started Successfully!"

if __name__ == '__main__':
    app.run(debug=True)
