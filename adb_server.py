from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import threading

app = Flask(__name__)
CORS(app)  # Allow all origins

is_recording = False
recording_thread = None

@app.route('/start_record', methods=['POST'])
def start_record():
    global is_recording, recording_thread
    if not is_recording:
        is_recording = True
        recording_thread = threading.Thread(target=record_events)
        recording_thread.start()
        return jsonify({"status": "Recording started"})
    return jsonify({"status": "Already recording"})

@app.route('/stop_record', methods=['POST'])
def stop_record():
    global is_recording
    is_recording = False
    return jsonify({"status": "Recording stopped"})

@app.route('/play', methods=['POST'])
def play():
    subprocess.call(["python", "adbrecord.py", "-p", "recorded_events.txt"])
    return jsonify({"status": "Playback started"})

def record_events():
    with open("recorded_events.txt", "w") as f:
        proc = subprocess.Popen(["python", "adbrecord.py", "-r", "recorded_events.txt"], stdout=subprocess.PIPE)
        while is_recording:
            line = proc.stdout.readline().decode('utf-8')
            if not line:
                break
            f.write(line)
        proc.terminate()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
