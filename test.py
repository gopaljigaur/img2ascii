import numpy as np
import cv2

cap = cv2.VideoCapture('example.mp4')

ret, frame = cap.read()
print('ret =', ret, 'W =', frame.shape[1], 'H =', frame.shape[0], 'channel =', frame.shape[2])


FPS= 20.0
FrameSize=(frame.shape[1], frame.shape[0])
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

out = cv2.VideoWriter('Video_output.avi', fourcc, FPS, FrameSize, 0)

while(cap.isOpened()):
    ret, frame = cap.read()

    # check for successfulness of cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = gray

    # Save the video
    out.write(frame)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break

cap.release()
out.release()
cv2.destroyAllWindows()