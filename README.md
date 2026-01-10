# autonomous-car
An open-source autonomous RC car project that uses AI for perception and decision-making. Inviting the community to collaborate on improving its intelligence, performance, and reliability.
Link to see it in action - https://youtu.be/dm20lDCO6KI

#### Components used
The project uses a simple RC car (the cheapest there was on Amazon - https://www.amazon.in/dp/B0DQGN2913). 

This project also uses the  open source software and hardware platforms
ESP32 - a microcontroller with WiFi and Bluetooth. Hosts a webserver, and also controls the RC Car
OpenCV for Computer Vision - Used by the algorigthm to connect to a camera. Locates the car, and the target and computes the distances, angles and speed at which the car should run
Bipolar Transistors, 10K Ω resistors (PCB, jumper wire, header pins, soldering iron etc)

## Summary
The project can be split into the following component, which are integrated at the end
1. Hack the remote of the car, and replace its manual switch with a Bipolar transitor (basically transistor as a switch, BJT switches). There'd be a BJT switch each for front, back, left and right
2. Code ESP32 such that it can control the BJT switches I mentioned earlier. 4 pins from ESP32 connected to 4 BJT switches; +3V/GND from ESP32 connected to the remotes +/- battery terminals
3. Also, code ESP32 to host a webserver(an http endpoint). The requests coming to the http endpoint will contain the instructions to control the RC car (front, back, left, right and duration)
4. The ComputerVision code which - uses a camera to locate your car/target; calculates the movements required by the car to reach the target; and then sends adequate requests to ESP32 webserver

TL;DR . Hack the remote with ESP32. Algorithm to determine the position of the car, and decide its movement. Algorithm then coded in python. Uses OpenCV and basic maths (coordinate geometry)

## In Detail

#### 1. Hack the remote of the car........... 
A standard Remote Control of an RC car has 4 switches - front, back, right and left. Open it, remove the plastics, the connections to the battery, everything until you are left with the circuit board and the components on it. The circuit board will have 
1. 5 tactile switches (4 pin) - you can see where they were positioned in the picture (1). The 4 tactitle switches in the corners control the movement. The 5th switch at the centre is the power button
2. The battery terminals (They will be marked B+ and B-).

(You can connect the +3V from ESP32 to B+, and the GND from ESP32 to B-. Then switch on one of the tectile switch to check if the RC still works.)

Step 1 - Remove the 4 tactile switch which control the movement. Do not remove the 5th tactile switch which is the power button.

Step 2 - Make 4 BJT switches. Something like this https://learn.sparkfun.com/tutorials/transistors/applications-i-switches. I have used NPN transitors 

Step 3 - Connect each of the 4 BJT switches to the pins where the 4 tactile switches used to be. So for e.g. To control the front movmement - take one of your BJT switches. Locate where the front control tactile switch was, and more importantly which pin was connected to +/-ve ends of the battery. If you are using npn transistor then connect the collector to the +ve pin, emitter to the -ve pin (For pnp it wil be the other way around). 

Step 4 - Solder a wire (or a header pin, which then can be connected to a wire) to the base resistor of the 4 BJT switches. Eventually this wire will control the movement of the CAR

Time to test - Connect the battery terminals to ESP32 (ie B+ on PCB to +3V on esp32; B- to GND on ESP32). Now pick up the wire connected to the base resistor of any one of the 4 BJT switches. Connect it to +3V on ESP32, and check for the response from the car. (you can try combinations - like, pick up the base resistor connections for front and left, and then connect it to +3V, and see if the care moves front and left.)

(If this is your first time soldering then probably try making the ciruit on a breadboard first.... )

<img width="784" height="588" alt="RC_ESP32_hack" src="https://github.com/user-attachments/assets/8913831c-b3e8-4ad4-8fa0-fd27b3084966" />

#### 2 & 3. Code ESP32........... 
The ESP32 microncontroler will server as the integration between your alogrithm, and the hacked RC of your car. So while it recieves the requests from your alogrithm via the web server it hosts, it will interpet those request and send signals to the BJT switches connected to your RC. This is how you will do so.

You will need a wifi, because that's how the alogorithm running on your PC will send commands wirelessly to your esp32

Step 1. Download code [09-remote-control.ino](https://github.com/sojith/autonomous-car/blob/main/09-remote-control.ino) that is provided in this repo. 
Step 2. Update the code with your Wifi name, and its password in line 5 & 6.
Step 3. Upload the code to ESP32. 
Step 4. Identify pins 13,15,19 and 32 on ESP32. 13 & 15 will control the front and back montions. 19 & 32 will control the the left and right motion.
Step 5. Connect pin 13 from ESP32 to the base resistor of the BJT switch which controls forward movment of the car. Similarly pin15 to BJT switch for backward movement; pin 19 to BJT switch for left; and pin 32 to BJT switch for right
Step 6. Connect the battery terminals on the RC  to ESP32 (ie B+ on PCB to +3V on esp32; B- to GND on ESP32)

Step 7. Identify the ip address of your esp32. To do so switch on your wifi. Then switch on your ESP32. The ESP32 will connect to WIFI (because step 2). Open your wifi's console on your laptop and then shoud be able to find the ip address of the esp32. What i have done is to permanently assign an ip address to my esp32 (like 192.168.1.100)

Your ESP32 code now runs a webserver capable of receiving https requests.




