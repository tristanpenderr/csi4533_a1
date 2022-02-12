import cv2 as cv
import os
import logging
import pandas as pd
from random import randint


# log configuration
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

#variables
files = sorted(os.listdir('img1'))
dict = {}
dir = 'gt.txt'
rectangle_englobantes = []
new_path = "img2"
color_dict = {}
img_bounding_boxes = {}

#Object for a bounding
class Box(object):
    x1 = 0.
    x2 = 0.
    y1 = 0.
    y2 = 0.

   # constructor for our box 
    def __init__(self, x, y, l, h):
        #left
        self.x1 = x
        #right
        self.x2 = x + l
        #bottom
        self.y1 = y
        #top
        self.y2 = y + h

        self.area = h * l

        self.l1 = l
        self.h1 = h

# function to create a box
def make_box(x, y, l,h):
    box = Box(x, y, l , h)
    return box
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
            if h1 <= l1 and files[i] not in img_bounding_boxes : 
                img_bounding_boxes[files[i]] = [make_box(x1,y1,l1,h1)]
            elif h1 <= l1: 
                img_bounding_boxes[files[i]] += [make_box(x1,y1,l1,h1)]
            elif files[i] not in img_bounding_boxes :
                img_bounding_boxes[files[i]] = []
                
# function for getting image from dict
def get_image(img_num)  :
    return cv.imread(dict[img_num])

# generate random color 
def generate_color() : 
    return [randint(0, 255), randint(0, 255), randint(0, 255)]



def calculate_iou(box1, box2):
    x1, y1 = max(box1.x1,box2.x1), max(box1.y1,box2.y1)
    x2, y2 = min(box1.x2, box2.x2), min(box1.y2, box2.y2)

    overlap = 0

    if x2-x1 > 0 and y2-y1 > 0 : 
        overlap = (x2-x1) * (y2-y1)
    
    combined = box1.area + box2.area - overlap

    iou = overlap/combined

    if iou < 0.4 : 
         return 0

    return iou


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



#begin iou calculations 
for i in range(len(files) - 1) :

    column = []
    # hold file names for images to examine
    img1 = files[i]
    img2 = files[i + 1]


    img = cv.imread('img1/'+img2)
    # get bounding box information
    box_list1 = img_bounding_boxes[img1]
    box_list2 = img_bounding_boxes[img2]
    # cycle through bounding boxes for f(x) and f(x + 1)
    for b in range(len(box_list1)) :
        row = []
        for k in range(len(box_list2)) :
            max_index = -1

            iou = calculate_iou(box_list1[b],box_list2[k])
            row.append(iou)
        max_value = max(row)
        max_index = row.index(max_value)
        row[~max_index] = 0        
        column.append(row)

    # find max column
    max_column = []

    for j in range(len(box_list2)) :
        max_column.append((0, -1, -1)) 

    for j in range(len(column)) :
        for k in range(len(column[j])) : 
            val, c, r = max_column[k]
            if column[j][k] > val : 
                max_column[k] = (column[j][k],j, k)
    for j in max_column : 
        val, c, r = j 
        column[c][r] = -1
        column[~c][r] = 0
    
    for j in range(len(column)) : 
        if -1 not in column[j] : 
            new_color = generate_color()
            x1 = box_list2[j].x1
            y1 = box_list2[j].y1
            l1 = box_list2[j].l1
            h1 = box_list2[j].h1


        else : 
            x1 = box_list2[j].x1
            y1 = box_list2[j].y1
            l1 = box_list2[j].l1
            h1 = box_list2[j].h1

            orig = box_list1[j]
            
            new_color = color_dict[(i+1,orig.x1, orig.y1)]
            cv.rectangle(img,(int(x1),int(y1+h1)), (int(x1+l1),int(y1)), new_color,3)
            color_dict[(i+2,x1,y1)] = new_color
            
    # for j in range(len(box_list2)) : 
    #     if -1 not in column[j] : 
    #         new_color = generate_color()
    #         x1 = box_list2[j].x1
    #         y1 = box_list2[j].y1
    #         l1 = box_list2[j].l1
    #         h1 = box_list2[j].h1
    #         cv.rectangle(img,(int(x1),int(y1+h1)), (int(x1+l1),int(y1)), new_color,3)
    #         color_dict[(i+2,x1,y1)] = new_color
    #     else : 
    #         x1 = box_list2[j].x1
    #         y1 = box_list2[j].y1
    #         l1 = box_list2[j].l1
    #         h1 = box_list2[j].h1

    #         orig = box_list1[j]
            
    #         new_color = color_dict[(i+1,orig.x1, orig.y1)]
    #         cv.rectangle(img,(int(x1),int(y1+h1)), (int(x1+l1),int(y1)), new_color,3)
    #         color_dict[(i+2,x1,y1)] = new_color
    
    cv.imwrite('img2/'+img2, img)
    
    
    



            

print(calculate_iou(img_bounding_boxes['000001.jpg'][0],img_bounding_boxes['000001.jpg'][0]))


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