import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import cv2 as cv

root = tk.Tk()
root.withdraw()  # Hide the main window

ImageWindow = tk.Tk()
ImageWindow.title("Image Window")
ImageWindow.geometry("800x500")
print("Image Window created successfully.")

file_types = [("Images", "*.jpg"),
              ("Images", "*png"),
              ("Images", "*jpeg")]
file_path = ""

Image_frame = tk.Frame(ImageWindow, width = 800, height = 400, bg = "Black")
Button_frame = tk.Frame(ImageWindow, width = 800, height = 100, bg = "White")
Image_frame.pack()
Button_frame.pack()


class image_processing:
    def __init__(self, file_path):
        self.file_path = file_path

    def img_read(self, file_path):
        img = cv.imread(file_path)
        return img
    
    def resize(self, img, dimensions):
        img = cv.resize(img, dimensions, interpolation = cv.INTER_AREA)
        return img
    
    def tk_img_read(self, img):
        pil_image = Image.fromarray(img)
        # tk_img = ImageTk.PhotoImage(pil_image, master = ImageWindow)
        return pil_image

    def grey(self, img):
        grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return grey_img


class image_display:
    def __init__(self):
        self.image_object = image_processing(file_path)

    def select_image(self):
        global file_path
        file_path = fd.askopenfilename(title = "Select Image", filetypes = file_types)
        if file_path:
            print(f"Image Selected: {file_path}")
        else:
            print("No Image Selected")

    def display_image(self, img, column = 0):
        resizeImg = self.image_object.resize(img, (400, 400))

        tkImg = self.image_object.tk_img_read(resizeImg)
        tk_img = ImageTk.PhotoImage(tkImg , master  = ImageWindow)

        label = tk.Label(Image_frame, image = tk_img)
        label.image = tk_img
        label.grid(row = 0, column=column, padx = 10, pady=0)

def select_and_display():
    image_selection = image_display()
    image_selection.select_image()

    image_process = image_processing(file_path)
    img = image_process.img_read(file_path)
    image_selection.display_image(img, column = 0)

def grey():
    image_process = image_processing(file_path)
    image_selection = image_display()
    img = image_process.img_read(file_path)
    img = image_process.resize(img, (400, 400))
    img = image_process.grey(img)

    image_selection.display_image(img, column = 1)


tK_SelectButton = tk.Button(Button_frame, text="Select Image", command = select_and_display)
tK_SelectButton.grid(row = 0 , column = 0, padx = 10, pady = 10)

tk_greyButton = tk.Button(Button_frame, text = "Convert to Grey", command = grey)
tk_greyButton.grid(row = 0, column = 1, padx = 10, pady = 10)




ImageWindow.mainloop()