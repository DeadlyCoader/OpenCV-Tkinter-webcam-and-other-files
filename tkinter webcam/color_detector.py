import cv2 as cv


color_indexes = {"Red" : {
    1: [(0, 100, 100), (10, 255, 255)],
    2: [(170, 100, 100), (179, 255, 255)]
    },
    "Green": [(35, 90, 50), (85, 255, 255)],
    "Blue": [(100, 100, 100), (130, 255, 255)]}

def detectColor(img, color):
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    if color != "Red":
        mask = cv.inRange(hsv_img, color_indexes[color][0], color_indexes[color][1])
    else:
        mask1 = cv.inRange(hsv_img, color_indexes["Red"][1][0], color_indexes["Red"][1][1])
        mask2  = cv.inRange(hsv_img, color_indexes["Red"][2][0], color_indexes["Red"][2][1])
        mask = cv.bitwise_or(mask1, mask2)

    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv.contourArea(contour=contour)
        if area < 1000:
            continue
        x, y, w, h = cv.boundingRect(contour)
        cx = int(x + (w/2))
        cy = int(y + (h/2))
        img = cv.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), thickness=2)
        img = cv.circle(img, (cx, cy), 1, (0, 255, 0), thickness=1)
        img = cv.putText(img, f"({cx}, {cy})", (cx, cy+10), cv.FONT_HERSHEY_COMPLEX, 1, (0,255, 0), thickness=1)

    return img


def detectColors(img, color_indexes = color_indexes):
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    colors = list(color_indexes.keys())
    #for red
    red_mask1 = cv.inRange(hsv_img, color_indexes["Red"][1][0], color_indexes["Red"][1][1])
    red_mask2 = cv.inRange(hsv_img, color_indexes["Red"][2][0], color_indexes["Red"][2][1])
    
    red_mask = cv.bitwise_or(red_mask1, red_mask2)
    red_contours,_ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    blue_mask = cv.inRange(hsv_img, color_indexes["Blue"][0], color_indexes["Blue"][1])
    blue_contours,_ = cv.findContours(blue_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    green_mask = cv.inRange(hsv_img, color_indexes["Green"][0], color_indexes["Green"][1])
    green_contours,_ = cv.findContours(green_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    contours = (red_contours, green_contours, blue_contours)
    
    for i in range(len(colors)):
        for contour in contours[i]:
            area = cv.contourArea(contour = contour)
            if area <1000:
                continue
            x, y, w, h = cv.boundingRect(contour)
            cx = int(x+w/2)
            cy = int(y+h/2)
            img = cv.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), thickness = 2)
            img = cv.circle(img, (cx, cy), 1, (0, 255, 0), thickness = 1)
            img = cv.putText(img, f"{colors[i]}: ({cx}, {cy})", (cx, cy+10), cv.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), thickness=1)
    
    return img

if __name__ == "__main__":
    cam = cv.VideoCapture(0)
    
    while True:
        isTrue, frame = cam.read()
        if not isTrue:
            print("Camera closed or not working")
            continue
        frame = detectColors(frame, color_indexes)
        cv.imshow('Video', frame)
        if (cv.waitKey(1) & 0xFF) == ord('d'):
            break

    cam.release()
    cv.destroyAllWindows()
    