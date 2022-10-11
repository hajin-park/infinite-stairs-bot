import cv2
import os
from dataclasses import dataclass


@dataclass
class Images:

    #   Initialize images
    start_screen_img  = cv2.imread(os.getcwd() + '\\assets\start_screen.png' , cv2.IMREAD_UNCHANGED)
    stop_screen_1_img = cv2.imread(os.getcwd() + '\\assets\stop_screen_1.png', cv2.IMREAD_UNCHANGED)
    stop_screen_2_img = cv2.imread(os.getcwd() + '\\assets\stop_screen_2.png', cv2.IMREAD_UNCHANGED)
    stop_screen_3_img = cv2.imread(os.getcwd() + '\\assets\stop_screen_3.png', cv2.IMREAD_UNCHANGED)
    default_stair_img = cv2.imread(os.getcwd() + '\\assets\purple_stair.png' , cv2.IMREAD_UNCHANGED)
    gold_stair_img    = cv2.imread(os.getcwd() + '\\assets\gold_stair.png'   , cv2.IMREAD_UNCHANGED)
    gem_stair_img     = cv2.imread(os.getcwd() + '\\assets\gem_stair.png'    , cv2.IMREAD_UNCHANGED)
    large_coin_img    = cv2.imread(os.getcwd() + '\\assets\large_coin.png'   , cv2.IMREAD_UNCHANGED)

    #   Group images in lists
    start_images = [start_screen_img]
    stop_images  = [stop_screen_1_img, 
                   stop_screen_2_img, 
                   stop_screen_3_img]
    stair_images = [default_stair_img, 
                    gold_stair_img, 
                    gem_stair_img,
                    large_coin_img]
