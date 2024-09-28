Joystick and Button Controller with Wi-Fi Communication

Overview

This project demonstrates how to use a Raspberry Pi Pico W to read inputs from two joysticks and three buttons and send the corresponding commands to a remote server over a Wi-Fi connection using UDP. The system uses debouncing to avoid unintentional button presses and thresholds to detect joystick movements. It supports:

Two analog joysticks, each with an X and Y axis, and a button.
Three digital buttons.
Wi-Fi connectivity to send the joystick and button data to a remote server.
Components

Raspberry Pi Pico W
2 Joysticks (each with X, Y axes and a button)
3 Push buttons
Wi-Fi network
Features

Wi-Fi Connection: Connects to a specified Wi-Fi network using the provided SSID and password.
Joystick Control: Reads the X and Y positions of two joysticks and detects button presses.
Button Control: Monitors three push buttons with debouncing to avoid repeated signals.
UDP Communication: Sends commands to a server over UDP based on the joystick and button inputs.
Requirements

Hardware: Raspberry Pi Pico W, 2 Joysticks, 3 Buttons
Software: MicroPython installed on Raspberry Pi Pico W, UDP Server on the receiving end.
Circuit Diagram

Component	Pin on Pico
Joystick 1 X-axis	GPIO 26 (ADC0)
Joystick 1 Y-axis	GPIO 27 (ADC1)
Joystick 1 Button	GPIO 22
Joystick 2 X-axis	GPIO 28 (ADC2)
Joystick 2 Y-axis	GPIO 29 (ADC3)
Joystick 2 Button	GPIO 21
Button 1	GPIO 15
Button 2	GPIO 14
Button 3	GPIO 13
Code Explanation

Wi-Fi Setup:
The code connects to a Wi-Fi network using the provided SSID and password.
Joysticks & Buttons:
Reads the analog values from the joysticks using the ADC pins and determines movement based on threshold values.
The joystick button and three additional buttons are debounced and monitored for state changes.
UDP Communication:
When joystick movements or button presses are detected, corresponding commands are sent to a server over a UDP socket.
Main Loop:
The main_loop continuously monitors the state of the joysticks and buttons, sending commands based on their states.
How to Use

Configure Wi-Fi:
Edit the SSID and PASSWORD variables with your Wi-Fi credentials.
Set Server IP:
Update the SERVER_IP variable with the IP address of the server that will receive the UDP packets.
Deploy to Raspberry Pi Pico:
Upload the code to your Raspberry Pi Pico W running MicroPython.
Run the Code:
The code will attempt to connect to the Wi-Fi network and start reading inputs from the joysticks and buttons, sending the data to the server.
Example Commands

Joystick 1:
Moves up: "C"
Moves down: "X"
Button press: "left click"
Joystick 2:
Moves left: "C_Up"
Moves right: "X_Down"
Button press: "right click"
Buttons:
Button 1: "jump"
Button 2: "M"
Button 3: "F"


Demo : 

[Joystick Controller Demo](https://www.instagram.com/reel/C-QlV3jAvQR/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==
