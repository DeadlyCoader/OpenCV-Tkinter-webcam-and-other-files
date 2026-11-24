import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd


detectorUi = tk.Tk()
height = 500
width = 500

detectorUi.geometry(f"{width+100}x{height+100}")
detectorUi.title("Color Detector")

imageFrame = tk.Frame(detectorUi, width = width, height = height, bg = "White")
imageFrame.pack()

file_types = [("Images", "*.jpg"),
              ("Images", "*.png"),
              ("Images", "*.jpeg")]
file_path = ""
file_selected = False
img = ""


def BGR2RGB(bgr_img):
    rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
    return rgb_img
def RGB2BGR(rgb_img):
    bgr_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2BGR)
    return bgr_img

def resize(img, dimensions = (400, 400)):
    img = cv.resize(img, dimensions, interpolation=cv.INTER_AREA)
    return img
def display_image(img):
    img = RGB2BGR(img)
    pil_img = Image.fromarray(img)
    tk_img = ImageTk.PhotoImage(pil_img)
    imageLabel.config(image = tk_img)
    imageLabel.image = tk_img
    imageLabel.pack()

def select_image():
    global file_path
    global file_selected
    global img
    global file_types
    file_path = fd.askopenfilename(title = "Select Image", filetypes = file_types)
    if file_path:
        file_selected = True
        img = cv.imread(file_path)
        img = resize(img=img)
        display_image(img)
    else:
        file_selected = False

def detect_color():
    global img
    if file_selected:
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_red1 = (0, 100, 100)
        upper_red1 = (10, 255, 255)
    
        lower_red2 = (170, 100, 100)
        upper_red2 = (179, 255, 255)
    
        mask1 = cv.inRange(hsv_img, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv_img, lower_red2, upper_red2)
        mask = cv.bitwise_or(mask1, mask2)
        result_img = cv.bitwise_and(img, img, mask=mask)
        cv.imshow("Detected Color", result_img)

        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            img = cv.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), thickness=1)
        cv.imshow("Detected", img)

    else:
        print("Please select an image") 


imageLabel = tk.Label(imageFrame)
imageLabel.pack()

selectButton = tk.Button(detectorUi, text = "Select Image", command = select_image)
selectButton.pack()

detectButton = tk.Button(detectorUi, text = "Detect", command = detect_color)
detectButton.pack()

detectorUi.mainloop()