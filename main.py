import network
import socket
from machine import ADC, Pin
import time

SSID = 'Vodafone-820C'
PASSWORD = 'xc5dadQYrqpo2J2sd2q2'


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f'Connecting to {ssid}...', end='')
        wlan.connect(ssid, password)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print(f'.', end='', flush=True)
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print(f'\nConnected! IP Address: {wlan.ifconfig()[0]}')
        else:
            print(f'\nFailed to connect.')
            return False
    else:
        print(f'Already connected. IP Address: {wlan.ifconfig()[0]}')
    return True


# Setup for Joystick 1
joy1_x = ADC(Pin(26))
joy1_y = ADC(Pin(27))
joy1_button = Pin(22, Pin.IN, Pin.PULL_UP)

# Setup for Joystick 2
joy2_x = ADC(Pin(28))
joy2_y = ADC(Pin(29))
joy2_button = Pin(21, Pin.IN, Pin.PULL_UP)

# Setup for Buttons
button1 = Pin(15, Pin.IN, Pin.PULL_UP)
button2 = Pin(14, Pin.IN, Pin.PULL_UP)
button3 = Pin(13, Pin.IN, Pin.PULL_UP)

SERVER_IP = '192.168.0.41'
SERVER_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

threshold_low = 20000
threshold_high = 45000

debounce_time = 0.2  # 200 ms debounce time
last_button1_state = True
last_button2_state = True
last_button3_state = True
last_joy1_button_state = True
last_joy2_button_state = True
last_button1_time = 0
last_button2_time = 0
last_button3_time = 0
last_joy1_button_time = 0
last_joy2_button_time = 0


def send_data(message):
    try:
        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    except OSError as e:
        print(f"Network error: {e}")


def check_joystick_1():
    global last_joy1_button_state, last_joy1_button_time
    x1_val = joy1_x.read_u16()
    y1_val = joy1_y.read_u16()

    command = ""

    if y1_val < threshold_low:
        command = "C"
    elif y1_val > threshold_high:
        command = "X"

    if command:
        send_data(command)

    # Check joystick button press with debounce
    current_time = time.time()
    joy1_button_state = not joy1_button.value()
    if joy1_button_state != last_joy1_button_state:
        if not joy1_button_state and (current_time - last_joy1_button_time) > debounce_time:
            send_data("left click")
            last_joy1_button_time = current_time
        last_joy1_button_state = joy1_button_state


def check_joystick_2():
    global last_joy2_button_state, last_joy2_button_time
    x2_val = joy2_x.read_u16()
    y2_val = joy2_y.read_u16()

    command = ""

    if x2_val < threshold_low:
        command = "C"
    elif x2_val > threshold_high:
        command = "X"

    if y2_val < threshold_low:
        command += "_Up"
    elif y2_val > threshold_high:
        command += "_Down"

    if command:
        send_data(command)

    # Check joystick button press with debounce
    current_time = time.time()
    joy2_button_state = not joy2_button.value()
    if joy2_button_state != last_joy2_button_state:
        if not joy2_button_state and (current_time - last_joy2_button_time) > debounce_time:
            send_data("right click")
            last_joy2_button_time = current_time
        last_joy2_button_state = joy2_button_state


def check_buttons():
    global last_button1_state, last_button2_state, last_button3_state, last_button1_time, last_button2_time, last_button3_time
    current_time = time.time()

    # Button 1
    button1_state = not button1.value()
    if button1_state != last_button1_state:
        if not button1_state and (current_time - last_button1_time) > debounce_time:
            send_data("jump")
            last_button1_time = current_time
        last_button1_state = button1_state

    # Button 2
    button2_state = not button2.value()
    if button2_state != last_button2_state:
        if not button2_state and (current_time - last_button2_time) > debounce_time:
            send_data("M")
            last_button2_time = current_time
        last_button2_state = button2_state

    # Button 3
    button3_state = not button3.value()
    if button3_state != last_button3_state:
        if not button3_state and (current_time - last_button3_time) > debounce_time:
            send_data("F")
            last_button3_time = current_time
        last_button3_state = button3_state


def main_loop():
    while True:
        check_joystick_1()
        check_joystick_2()
        check_buttons()
        time.sleep(0.1)  # Adjust the delay as needed


try:
    print("Connecting to Wi-Fi...")
    if connect_wifi(SSID, PASSWORD):
        print("Starting the main loop...")
        main_loop()
    else:
        print("Could not connect to Wi-Fi. Exiting...")
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    sock.close()

