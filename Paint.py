import cv2 as cv
import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd


height = 700
width = 1600


ui = tk.Tk()
ui.title("JaadogarChhipcali")
ui.geometry(f"{width}x{height}")


file_types = [("Image", "*.jpg"),
            ("Image", "*.jpeg"),
            ("Image", "*.png")]
file_path = ""
file_selected = False
display_img = ""

current_image_status = {0: ""}
current_img_id = 0
current_image = ""


rectangle_tool = False
pencil_tool = False




leftClicked = False
clickReleased = False
left_click_location = (0,0)
cursor_coordinates = (0,0)


header_frame = tk.Frame(ui, width=width, height=100, bg = 'White')
header_frame.place(x=0, y=0)

work_frame = tk.Frame(ui, width=width, height=height-100, bg = 'White')
work_frame.place(x=0, y=100)

tool_frame = tk.Frame(ui, width = 500, height = 100, bg = 'Gray')
tool_frame.place(x=800, y = 0)

def BGR2RGB(bgr_img):
    rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
    return rgb_img
def RGB2BGR(rgb_img):
    bgr_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2BGR)
    return bgr_img
def get_imgDimensins(img):
    img_height = img.shape[0]
    img_width = img.shape[1]
    return (img_height, img_width)
def img_resize(img, dimensions):
    resized_img = cv.resize(img, dimensions)
    return resized_img
def img_read(file_path):
    img = cv.imread(file_path)
    return img

def get_cursor_position(event):
    global cursor_coordinates
    cursor_coordinates = (event.x, event.y)
def onLeftClick(event):
    global leftClicked
    global left_click_location
    leftClicked = True
    left_click_location = (event.x, event.y)
def onLeftRelease(event):
    global clickReleased
    clickReleased = True
    

def CONVERT_TO_TKIMG(img):
    global display_img
    img_height, img_width = get_imgDimensins(img)
    max_width = width
    max_height = height-100
    scale = min(max_width / img_width,
                max_height / img_height,
                1)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
     
    resized_img = img_resize(img, (new_width, new_height))
    display_img = resized_img
    
    rgb_img = BGR2RGB(resized_img)
    pil_img = Image.fromarray(rgb_img)
    tk_img = ImageTk.PhotoImage(pil_img)
    return tk_img

def show_in_window(tk_img):
    image_label.config(image=tk_img)
    img_dimensions = get_imgDimensins(display_img)
    image_label.image = tk_img
    image_label.place(x=(((width-img_dimensions[1])//2)-100), y = ((height-100-img_dimensions[0])//2))


def open_file():
    global file_path
    global file_selected
    global current_image
    file_path = fd.askopenfilename(title="Select file", filetypes=file_types)
    if file_path:
        file_selected = True
        img = img_read(file_path)
        current_image_status[current_img_id] = img
        current_image = img
        update()

    else:
        file_selected = False

def make_rectangle(img, start_point, end_point, color, thickness=2):
    img = cv.rectangle(img, (start_point), (end_point), color=color, thickness=thickness)
    return img

def draw(img, start_point, end_point, color, thickness = 2):
    copy_img = img.copy()
    # img = cv.circle(img, coordinates, radius=thickness, color=color, thickness=thickness)
    copy_img = cv.line(copy_img, start_point, end_point, color, thickness=thickness)
    return copy_img

def update():
    global current_image
    global current_img_id
    global leftClicked
    global clickReleased
    global left_click_location
    global cursor_coordinates
    #cv.imshow(f"Current Image{current_img_id}", current_image_status[current_img_id])
    editing_image = current_image_status[current_img_id].copy()
    # current_image = current_image_status[current_img_id]
    if rectangle_tool:
        if leftClicked:
            current_image = make_rectangle(editing_image, left_click_location, cursor_coordinates, (255, 255, 255))
            if clickReleased:
                print("released")
                leftClicked = False
                clickReleased = False
                current_image_status[current_img_id+1] = current_image.copy()
                current_img_id +=1
    if pencil_tool:
        if leftClicked:
            current_image = draw(current_image, left_click_location, cursor_coordinates, (255, 255, 255))
            if clickReleased:
                print("released")
                leftClicked = False
                clickReleased = False
                current_image_status[current_img_id+1] = current_image.copy()
                current_img_id +=1
        left_click_location = cursor_coordinates
                
    tk_img = CONVERT_TO_TKIMG(current_image)
    show_in_window(tk_img)
    # current_image = current_image_status[current_img_id]

    ui.after(5, update)

def undo():
    global current_img_id, current_image
    if not (current_img_id-1 < 0):
        current_img_id -= 1
    print(current_img_id)
    current_image = current_image_status[current_img_id]
def redo():
    global current_img_id, current_image
    ids = current_image_status.keys()
    if not (current_img_id+1 > max(ids)):
        current_img_id += 1
    print(current_img_id)
    current_image = current_image_status[current_img_id]

def all_tool_false():
    global rectangle_tool
    global pencil_tool
    rectangle_tool = False
    pencil_tool = False


def rectangle():
    global rectangle_tool
    print("rectangle tool activated")
    if rectangle_tool:
        rectangle_tool = False
    else:
        all_tool_false()
        rectangle_tool = not rectangle_tool
    image_label.bind("<Motion>", get_cursor_position)
    image_label.bind("<Button-1>", onLeftClick)
    image_label.bind("<ButtonRelease-1>", onLeftRelease)

def pencil():
    global pencil_tool
    print("activated pencil tool")
    if pencil_tool:
        pencil_tool = False
    else:
        all_tool_false()
        pencil_tool = not pencil_tool
    image_label.bind("<Motion>", get_cursor_position)
    image_label.bind("<Button-1>", onLeftClick)
    image_label.bind("<ButtonRelease-1>", onLeftRelease)


open_button = tk.Button(header_frame, text="File", command=open_file)
open_button.place(x=10,y=10)

undo_button = tk.Button(header_frame, text = "Undo", command = undo)
undo_button.place(x=50, y=10)

redo_button = tk.Button(header_frame, text = "Redo", command = redo)
redo_button.place(x=100, y=10)

image_label = tk.Label(work_frame)
image_label.place(x=0, y=0)

pencil_button = tk.Button(tool_frame, text = "Pencil", command = pencil)
pencil_button.place(x=30, y=10)

rectangle_button = tk.Button(tool_frame, text="▭", command=rectangle)
rectangle_button.place(x=5,y=10)

ui.mainloop()