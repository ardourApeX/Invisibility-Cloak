import numpy as np
import cv2 as cv
import time

capture = cv.VideoCapture(0)

time.sleep(2) #Response time

background_image = 0 # Numpy array

# This one is to capture the background before overlaying an object
for i in range(50):
    bool_value, bg = capture.read()

while(capture.isOpened()):
    bool_value, frame = capture.read()

    if (not bool_value):
        break
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #  HSV = Hue Saturation Lightness
    
    # There are 2 ranges of red color
    # one is from 0 to 10
    red_lower = np.array([0, 120, 70]) 
    red_upper = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, red_lower, red_upper) # Separating the cloak part 

    # Another one is from 170 to 180
    red_lower = np.array([170, 120, 70])
    upper_lower = np.array([180, 255, 255]) # Again separating the cloak part
    mask2 = cv.inRange(hsv, red_lower, red_upper)

    # Operator Overloading
    mask1 = mask1 + mask2

    # Removing noise from the frame using morphology
    mask1 = cv.morphologyEx(mask1, cv.MORPH_OPEN, np.ones((3, 3), np.uint8),  iterations = 2)

    # Increasing the smoothness
    mask1 = cv.morphologyEx(mask1, cv.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations = 1)


    # Mask1 detects the red color
    # Now we are selecting all the pixels other than that red color
    mask2 = cv.bitwise_not(mask1) 
    
    result1 = cv.bitwise_and(bg, bg, mask = mask1)
    result2 = cv.bitwise_and(frame, frame, mask = mask2)

    final_frame = cv.addWeighted(result1, 1, result2, 1, 0)
    cv.imshow("Aaabra Ka Daabra ", final_frame)

    key_pressed = cv.waitKey(1) & 0xFF
	# There is no input function so when the key is pressed, it is interpreted as an ASCII value (accepted by waitKey(1))
	# & 0xFF is to convert it into a 8 bit character rather than 64 or 32 bit
    if key_pressed == ord('q'):
        break

capture.release()
cv.destroyAllWindows()