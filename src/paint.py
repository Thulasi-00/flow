

# Libraries
import cv2
import numpy as np

# 2) Painting with identified object's color

# Load saved file that contain hsv ranges ('hsvVal.npy')
hsvVal = np.load('hsvVal.npy')

# Show shortcuts information
print("\n 2) Painting with identified object's color \n")
print("'hsvVal.npy' loaded")
print("Painting ready\n")
print("#####################################")
print("# Press 'q' to exit the program     #")
print("#####################################")
print("\n")

# Get minimum and maximum ranges from file
minRange = hsvVal[0]
maxRange = hsvVal[1]

# Initializing the webcam
cap = cv2.VideoCapture(1)         # 0, 1, 2, ... webcam port number
cap.set(3,720)                    # width of camera
cap.set(4,480)                    # height of camera

# BGR colors to painting
colorBlue = (255, 134, 58)
colorYellow = (11, 190, 255)
colorPink = (110, 0, 255)
colorGreen = (0 ,255, 36)
colorPurple = (236, 56, 131)
colorScreenCleaner = (7, 86, 251)
colorEraser = (7, 86, 251)

# Thickness of colors's boxes
thicknessBlue = 6
thicknessYellow = 2
thicknessPink = 2
thicknessGreen = 2
thicknessPurple = 2

# Thickness of marker's thicknesses boxes
thicknessSmall = 4
thicknessMedium = 1
thicknessLarge = 1

# Thickness of eraser
thicknessEraser = 1

# Default values for marker
color = colorBlue                # Set default marker's color is blue
thickness = 3                    # Set default marker's thickness is small

# Create x, y top coordinates of marker that identified first
# Top and middle coordinates of tracking object area is tip of marker
# like a pencil tip to painting
x1 = None
y1 = None

# Create canvas window to see painting without webcam
canvas = None

# Get width and height to put painting tools
ret, frame = cap.read()
h, w, c = frame.shape

# Showing webcam and painting on it in a loop
while True:
    # Read from webcam frame by frame.
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally (That makes mirror effect).
    frame = cv2.flip(frame, 1)
    
    # Convert to BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # If canvas empty show black screen
    if canvas is None:
        canvas = np.zeros(frame.shape, dtype=np.uint8)
    
    # -------------------------- <top-section> --------------------------
    # Put screen cleaner box
    # Uncomment if want to make visible rectange of cleaner
    # cv2.rectangle(frame, (0,0), (100,50), colorScreenCleaner, 0)
    cv2.putText(frame, 'Clear', (15,35), 5, 1, colorScreenCleaner, 1,
                cv2.LINE_AA)
    
    # Put eraser
    # Uncomment if want to make visible rectange of eraser
    # cv2.rectangle(frame, (100,0), (200,50), colorEraser, 0)
    cv2.putText(frame, 'Eraser', (110,35), 5, 1, colorEraser, thicknessEraser, 
                cv2.LINE_AA)
    
    # Put colors boxes
    cv2.rectangle(frame, (w-3,5), (w-53,55), colorYellow, thicknessYellow)
    cv2.rectangle(frame, (w-58,5),(w-108,55), colorPink, thicknessPink)
    cv2.rectangle(frame, (w-113,5), (w-163,55), colorGreen, thicknessGreen)
    cv2.rectangle(frame, (w-168,5), (w-218,55), colorBlue, thicknessBlue)
    cv2.rectangle(frame, (w-223,5), (w-273,55), colorPurple, thicknessPurple)
    
    # Put thickness boxes
    cv2.rectangle(frame, (w-352,5), (w-402,55), (0,0,0), thicknessLarge)
    cv2.circle(frame, (w-377,30), 11, (0,0,0), -1)
    cv2.rectangle(frame, (w-402,5), (w-452,55), (0,0,0), thicknessMedium)
    cv2.circle(frame, (w-427,30), 7, (0,0,0), -1)
    cv2.rectangle(frame, (w-452,5), (w-502,55), (0,0,0), thicknessSmall)
    cv2.circle(frame, (w-477,30), 3, (0,0,0), -1)
    # ------------------------- </top-section> --------------------------
    
    # Create mask with adjusted ranges
    mask = cv2.inRange(hsv, minRange, maxRange)
    
    # Perform filter operations to get rid of the noise
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.medianBlur(mask, 13)
    
    # Find contours
    contours, hierarchy = cv2.findContours(mask,
    cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    
    for c in contours:
        # Assign contour area to area
        area = cv2.contourArea(c)
        
        # Check contour area size
        # 1000 is enough used object, can be changed to draw more smoothly
        if area > 1000:
            # Get x, y coordinate and width, height rate of contour
            # y2 gives y coordinate of marker's tip
            x, y2, wc, hc = cv2.boundingRect(c)
            
            # x coordinate of marker's tip 
            x2 = x + wc//2
            
            # Show area lines
            cv2.rectangle(frame, (x,y2), (x+wc,y2+hc), color, 2)
            
            # If object trackable
            if x1 is not None:
                
                # If marker's tip coordinates on yellow box set color yellow
                if w-53 < x2 < w-3 and 5 < y2 < 55:
                    color = colorYellow
                    thicknessBlue = 2
                    thicknessYellow = 6
                    thicknessPink = 2
                    thicknessGreen = 2
                    thicknessPurple = 2
                    thicknessEraser = 1
                
                # If marker's tip coordinates on pink box set color pink
                if w-108 < x2 < w-58 and 5 < y2 < 55:
                    color = colorPink
                    thicknessBlue = 2
                    thicknessYellow = 2
                    thicknessPink = 6
                    thicknessGreen = 2
                    thicknessPurple = 2
                    thicknessEraser = 1
                    
                # If marker's tip coordinates on green box set color green
                if w-163 < x2 < w-113 and 5 < y2 < 55:
                    color = colorGreen
                    thicknessBlue = 2
                    thicknessYellow = 2
                    thicknessPink = 2
                    thicknessGreen = 6
                    thicknessPurple = 2
                    thicknessEraser = 1
                
                # If marker's tip coordinates on blue box set color blue
                if w-218 < x2 < w-168 and 5 < y2 < 55:
                    color = colorBlue
                    thicknessBlue = 6
                    thicknessYellow = 2
                    thicknessPink = 2
                    thicknessGreen = 2
                    thicknessPurple = 2
                    thicknessEraser = 1
                
                # If marker's tip coordinates on purple box set color blue
                if w-268 < x2 < w-218 and 5 < y2 < 55:
                    color = colorPurple
                    thicknessBlue = 2
                    thicknessYellow = 2
                    thicknessPink = 2
                    thicknessGreen = 2
                    thicknessPurple = 6
                    thicknessEraser = 1
                
                # If marker's tip coordinates on eraser
                if 100 < x2 < 200 and 5 < y2 < 55:
                    # Painting with black means delete
                    # Because canvas created with np.zeros
                    color = (0,0,0)
                    thicknessBlue = 2
                    thicknessYellow = 2
                    thicknessPink = 2
                    thicknessGreen = 2
                    thicknessEraser = 2
                 
                # If marker's tip coordinates on large thickness box
                if w-402 < x2 < w-352 and 5 < y2 < 55:
                    thickness = 11
                    thicknessSmall = 1
                    thicknessMedium = 1
                    thicknessLarge = 4
                                 
                # If marker's tip coordinates on medium thickness box
                if w-452 < x2 < w-402 and 5 < y2 < 55:  
                    thickness = 7
                    thicknessSmall = 1
                    thicknessMedium = 4
                    thicknessLarge = 1
                                    
                # If marker's tip coordinates on small thickness box
                if w-502 < x2 < w-452 and 5 < y2 < 55:
                    thickness = 3
                    thicknessSmall = 4
                    thicknessMedium = 1
                    thicknessLarge = 1
                
                # If marker's tip coordinates on clear box
                if 0 < x2 < 100 and 5 < y2 < 55:
                    cv2.putText(frame, 'Clear', (15,35), 5, 1, 
                                colorScreenCleaner, 2, cv2.LINE_AA)
                    # Clear canvas
                    canvas = np.zeros(frame.shape, dtype=np.uint8)
                
                # Show canvas if marker's tip not on top section area
                if y2 < 65 or y1 < 65:
                    canvas = canvas
                
                # Otherwise, assign new values
                else:
                    # If eraser selected, make thickness larger
                    if thicknessEraser == 2:
                        canvas = cv2.line(canvas, (x1,y1), (x2,y2), color, 
                                          thickness+15)
                    
                    # Otherwise, make thickness normal values
                    else:
                        canvas = cv2.line(canvas, (x1,y1), (x2,y2), color, 
                                          thickness)
            
            # Set marker's tip that set options
            cv2.circle(frame, (x2,y2), thickness, color, 2)
            
            # Set painting coordinates
            x1 = x2
            y1 = y2
        
        # If object not trackable
        else:
            # Set painting coordinates none to don't paint
            x1 = None
            y1 = None
    
    # Just for smooth drawing (Optional)
    canvasGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(canvasGray, 10, 255, cv2.THRESH_BINARY)
    thInv = cv2.bitwise_not(th)
    
    # Add mask to frame to show on webcam frame
    frame = cv2.bitwise_and(frame, frame, mask=thInv)
    frame = cv2.add(frame, canvas)
    
    # Stack canvas and frame to show same window
    stacked = np.hstack((canvas, frame))
    
    # Show stacked frames
    cv2.imshow("Painting", cv2.resize(stacked, None, fx=.8, fy=.8))

    # If 'q' pressed then exit the program
    k = cv2.waitKey(1)
    if (k == ord('q') or k == ord('Q')):
        break

# Release the camera and destroy all windows    
cap.release()
cv2.destroyAllWindows()
