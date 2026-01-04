# autonomous-car
An open-source autonomous RC car project that uses AI for perception and decision-making, inviting the community to collaborate on improving its intelligence, performance, and reliability.
Link to see it in action - https://youtu.be/dm20lDCO6KI

#### Components used
The project uses a simple RC car (the cheapest there was on Amazon - https://www.amazon.in/dp/B0DQGN2913). 

This project also uses the  open source software and hardware platforms
ESP32 - a microcontroller with WiFi and Bluetooth. Hosts a webserver, and also controls the RC Car
OpenCV for Computer Vision - Used by the algorigthm to connect to a camera. Locates the car, and the target and computes the distances, angles and speed at which the car should run

## Summary
The alogrithm is coded in python. It uses Computer Vision (ie OpenCV) to connect to a camera and then locate the car and its target (OpenCV provides its coordinates)

The algorithm then calculates the relative angles of the car and target, the distnace between the car and the target, and the distance between the car and edge of the frame of camera's visions. (This is simple coordinate geometry)

Based on the relaitve angles, and the distance, the algorthm decides the direction the car should move in and the speed it should move at. 

The direction and the speed is then sent by the alogrithm to a REST endpoint which is hosted on the ESP32 microcontroller.
The ESP32 is capable of controlling the RC of the CAR. ESP32 commmands the car to move based on the direction (front, back, right or left) and the speed it receives in the REST request.

#### Use of ESP32 to hack the RC CAR
The standard Remote Control of an RC car has 4 switches, each of which controls front, back, right and left.

Open the Remote Control. Remove the 4 mechanical switches. Now use a transistor (Bipolar Junctions Transistor) as a switch to replace each of those switches

The Base of each of those transistor switches is then connected to ESP32 pins.

The +3V supply from the ESP32 board is sufficient to power the RC

<img width="784" height="588" alt="RC_ESP32_hack" src="https://github.com/user-attachments/assets/8913831c-b3e8-4ad4-8fa0-fd27b3084966" />



