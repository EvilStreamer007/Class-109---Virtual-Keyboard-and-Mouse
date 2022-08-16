import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller
#import pyautogui - not needed as installed

keyboard = Controller()
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5)

tipID = [4,8,12,16,20]

state = None

def countFingers(image, handLandmarks, handNumber = 0):
	global state #used to make any variable global
	
	if handLandmarks:
		landmarks = handLandmarks[handNumber].landmark

		fingers = []

		for lm_index in tipID:
			finger_tip_y = landmarks[lm_index].y 
			finger_bottom_y = landmarks[lm_index - 2].y

			if lm_index !=4:
				if finger_tip_y < finger_bottom_y:
					fingers.append(1)

				if finger_tip_y > finger_bottom_y:
					fingers.append(0)

		totalFingers = fingers.count(1)	

		if(totalFingers == 4):
			state = "play"
			print("Playing video")
		
		if(totalFingers == 0 and state == "play"):
			state = "pause"
			print("Pausing video")
			keyboard.press(Key.space)
		
		finger_tip_x = (landmarks[8].x)*width

		if(totalFingers == 1):
			if(finger_tip_x < width-200):
				print("Playing Backwards")
				keyboard.press(Key.left)	

			elif(finger_tip_x > width-50):
				print("Playing Forward")
				keyboard.press(Key.right)
				#not working

def drawHandLanmarks(image, handLandmarks):

    # Darw connections between landmark points
    if handLandmarks:

      for landmarks in handLandmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)

    results = hands.process(image)
    handLandmarks = results.multi_hand_landmarks

    drawHandLanmarks(image, handLandmarks)
    countFingers(image, handLandmarks)

    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

			
