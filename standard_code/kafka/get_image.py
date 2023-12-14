import cv2
import time
from kafka import KafkaProducer
import config

topic_name = 'camera_in'
p = KafkaProducer(
    bootstrap_servers=[config.kafka_ip],
    max_request_size=9000000
)

cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    if ret:
        frame = cv2.resize(frame, fx=0.2, fy=0.2, dsize=None)
        cv2.imshow("Image", frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        p.send(topic_name, buffer.tobytes())
        p.flush()

        time.sleep(3)
    else:
        break
    
cam.release()
cv2.destroyAllWindows()