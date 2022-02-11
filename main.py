from curses.textpad import rectangle
from email.mime import image
import cv2 as cv
import numpy as np
import os
import logging
from random import randint


#variables
files = sorted(os.listdir('img1'))
dict = {}
dir = 'gt.txt'
rectangle_englobantes = []
new_path = "img2"
color_dict = {}
img_bounding_boxes = {}

#create temporary matrix to be used in the loop 
tmp_matrix = []
tmp_img1 = []
tmp_img2 = []


#populate dict with filenames for each picture
for i in range(len(files)):
	dict[i+1] = 'img1/'+files[i]

# populate rectangle_englobantes with all available bounding box informations
with open(dir) as d : 
    for line in d : 
        rectangle_englobantes.append(line.strip("\n").split(','))


#populate dict with list of bounding boxes for each picture 
for i in range(len(files)):
    for j in range(len(rectangle_englobantes)) : 
        if rectangle_englobantes[j][0] == str(i + 1) : 
            x1 = int(rectangle_englobantes[j][2])
            y1 = int(rectangle_englobantes[j][3])
            l1 = int(rectangle_englobantes[j][4])
            h1 = int(rectangle_englobantes[j][5])
            if h1 <= l1 : 
                if files[i] not in img_bounding_boxes : 
                    img_bounding_boxes[files[i]] = [(x1,y1,l1,h1)]
                else : 
                    img_bounding_boxes[files[i]] += [(x1,y1,l1,h1)]
	
# function for getting image from dict
def get_image(img_num)  :
    return cv.imread(dict[img_num])

# generate random color 
def generate_color() : 
    return [randint(0, 255), randint(0, 255), randint(0, 255)]

#create new folder for images
try:
    os.mkdir(new_path)
except OSError:
    logging.error('Failed to create path' + new_path)
else:
    logging.info("Succesfully created new path")
    

# initialize first image with rectangles

img = cv.imread(dict[int(rectangle_englobantes[0][0])])
counter = 0
for i in range(len(rectangle_englobantes)) :
    if rectangle_englobantes[i][0] == str(1):
        x1 = int(rectangle_englobantes[i][2])
        y1 = int(rectangle_englobantes[i][3])
        l1 = int(rectangle_englobantes[i][4])
        h1 = int(rectangle_englobantes[i][5])
        
        # check if height is greater then length -> verify with TA if this is the best way to do this
        if h1 <= l1 : 
            new_color = generate_color()
            cv.rectangle(img,(int(x1),int(y1+h1)), (int(x1+l1),int(y1)), new_color,3)
            color_dict[(1,x1,y1)] = new_color
    else : 
        break

cv.imwrite('img2/'+rectangle_englobantes[1][0]+'.jpg', img)









# curr = 1
# for i in range(0,len(rectangle_englobantes) - 1) :
    
#     continue


#img1 = cv.imread('img1/000001.jpg')
#img2 = cv.imread('img1/000002.jpg')

#cv.imwrite('img1.jpg',img1)
#cv.imwrite('img2.jpg',img2)


# curr = 0
# #matrice = []
# for i in range(len(rectangle_englobantes)) : 
#     x1 = int(rectangle_englobantes[i][2])
#     y1 = int(rectangle_englobantes[i][3])
#     l1 = int(rectangle_englobantes[i][4])
#     h1 = int(rectangle_englobantes[i][5])
#     if int (rectangle_englobantes[i][0]) == curr and h1 <= l1 :
#         cv.rectangle(img,(int(x1),int(y1+h1)), (int(x1+l1),int(y1)),(0,255,3))
#         cv.imwrite('foobar.jpg', img)
        




# y = 485
# x = 1376
# l = 37
# h = 28

#cv.imshow('Cropped_image',crp_img)
#cv.waitKey(0)
#cv.destroyAllWindows()