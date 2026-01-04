import cv2
import numpy as np
import math
import requests
import time


def direction(car_front_leftx, car_front_lefty, car_bottom_leftx, car_bottom_lefty, target_front_leftx, target_front_lefty):

    car_angle = math.degrees(math.atan2(-(car_front_lefty-car_bottom_lefty), car_front_leftx-car_bottom_leftx))
    target_to_car_angle = math.degrees(math.atan2(-(car_front_lefty-target_front_lefty), car_front_leftx-target_front_leftx))
            
    return(car_angle, target_to_car_angle)


                    
      

def car_movement(car_speed):
    ##IP address of the remote
    domain = "192.168.1.100"

    # 1. Load the dictionary and detector parameters
    # This MUST match the dictionary you used to generate the markers
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # 2. Define your object mapping
    # Map the ID to the real-world object name
    object_map = {
        0: "Car",
        1: "Target"
    }

    # 3. Start the Webcam
    cap = cv2.VideoCapture(0)  # Use 0 for default camera, 1 for external
    #cap = cv2.VideoCapture("http://192.168.1.102:4747/video")

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    print("Press 'q' to quit...")

    initial_car_posx, initial_car_posy = 0.0, 0.0
    final_car_posx, final_car_posy = 0.0, 0.0
    car_loc_change = True
    camera_iter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 4. Detect Markers
        # corners: positions of the markers
        # ids: the unique ID numbers detected
        corners, ids, rejected = detector.detectMarkers(gray)

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))   


        car_front_leftx, car_front_lefty = None, None
        car_front_rightx, car_front_righty = None, None
        car_bottom_rightx, car_bottom_righty = None, None
        car_bottom_leftx, car_bottom_lefty = None, None
        target_front_leftx, target_front_lefty = None, None
        target_front_rightx, target_front_righty = None, None
        target_bottom_rightx, target_bottom_righty = None, None
        target_bottom_leftx, target_bottom_lefty = None, None 



        # 5. Process detected markers
        if ids is not None:
            # Draw outlines for all markers
            #cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.aruco.drawDetectedMarkers(frame, corners)


            # Loop through each detected marker to label it
            for i, marker_id in enumerate(ids.flatten()):
                # Get the center point of the marker for text placement
                # corners[i][0] is the list of 4 points: top-left, top-right, bottom-right, bottom-left
                c = corners[i][0]
                center_x = int(c[:, 0].mean())
                center_y = int(c[:, 1].mean())
                #array of the corners
                #print(c)
                obj_name = object_map[marker_id]
                #label = f"{obj_name} (ID: {marker_id})"    #To Debug
                label = f"{obj_name}"
            

                # if marker belongs to the car
                if marker_id == 0:
    
                                
                    car_front_leftx, car_front_lefty = c[0]
                    car_front_rightx, car_front_righty = c[1]
                    car_bottom_rightx, car_bottom_righty = c[2]
                    car_bottom_leftx, car_bottom_lefty = c[3]

                    # Draw the label near the top left of the CAR
                    cv2.putText(frame, label, (int(car_bottom_rightx), int(car_bottom_righty)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    cv2.arrowedLine(frame, (int(car_bottom_leftx), int(car_bottom_lefty)), (int(car_front_leftx), int(car_front_lefty)), (0, 0, 255), 2, line_type=cv2.LINE_AA, tipLength=0.1)

                    #Draw coordinates                              
                    cv2.putText(frame, str(car_front_leftx)+","+str(car_front_lefty),(int(car_front_leftx),int(car_front_lefty)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1) 


                # if marker belongs to target
                elif marker_id == 1:
                    # obj_name = object_map[marker_id]
                    # label = f"{obj_name} (ID: {marker_id})"

                    target_front_leftx, target_front_lefty = c[0]
                    target_front_rightx, target_front_righty = c[1]
                    target_bottom_rightx, target_bottom_righty = c[2]
                    target_bottom_leftx, target_bottom_lefty = c[3]             
                    
                    # Draw the label near the top left of the TARGET
                    cv2.putText(frame, label, (int(target_bottom_rightx), int(target_bottom_righty)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    
                    cv2.circle(frame, (int(target_front_leftx), int(target_front_lefty)), 2, (0, 0, 255), 2)
                        
                    #Draw coordinates
                    cv2.putText(frame, str(target_front_leftx)+","+str(target_front_lefty),(int(target_front_leftx),int(target_front_lefty)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1) 
                    


                else:
                    # Handle unknown markers
                    cv2.putText(frame, f"Unknown (ID: {marker_id})", (center_x, center_y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            if car_front_leftx and target_front_leftx:

                #Green line from front of car to target
                cv2.line(frame, (int(car_front_leftx), int(car_front_lefty)), (int(target_front_leftx), int(target_front_lefty)), (0, 255, 0), 2)

                #Blue line from bottom of car to target
                cv2.line(frame, (int(car_bottom_leftx), int(car_bottom_lefty)), (int(target_front_leftx), int(target_front_lefty)), (255, 0, 0), 2)
                
                #Defining the DMZ
                ##Length of car = 4 times the length of aruco marker
                CAR_LENGTH = 3.25 * round(math.sqrt((car_front_leftx - car_bottom_leftx)**2 + (car_front_lefty - car_bottom_lefty)**2),2)
                ##WIDTH of car = 2 times the lenght of the car
                CAR_WIDTH = 1.25 * round(math.sqrt((car_front_leftx - car_bottom_leftx)**2 + (car_front_lefty - car_bottom_lefty)**2),2)
                DMZ_Y = CAR_LENGTH * 0.75
                DMZ_X = CAR_WIDTH * 0.75

                #Distance between the target and the car
                target_car_back = round(math.sqrt((target_front_leftx - car_bottom_leftx)**2 + (target_front_lefty - car_bottom_lefty)**2),2)
                target_car_front = round(math.sqrt((target_front_leftx - car_front_leftx)**2 + (target_front_lefty - car_front_lefty)**2),2)            
                
                #Initializing the car's movmeent
                movement = "None"

                ## Car has reached target
                if (target_car_front < CAR_LENGTH/2) or (target_car_back < CAR_LENGTH/2): 
                    print("target reached")
                    cv2.putText(frame, "Target Reached", (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                    #time.sleep(10)
                    #return("Car has reached the target")

                ##Car has not reached its target
                else:
                    ##Get angle of Car from horizontal; and get angle of target to car's bottom from horizonatal
                    car_angle, target_to_car_angle = direction(car_front_leftx, car_front_lefty, car_bottom_leftx, car_bottom_lefty, target_front_leftx, target_front_lefty)
                    dmz_duration = 30
                    #normal_duration = 50
                    #normal_duration = int(round(target_car_front/4,0))
                    normal_duration = int(round(target_car_front/car_speed,0))
                    

                    #If car in DMZ then move out
                    if ( abs(car_front_lefty-0) < DMZ_Y ): ##upper fame
                        print("dmz")
                        duration = dmz_duration
                        if car_angle > 0:
                            movement = "back"
                        else:
                            movement = "front"
                    elif( abs(car_front_lefty-frame_height) < DMZ_Y ): ##lower frame
                        print("dmz")
                        duration = dmz_duration
                        if car_angle > 0:
                            movement = "front"
                        else:
                            movement = "back"      
                    elif( abs(car_front_leftx-frame_width) < DMZ_X ):   ##right frame
                        print("dmz")
                        duration = dmz_duration
                        if (car_angle < 90) and (car_angle > -90):
                            movement = "back"
                        else:
                            movement = "front"                                             
                    elif( abs(car_front_leftx - 0) < DMZ_X ):   ##left frame
                        print("dmz")
                        duration = dmz_duration
                        if (car_angle < 90) and (car_angle > -90):
                            movement = "front"
                        else:
                            movement = "back"   
                    
                    #Car is not in DMZ, and has not reached its target
                    else:
                        #print("normal movement")
                        diff = target_to_car_angle - car_angle
                        normalized_diff = ( (180+diff) % 360) - 180
                        margin = 20
                        cv2.putText(frame, "Difference:" + str(round(normalized_diff,2)), (5,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                        duration = normal_duration
                        
                        if abs(normalized_diff) > margin:
                            if normalized_diff < 0 and diff > -90:
                                movement = "back-left"
                            if normalized_diff > -180 and diff < -90:
                                movement = "front-left"
                            if normalized_diff > 0 and diff < 90:
                                movement = "back-right"
                            if normalized_diff > 90 and diff < 180:
                                movement = "front-right"
                        if abs(normalized_diff) < margin or abs(normalized_diff) > 180-margin:
                            if abs(normalized_diff) < margin:
                                movement = "back"
                            if abs(normalized_diff) > 180 - margin:
                                movement = "front"                    

                    cv2.putText(frame, "Car:" + str(round(car_angle,2)), (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1) 
                    cv2.putText(frame, "Target to Car Angle:" + str(round(target_to_car_angle,2)), (5,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1) 
                                        
                    cv2.putText(frame, "Movement:" + movement, (5,80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1) 
                    
                    if "front" in movement:
                        brake = "back"
                    else:
                        brake = "front"

                    
                    initial_car_posx = final_car_posx
                    initial_car_posy = final_car_posy

                    final_car_posx = car_front_leftx
                    final_car_posy = car_front_lefty

                    if iter !=0 and (abs(final_car_posy - initial_car_posy) < 4 and abs(final_car_posx - initial_car_posx) < 4):
                        car_loc_change = False
                    else:
                        car_loc_change = True

                    if car_loc_change == True:
                        movement_path = "http://"+domain+"/action/"+movement+"/time/"+str(int(round(duration,0)))+"/end"
                        #brake_path = "http://"+domain+"/action/"+brake+"/time/0.7/end"  
                        #print(movement_path)
                        #print(brake_path)
                        
                        movement_response = requests.get(movement_path)    
                        #brake_response = requests.get(movement_path)   
                        #time.sleep(1.5) 
                        cv2.waitKey(int(round(duration,0)))

                        camera_iter = 0
                    else:
                        camera_iter = camera_iter + 1
                        #print(f"Camera iteration : {camera_iter}")
                        if camera_iter > 30:
                            camera_iter = 0
                            movement_response = requests.get(movement_path) 
                            #print("Camera iteration reset")
                            
                            

        if not car_front_leftx:
            #print("Car not present")  ## DEBUG
            cv2.putText(frame, "Car: Not present", (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1) 
        if not target_front_leftx:
            #print("Target not present") ##DEBUG
            cv2.putText(frame, "Target : Not present", (5,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1) 

            #

        # Show the frame
        cv2.namedWindow("ArUco Object Tracker", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("ArUco Object Tracker", 1200, 800)
        cv2.imshow("ArUco Object Tracker", frame)

        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
        print(car_movement(8))    


