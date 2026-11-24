import cv2 as cv
import time


def detectMotion(previous_frame, current_frame):
    motionStatus = False
    previous_gray_frame = cv.cvtColor(previous_frame, cv.COLOR_BGR2GRAY)
    current_gray_frame = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
    frame_difference = cv.absdiff(previous_gray_frame, current_gray_frame)
    # frame_difference = cv.cvtColor(frame_difference, cv.COLOR_BGR2GRAY)
    
    threshold_value, threshold_frame = cv.threshold(frame_difference, 40, 255, cv.THRESH_BINARY)
    
    contours, hierarchy = cv.findContours(threshold_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area < 500:
            continue
        motionStatus = True
        x, y, w, h = cv.boundingRect(contour)
        cx = x+w//2
        cy = y+h//2
        current_frame = cv.rectangle(current_frame, (x, y), (x+w, y+h), (255, 0, 0), thickness=1)
        current_frame = cv.circle(current_frame, (cx, cy), 1, (255, 0, 0), thickness=1)
        current_frame = cv.putText(current_frame, f"({cx}, {cy})", (cx+10, cy), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), thickness=1)
    return current_frame, motionStatus


background_subtractor = cv.createBackgroundSubtractorMOG2()
def background_model_motion_detector(current_frame):
    foreground_mask = background_subtractor.apply(current_frame)
    return foreground_mask
    
if __name__ == "__main__":
    cam = cv.VideoCapture(0)
    while True:
        isTrue, frame = cam.read()
        if not isTrue:
            break
        frame = background_model_motion_detector(frame)
        cv.imshow('Motion detector', frame)
        if (cv.waitKey(1) & 0xFF) == ord('d'):
            break