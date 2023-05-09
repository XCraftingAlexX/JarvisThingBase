import threading
import cv2
import os
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False

reference_imgs = []
for filename in os.listdir("references"):
    img = cv2.imread(os.path.join("references", filename))
    if img is not None:
        reference_imgs.append(img)

models = ['VGG-Face', 'Facenet', 'OpenFace']

def check_face(frame):
    global face_match
    for reference_img in reference_imgs:
        try:
            for model in models:
                result = DeepFace.verify(frame, reference_img.copy(), model_name=model)
                if result['verified']:
                    face_match = True
                    return
        except ValueError:
            pass
    face_match = False

def recognize_faces():
    global face_match
    global counter
    while True:
        ret, frame = cap.read()
        counter += 1

        if ret:
            try:
                if counter % 5 == 0:
                    frame_copy = frame.copy()
                    check_face(frame_copy)
            except ValueError:
                pass

def render_video():
    while True:
        ret, frame = cap.read()

        if ret:
            if face_match:
                cv2.putText(frame, "ALEX", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NOT ALEX", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            cv2.imshow("video", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

video_thread = threading.Thread(target=render_video)
video_thread.start()

recognize_faces()