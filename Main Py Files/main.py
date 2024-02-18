import time
import network
import utime
import random
import ubinascii
from umqtt.simple import MQTTClient
import machine

#Interrupt request
interrupt_flag = False

#Interrupt function ISR
def reset_interrupt_handler(pin):
    global interrupt_flag
    interrupt_flag = True

#Wifi Details
SSID=None
SSID_PASSWORD=None

#Function to connect with the WIFI
def do_connect():
    global SSID,SSID_PASSWORD
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())

#Function to disconnect from Wifi
def disconnect_from_wifi():
    # Initialize Wi-Fi interface
    wifi_interface = network.WLAN(network.STA_IF)

    # Disconnect from the Wi-Fi network
    wifi_interface.disconnect()

    # Give some time for disconnection to complete
    time.sleep(1)

    # Check if disconnected
    if not wifi_interface.isconnected():
        print("Disconnected from Wi-Fi network.")
    else:
        print("Failed to disconnect from Wi-Fi network.")
#End of Disconnected Funtion
        
# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = "192.168.160.115"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC1 = None #subscriber topic as well publisher topic
TOPIC2 = None #subscriber topic as well publisher topic
TOPIC3 = None #subscriber topic as well publisher topic
TOPIC4 = None #subscriber topic as well publisher topic
TOPIC6 = b"LED_ALL" #subscriber topic #fixed because it controls all the devices
TOPIC5 = b"Status" #Publisher topic
TOPIC7 = None #subscriber topic
TOPIC11= b"LEDOFF" #Publish for all LED


# Variable to store the received message
received_message = None
received_topic = None
# Ping the MQTT broker since we are not publishing any message
last_ping = time.time()
ping_interval = 60

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    global received_message,received_topic
    if topic == TOPIC1:
        received_message = msg
        received_topic = topic
        print("TOPIC 1 called")
        #print((topic, msg))
    elif topic == TOPIC2:
        received_message = msg
        received_topic = topic
        print("TOPIC 2 called")
        #print((topic, msg))
    elif topic == TOPIC3:
        received_message = msg
        received_topic = topic
        print("TOPIC 3 called")
    elif topic == TOPIC4:
        received_message = msg
        received_topic = topic
        print("TOPIC 4 called")
    elif topic == TOPIC6:
        received_message = msg
        received_topic = topic
        print("TOPIC 6 called")
    elif topic == TOPIC7:
        received_message = msg
        received_topic = topic
        print("TOPIC 7 called")
    else:
        print("No Topic Called")

def reset():
    print("Broker Not available.Resetting...")
    time.sleep(5)
    machine.reset()
#End OF MQTT Checking

#Setting Up the Digital Pins
LED1 = machine.Pin(15,machine.Pin.OUT)
LED2 = machine.Pin(5,machine.Pin.OUT)
LED3 = machine.Pin(18,machine.Pin.OUT)
LED4 = machine.Pin(21,machine.Pin.OUT)
FAN = machine.Pin(12, machine.Pin.OUT)
fan_pwm = machine.PWM(FAN)

# Define minimum and maximum duty cycle values
min_duty = 0  # 0% duty cycle
max_duty = 1023  # 100% duty cycle

#Function for setting fan speed
def set_fan_speed(speed_percentage):
    # Convert speed percentage to duty cycle value
    duty_cycle = int((speed_percentage / 100) * max_duty)
    fan_pwm.duty(duty_cycle)
    
set_fan_speed(0)

#Main Part of the program
def main():
    #Setting up variables
    global received_message,received_topic
    global interrupt_flag
    global SSID,SSID_PASSWORD,TOPIC1,TOPIC2,TOPIC3,TOPIC4,TOPIC7
    
    #Reading Appropriate data from the Text File 
    Username = None
    x=[]
    with open('data.txt', 'r') as file:
        for line in file:
            key= line.rstrip()
            x.append(key)
            
    #Putting the appropriate data into Variables SSID and Topics
    Username=x[0]
    SSID = x[1]
    SSID_PASSWORD = x[2]
    TOPIC1=x[3].encode()
    TOPIC2=x[4].encode()
    TOPIC3=x[5].encode()
    TOPIC4=x[6].encode()
    TOPIC7=x[7].encode()
    
    #Setting Up Pin For Interrupt Request
    EN_PIN = 0  # Define the pin number for the reset pin
    reset_pin = machine.Pin(EN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    reset_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=reset_interrupt_handler)
    start_time = time.ticks_ms()
    #End OF Interrupt part in main(Remaining In While True Loop)
    
    #Turning On the WIFI Of ESP32 Module
    print("Connecting to your wifi...")
    do_connect()
    print("Connected to wifi")
    #Connected with The WIFI 
    
    #Setting Up MQTT In the main Code
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(TOPIC1)
    mqttClient.subscribe(TOPIC2)
    mqttClient.subscribe(TOPIC3)
    mqttClient.subscribe(TOPIC4)
    mqttClient.subscribe(TOPIC6)
    mqttClient.subscribe(TOPIC7)
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")
    #End of MQTT Part
    
    #Checking IF LEDs were Previously ON or OFF
    if LED2.value()==0 and LED3.value()==0 and LED4.value()==0 and LED1.value()==0:
        msg3=b'OFF'
        msg4=b'0'
        mqttClient.publish(TOPIC1,msg3)
        mqttClient.publish(TOPIC2,msg3)
        mqttClient.publish(TOPIC3,msg3)
        mqttClient.publish(TOPIC4,msg3)
        mqttClient.publish(TOPIC11,msg3)
        mqttClient.publish(TOPIC7,msg4) 
    else:
        msg3=b'ON'
        msg4=b'0'
        mqttClient.publish(TOPIC1,msg3)
        mqttClient.publish(TOPIC2,msg3)
        mqttClient.publish(TOPIC3,msg3)
        mqttClient.publish(TOPIC4,msg3)
        mqttClient.publish(TOPIC11,msg3)
        mqttClient.publish(TOPIC7,msg4)
    #Finished Checking
    
    #part of the Code which gets repeated until break statement arrives
    while True:
       #This Portion is for Checking which topic is received and publish Appropriate messages to the user 
        if received_message is not None:
            #FOR LED1
            if received_topic == TOPIC1:
                if received_message==b'ON':
                    LED1.value(1)
                    msg1 = "LED 1 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    if LED2.value()==1 and LED3.value()==1 and LED4.value()==1:
                        msg3=b'ON'
                        mqttClient.publish(TOPIC11,msg3)
                    else:
                        msg3=b'OFF'
                        mqttClient.publish(TOPIC11,msg3)
                else:
                    LED1.value(0)
                    msg1 = "LED 1 is OFF"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    msg3=b'OFF'
                    mqttClient.publish(TOPIC11,msg3)
            #FOR LED1
                    
            #FOR LED2
            elif received_topic == TOPIC2:
                if received_message==b'ON':
                    LED2.value(1)
                    msg1 = "LED 2 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    if LED1.value()==1 and LED3.value()==1 and LED4.value()==1:
                        msg3=b'ON'
                        mqttClient.publish(TOPIC11,msg3)
                    else:
                        msg3=b'OFF'
                        mqttClient.publish(TOPIC11,msg3)
                else:
                    LED2.value(0)
                    msg1 = "LED 2 is OFF"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    msg3=b'OFF'
                    mqttClient.publish(TOPIC11,msg3)
            #FOR LED2
                    
            #FOR LED3        
            elif received_topic == TOPIC3:
                if received_message==b'ON':
                    LED3.value(1)
                    msg1 = "LED 3 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    if LED2.value()==1 and LED1.value()==1 and LED4.value()==1:
                        msg3=b'ON'
                        mqttClient.publish(TOPIC11,msg3)
                    else:
                        msg3=b'OFF'
                        mqttClient.publish(TOPIC11,msg3)
                else:
                    LED3.value(0)
                    msg1 = "LED 3 is OFF"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    msg3=b'OFF'
                    mqttClient.publish(TOPIC11,msg3)
            #FOR LED3
            
            #FOR LED4
            elif received_topic == TOPIC4:
                if received_message==b'ON':
                    LED4.value(1)
                    msg1 = "LED 4 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    if LED2.value()==1 and LED3.value()==1 and LED1.value()==1:
                        msg3=b'ON'
                        mqttClient.publish(TOPIC11,msg3)
                    else:
                        msg3=b'OFF'
                        mqttClient.publish(TOPIC11,msg3)
                else:
                    LED4.value(0)
                    msg1 = "LED 4 is OFF"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    msg3=b'OFF'
                    mqttClient.publish(TOPIC11,msg3)
            #FOR LED4
                    
            #FOR ALL LEDs
            elif received_topic == TOPIC6:
                if received_message==b'ON':
                    LED1.value(1)
                    LED2.value(1)
                    LED3.value(1)
                    LED4.value(1)
                    msg1 = "All LEDs are ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    msg3=b'ON'
                    mqttClient.publish(TOPIC1,msg3)
                    mqttClient.publish(TOPIC2,msg3)
                    mqttClient.publish(TOPIC3,msg3)
                    mqttClient.publish(TOPIC4,msg3)
                    mqttClient.publish(TOPIC11,msg3)
                else:
                    LED1.value(0)
                    LED2.value(0)
                    LED3.value(0)
                    LED4.value(0)
                    msg1 = "All LEDs are OFF"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    msg3=b'OFF'
                    mqttClient.publish(TOPIC1,msg3)
                    mqttClient.publish(TOPIC2,msg3)
                    mqttClient.publish(TOPIC3,msg3)
                    mqttClient.publish(TOPIC4,msg3)
                    mqttClient.publish(TOPIC11,msg3)
            #FOR ALL LEDs
                    
            #FOR FAN
            elif received_topic == TOPIC7:
                    # Read input from user for desired fan speed
                    speed_input = received_message
                    try:
                        # Convert input to integer and ensure it's within range
                        speed = int(speed_input)
                        if 0 <= speed <= 100:
                            set_fan_speed(speed)
                            msg1 = str(speed)
                            print(f"Publishing msg :: {msg1}")
                            mqttClient.publish(TOPIC5, str(msg1).encode())
                        else:
                           print("Speed must be between 0 and 100")
                    except ValueError:
                        print("Invalid input. Please enter a number between 0 and 100.")
            #FOR FAN
            
            #No Topic Called
            else:
                print("No such Topic Exists");
            # No Topic Called
            
            # Reset the variables
            received_message = None
            received_topic = None
            
        # Non-blocking wait for message
        mqttClient.check_msg()
        # Then need to sleep to avoid 100% CPU usage 
        #waits for this much time
        time.sleep(0.15)
        
        # Then need to sleep to avoid 100% CPU usage (in a real
        # app other useful actions would be performed instead)
        global last_ping
        if (time.time() - last_ping) >= ping_interval:
            mqttClient.ping()
            last_ping = time.time()
            now = time.localtime()
            print(f"Pinging MQTT Broker, last ping :: {now[0]}/{now[1]}/{now[2]} {now[3]}:{now[4]}:{now[5]}")
        
        time.sleep(0.15)
        # Checks for pings throughout the runtime
        
        #Checks the Interrupt Request Constantly. If pressed for 5 seconds consecutively, Then Only it follows the ISR and resets Everything
        if not reset_pin.value():
            if time.ticks_diff(time.ticks_ms(), start_time) >= 5000:
                if interrupt_flag:
                    print("Reset pin pressed for 5 seconds. Generating interrupt request.")
                    x=[]
                    Username=None
                    TOPIC1=None
                    TOPIC2=None
                    TOPIC3=None
                    TOPIC4=None
                    TOPIC7=None
                    SSID=None
                    #msg3=b'OFF'
                    #mqttClient.publish(TOPIC1,msg3)
                    #mqttClient.publish(TOPIC2,msg3)
                    #mqttClient.publish(TOPIC3,msg3)
                    #mqttClient.publish(TOPIC4,msg3)
                    #mqttClient.publish(TOPIC11,msg3)
                    LED1.value(0)
                    LED2.value(0)
                    LED3.value(0)
                    LED4.value(0)
                    set_fan_speed(0)
                    SSID_PASSWORD=None
                    with open('data.txt', 'w') as file:
                        pass
                    msg1 = "Disconnected.Reboot with BT"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())    
                    print("Program Terminated,ALL VARIABLES HAVE BEEN RESET")
                    print("Disconnecting...")
                    
                    mqttClient.disconnect()
                    print("Disconnected. Reboot The Device and follow the BLE Process. Fill the same data again")
                    disconnect_from_wifi()
                    break
                # Perform action for generating interrupt request
                # For example: machine.reset()
                else:
                    print("Reset pin not continuously pressed for 5 seconds.")
            # Reset interrupt flag and start time
                interrupt_flag = False
                start_time = time.ticks_ms()
                print(start_time)
        else:
        #print("Pressed for less than 5 seconds")
            start_time = time.ticks_ms()

        #End OF Interrupt Service

#Runs the main() of the code
if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()



