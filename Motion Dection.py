import cv2

#making a object to capture video from camera
video = cv2.VideoCapture(0)

frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)
out = cv2.VideoWriter("demo1.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10, size)
print(video)

while video.isOpened():
    #to breake while loop when presed 'q'
    if cv2.waitKey(1) == ord('q'):
        break

    #making 2 object to compare
    check, frame1 = video.read()
    check, frame2 = video.read()
    
    #if failes to take video it will break
    if not check:
        break
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    out.write(frame2)
    cv2.imshow("frame", frame1)

video.release()
out.release()
cv2.destroyAllWindows()
