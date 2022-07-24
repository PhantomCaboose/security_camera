import cv2, os, time, datetime

class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GREY = '\033[37m'
    WHITE = '\033[0m'
    UNDERLINE = '\033[4m'
    RESET = WHITE

if not os.path.exists('videos'):
    os.makedirs('videos')


capture = cv2.VideoCapture(3)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
detection = False
frame_size = (int(capture.get(3)), int(capture.get(4)))
four_char_code = cv2.VideoWriter_fourcc(*"mp4v")
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

while True:
    _, frame = capture.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.3, 5)
    bodies = body_cascade.detectMultiScale(grey, 1.3, 5)
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            output = cv2.VideoWriter(f"videos/{current_time}.mp4", four_char_code, 20.0, frame_size)
            print(f"{Style.GREEN}Started recording!{Style.RESET}")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                output.release()
                print(f"{Style.RED}Stopped recording!{Style.RESET}")
        else:
            timer_started = True
            detection_stopped_time = time.time()
    if detection:
        output.write(frame)
    #cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
output.release()
capture.release()
cv2.destroyAllWindows()
