import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import time

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

def CAM2GRAY():
    _, bgr_frame = webcam()
    gray_frame = cv.cvtColor(bgr_frame, cv.COLOR_BGR2GRAY)
    
    return gray_frame

def ClickPhoto(frame):
    current_time = time.time()
    cv.imwrite(f"{current_time}.jpg", frame)

def DiscoColor(color_channel, frame):
    frame[:, :, color_channel] = frame[:,:, color_channel] *0.3
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

def update():
    global grayed
    global save_img
    global count_start
    if not grayed:
        current_frame,bgr_frame = webcam()
    else:
        current_frame = CAM2GRAY()
    if save_img == True:
        save_img = False
        current_time = time.time()
        print(current_time)
        if not grayed:
            ClickPhoto(bgr_frame)
        else:
            ClickPhoto(current_frame)
        print("Image Saved")

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

                

    pil_frame = Image.fromarray(current_frame)
    tk_frame = ImageTk.PhotoImage(pil_frame)

    webcamLabel = tk.Label(cam_frame, image = tk_frame)
    webcamLabel.image = tk_frame
    webcamLabel.grid(row = 0, column = 0, padx = 0, pady = 0)

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

ui.mainloop()