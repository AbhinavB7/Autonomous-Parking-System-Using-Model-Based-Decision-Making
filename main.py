
from algorithm.parking_car import ParkingCarRRT
from map.map import ParkingMap
from algorithm.basic_rrt import BasicRRT
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt

import cv2
import random

random_number = random.randint(0, 3)
random_number =3

print(random_number)

if random_number == 0 :
    point = (125, 125)
elif random_number ==1 :
    point =  (125,225)
elif random_number ==2:
    point = (365,270)
else :
    point = (824,799)



my_map = ParkingMap((50, 50), (480, 350), point)

# rrt = BasicRRT(my_map,20)

try:
    rrt = ParkingCarRRT(my_map,20)
finally:
    rrt = ParkingCarRRT(my_map,20)








