from google import genai
from google.genai import types
import re
import cv2
import calibration
import car
import requests
import time


#The function takes a picture. Saves it. Then calls LLM with the saved image to identify it
def func_check_camera():
    ##Check if camera is opern
    try:
        cap = cv2.VideoCapture(0)
    except:
        pass

    try:
        if not cap.isOpened():
            cap.release()
            print("No camera detected or camera is not accessible.")
            return "No camera detected or camera is not accessible."
        else:
            ## Take a pic
            # Read a single frame from the camera
            ret, frame = cap.read()

            if ret:
                # Save the captured image
                cv2.imwrite("captured_image.jpg", frame)
                # Release the camera
                cap.release()
                cv2.destroyAllWindows()
            else:
                cap.release()
                cv2.destroyAllWindows()    
                print("Error: Could not read frame from webcam.")
                return "User asked to take a pic using the attached cam. But coudl not read frame from webcam."              



            ##Identify image
            with open('captured_image.jpg', 'rb') as f:
                image_bytes = f.read()

            response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
                ),
                'What is this an image of?'
            ]
            )

            print(response.text)
            return "User asked to identify the object. This was the response " + response.text
            
    except:
        print("Could not connect to camera")
        return "Could not connect to camera"

def func_car():
    calibration_response = calibration.calibrate()

    if isinstance(calibration_response, str):
        print(calibration_response)
        return(calibration_response)
    else:
        print(f"Speed is {calibration_response} px/ms")  

        input("Proceed:")

        car.car_movement(calibration_response*10)    
        print("The car has reached its target")
        return("he car has reached its target")

def func_movement(url_path):
    full_path = "http://"+domain+"/"+url_path
    response = requests.get(full_path)
    print (response.headers)

domain = "192.168.1.100"

# A dictionary to map function names (strings) to function objects
function_map = {
    "func_check_camera": func_check_camera,  
    "func_car": func_car
}

## Use in the System prompt to relate a users question to the name of the funciton
question_json = "{" \
"'Is the camera working':'func_check_camera'," \
"'Move the car to its target':'func_car'," \
"}"

client = genai.Client(api_key="")
chat = client.chats.create(model="gemini-2.5-flash",                       
                           config=types.GenerateContentConfig(
                               thinking_config=types.ThinkingConfig(thinking_budget=0),
                               system_instruction=\
                                "You are an autonomous car."\
                                "1. If the user asks you move the car to the target then print 'func_car'"
                                "2. If the user asks you to check the camera then print 'func_check_camera'"

                               )
                           )


while True:
    print("\n\n---------------------------------------")
    question = input("> ")
    print("\n\n")
    if question == "q":
        break
    result = chat.send_message(question)
    #print(result.text)

    pattern = r"\bfunc_\w+"
    if  re.findall(pattern, result.text):
        
        func_name = re.findall(pattern, result.text)
        print(func_name)
        func = function_map[func_name[0]]
        function_ouput = func()
        if function_ouput:
            result = chat.send_message(function_ouput)
            print(result.text)
    if ("action/" in result.text) and ("/time/" in result.text) and ("/end" in result.text):
        print(result.text)
        pattern1 = r'action/[^/]+/[^/]+/[^/]+/end'
        output_list = re.findall(pattern1, result.text)
        for output_list_lines in output_list:
            func_movement(output_list_lines)
            time.sleep(1)
            #print(output_list_lines)            
    else:
        print(result.text)

