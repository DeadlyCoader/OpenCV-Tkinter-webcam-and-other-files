import cv2 as cv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import color_detector
import motion_detector

width = 500
height = 500
ui = tk.Tk()
ui.title("Webcam")
ui.geometry(f"{width+20}x{height+200}")

cam_frame = tk.Frame(ui, width = width, height =height, bg = "White")
cam_frame.pack()
cam = cv.VideoCapture(0)

paused = False
grayed = False
save_img = False
count_start = False
counter_start_time = 0
count_till = 10

disco_start = False
color_change_time = 0
detect_edges = False
current_brightness = 100

crop_start = False
leftClicked = False
clickReleased = False
left_click_location = (0,0)
cursor_coodinates = (0,0)

detect_colors = False
colors = ["All", "Red", "Green", "Blue"]
color_to_detect = ""

detect_motion = False
previous_frame = ""

def get_cursor_position(event):
    global cursor_coodinates
    cursor_coodinates = (event.x, event.y)
def onLeftClick(event):
    global left_click_location
    global leftClicked
    leftClicked = True
    left_click_location = (event.x, event.y)
def onLeftRelease(event):
    global clickReleased
    clickReleased = True


def BGR2RGB(frame):
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    return rgb_frame
def RGB2BGR(frame):
    bgr_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    return bgr_frame
def webcam():
    isTrue, bgr_frame = cam.read()
    if not isTrue:
        print("Stream end")
        return None, None

    rgb_frame = BGR2RGB(bgr_frame)
    return rgb_frame, bgr_frame

def CAM2GRAY(bgr_frame):
#     _, bgr_frame = webcam()
    gray_frame = cv.cvtColor(bgr_frame, cv.COLOR_BGR2GRAY)
    return gray_frame

def ClickPhoto(frame):
    current_time = time.time()
    cv.imwrite(f"{current_time}.jpg", frame)

def DiscoColor(color_channel, frame):
    frame[:, :, color_channel] = frame[:,:, color_channel] *0.3
    return frame

def EdgeDetector(frame):
    frame = cv.Canny(CAM2GRAY(frame), 70, 200)
    # frame = BGR2RGB(frame)
    return frame

def counter(i, rgb_frame):
    #_, bgr_frame = webcam()
    bgr_frame = RGB2BGR(rgb_frame)
    font = cv.FONT_HERSHEY_COMPLEX
    fontScale = 3
    thickness = 2
    color = (255,0,0)
    cv.putText(
        bgr_frame, 
        text=f"{i}",
        org=(int(width/2), int(height/2)),
        fontFace = font, 
        fontScale=fontScale,
        color=color, 
        thickness=thickness
        )
    rgb_frame = BGR2RGB(bgr_frame)
    return rgb_frame

def make_rectangle(frame, start_point, end_point, color = (255, 255, 255)):
    frame = cv.rectangle(frame, (start_point), (end_point), color, thickness=1)
    return frame

def update():
    global grayed
    global save_img
    global count_start
    global current_brightness
    global crop_start
    global previous_frame
    current_frame,bgr_frame = webcam()
    if grayed:
        current_frame = CAM2GRAY(bgr_frame)

    if disco_start:
        if grayed:
            grayed = False
        global color_change_time
        disco_current_time = time.time()
        if disco_current_time - color_change_time < 0.5:
            current_frame = DiscoColor(0, bgr_frame)
        elif disco_current_time - color_change_time < 1:
            current_frame = DiscoColor(1, bgr_frame)
        elif disco_current_time - color_change_time < 1.5:
            current_frame = DiscoColor(2, bgr_frame)
        else:
            color_change_time = time.time()

    if detect_edges:
        current_frame = EdgeDetector(current_frame)

    if crop_start:
        global left_click_location
        global cursor_coodinates
        global clickReleased
        global leftClicked
        if leftClicked:
            if left_click_location == cursor_coodinates:
                if not left_click_location == (0,0):
                    left_click_location = cursor_coodinates
            else:
                current_frame = make_rectangle(current_frame, (left_click_location), cursor_coodinates)
                if clickReleased:
                    x1, y1 = left_click_location[0], left_click_location[1]
                    x2, y2 = cursor_coodinates[0], cursor_coodinates[1]
                    cropped_frame = current_frame[y1:y2, x1:x2]
                    if grayed:
                        ClickPhoto(cropped_frame)
                    else:    
                        cropped_frame = RGB2BGR(cropped_frame)
                        ClickPhoto(cropped_frame)
                    
                    crop_start = False
                    clickReleased = False
                    leftClicked = False

    if count_start:
        current_time = time.time()
        global count_till
        global counter_start_time
        if current_time - counter_start_time < 1:
            current_frame = counter(count_till, current_frame)
        else:
            count_till -= 1
            counter_start_time = time.time()

        if count_till <=0:
            count_start = False
            count_till = 10
            if not grayed:
                photo = RGB2BGR(current_frame)
                ClickPhoto(photo)
            else:
                ClickPhoto(current_frame)

    if detect_colors:
        bgr_img = RGB2BGR(current_frame)
        if color_to_detect != "All":
            detected_color_img = color_detector.detectColor(bgr_img, color_to_detect)
        else:
            detected_color_img = color_detector.detectColors(bgr_img)
        current_frame = BGR2RGB(detected_color_img)
        
    if detect_motion:
        # previous_gray_frame = CAM2GRAY(previous_frame)
        # current_gray_frame = CAM2GRAY(bgr_frame)
        motion_difference_frame, motionStatus = motion_detector.detectMotion(previous_frame=previous_frame, current_frame=bgr_frame)
        current_frame = BGR2RGB(motion_difference_frame)
        current_frame = cv.putText(current_frame, f"Motion: {motionStatus}", (50, 50), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), thickness=1)
        
    if save_img == True:
        save_img = False
        current_time = time.time()
        print(current_time)
        if not grayed:
            ClickPhoto(BGR2RGB(current_frame))
        else:
            ClickPhoto(current_frame)
        print("Image Saved")                

    current_frame = cv.convertScaleAbs(current_frame, alpha=1.0, beta =brightness_slider.get())

    pil_frame = Image.fromarray(current_frame)
    tk_frame = ImageTk.PhotoImage(pil_frame)

    webcamLabel.config(image = tk_frame)
    webcamLabel.image = tk_frame
    webcamLabel.grid(row = 0, column = 0, padx = 0, pady = 0)

    previous_frame = bgr_frame
    if not paused:
        ui.after(44, update)
    
def pause():
    global paused
    if not paused:
        paused = True
    else:
        paused = False
    print(paused)
def start():
    global paused 
    paused = False
    update()
def gray():
    global grayed
    if not grayed:
        grayed = True
    else:
        grayed = False
def save():
    global save_img
    print(save_img)
    save_img = True
def countdown():
    global count_start
    global counter_start_time
    counter_start_time = time.time()
    count_start = True
    
def disco():
    global disco_start
    global color_change_time
    if not disco_start:
        disco_start = True
        color_change_time = time.time()
    else:
        disco_start = False 

def edge_detection_mode():
    global detect_edges
    if not detect_edges:
        detect_edges = True
    else:
        detect_edges = False

def color_detection_mode():
    global detect_colors
    global color_to_detect
    detect_colors = not detect_colors
    color_to_detect = color_combobox.get()
    print(color_to_detect)

def motion_detection_mode():
    global detect_motion
    detect_motion = not detect_motion

def crop():
    global crop_start
    crop_start = True
    webcamLabel.bind("<Motion>", get_cursor_position)
    webcamLabel.bind("<Button-1>", onLeftClick)
    webcamLabel.bind("<ButtonRelease-1>", onLeftRelease)

    # crop_start_coordinates = (start_x, start_y)

webcamLabel = tk.Label(cam_frame)
webcamLabel.grid(row = 0, column = 0, padx = 0, pady = 0)

x = 500
y = 550
pause_button = tk.Button(ui, text = "Pause Camera", command = pause)
pause_button.place(x=x, y=y)

start_button = tk.Button(ui, text = "Start Stream", command = start)
start_button.place(x=x+100, y=y)

gray_button = tk.Button(ui, text = "Turn Gray", command = gray)
gray_button.place(x=x+200, y=y)

save_button = tk.Button(ui, text = "Save", command = save)
save_button.place(x=x+300, y =y)

counter_button = tk.Button(ui, text = "Timer", command = countdown)
counter_button.place(x=x, y = y+50)

disco_button = tk.Button(ui, text = "Disco", command = disco)
disco_button.place(x=x+50, y = y+50)

edge_detection_button = tk.Button(ui, text = "Detect Edges", command = edge_detection_mode)
edge_detection_button.place(x = x+100, y = y+50)

crop_button = tk.Button(ui, text = "Crop", command = crop)
crop_button.place(x = x+200, y = y+50)

color_detection_button = tk.Button(ui, text = "Detect Color", command = color_detection_mode)
color_detection_button.place(x = x+250, y = y+50)

motion_detection_button = tk.Button(ui, text = "Detect Motion", command = motion_detection_mode)
motion_detection_button.place(x = x, y=y+100)

color_combobox = ttk.Combobox(ui, values = colors, state = "randomly")
color_combobox.set(colors[0])
color_combobox.place(x=x+350, y=y+50)

brightness_label = tk.Label(ui, text= "Bightness Level")
brightness_label.place(x=x+550, y = y-520)

brightness_slider = tk.Scale(ui, from_ = -100, to = 100, orient = 'horizontal', length = 300)
brightness_slider.set(0)
brightness_slider.place(x = x+550, y=y-500)

ui.mainloop()

