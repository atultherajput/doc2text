from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re

def get_pan(filename):
    filename = filename
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray,3)

    temp_filename = "{}.png".format(os.getpid())
    cv2.imwrite(temp_filename, gray)

    text = pytesseract.image_to_string(Image.open(temp_filename))
    os.remove(temp_filename)

    with open(filename+'.txt', "w") as my_log:
        my_log.write(text)
    fr = open(filename+'.txt', 'r')
    data = []
    for line in fr:
        line=line.rstrip()
        if line is not '':
            data.append(line)
    name = data[1]
    f_name = data[2]
    dob = data[3]
    dob = dob.replace(" ", "")
    pan = data[5]
    pan = pan.replace(" ", "")
    return(name, f_name, dob, pan)

#print(get_pan('pan.jpg'))