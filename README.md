# autonomous-car
An open-source autonomous RC car project that uses AI for perception and decision-making, inviting the community to collaborate on improving its intelligence, performance, and reliability.

#### Components used
The project uses a simple RC car (the cheapest there was on Amazon - https://www.amazon.in/dp/B0DQGN2913). 

This project also uses the  open source software and hardware platforms
ESP32 - a microcontroller with WiFi and Bluetooth. Hosts a webserver, and also controls the RC Car
OpenCV for Computer Vision - Used by the algorigthm to connect to a camera. Locates the car, and the target and computes the distances, angles and speed at which the car should run

## Summary
The alogrithm is coded in python. It uses Computer Vision (ie OpenCV) to connect to a camera and then locate the car and its target (OpenCV provides its coordinates)
The algorithm then calculates the relative angles of the car and target, the distnace between the car and the target, and the distance between the car and edge of the frame of camera's visions. (This is simple coordinate geometry)
Based on the relaitve angles, and the distance, the algorthm decides the direction the car should move in and the speed it should move at. 
The direction and the speed is then sent by the alogrithm to a REST endpoint which is hosted on the ESP32 microcontroller
