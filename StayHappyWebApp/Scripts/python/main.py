from flask import Flask, Response, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import sys
from flask_cors import CORS
import threading

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


app = Flask(__name__)
CORS(app)

face_classifier = cv2.CascadeClassifier(r'C:\Users\kvist\Skola\AI\djupinlaerning\stay_happy\StayHappyWebApp\Scripts\python\haarcascade_frontalface_default.xml')
classifier = load_model(r'C:\Users\kvist\Skola\AI\djupinlaerning\stay_happy\StayHappyWebApp\Scripts\python\model.h5', compile=False)

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

current_label = 'Neutral'
label_lock = threading.Lock()

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                new_label = emotion_labels[prediction.argmax()]
                
                with label_lock:
                    global current_label
                    current_label = new_label                
                
                # label_position = (x, y)
                # cv2.putText(frame, current_label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/current_label')
def get_current_label():
    global current_label
    with label_lock:
        return jsonify({'label': current_label})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
