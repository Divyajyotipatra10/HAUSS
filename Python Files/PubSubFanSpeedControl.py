import time
import random
import ubinascii
from umqtt.simple import MQTTClient
import machine
import time

# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = "192.168.57.67"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC1 = b"LED_1" #subscriber topic
TOPIC2 = b"LED_2" #subscriber topic
TOPIC3 = b"LED_3" #subscriber topic
TOPIC4 = b"LED_4" #subscriber topic
TOPIC6 = b"LED_ALL" #subscriber topic
TOPIC5 = b"Status" #Publisher topic
TOPIC7 = b"FAN" #subscriber topic
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
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
FAN = machine.Pin(12, machine.Pin.OUT)
fan_pwm = machine.PWM(FAN)

# Define minimum and maximum duty cycle values
min_duty = 0  # 0% duty cycle
max_duty = 1023  # 100% duty cycle

def set_fan_speed(speed_percentage):
    # Convert speed percentage to duty cycle value
    duty_cycle = int((speed_percentage / 100) * max_duty)
    fan_pwm.duty(duty_cycle)
    
set_fan_speed(0)
    
def main():
    global received_message,received_topic
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
    
    LED1 = machine.Pin(15,machine.Pin.OUT)
    LED2 = machine.Pin(2,machine.Pin.OUT)
    LED3 = machine.Pin(5,machine.Pin.OUT)
    LED4 = machine.Pin(18,machine.Pin.OUT)
    
    while True:
        
        if received_message is not None:
            # Process the received message
            #print(received_topic)
            #x=received_message.decode('utf-8') 
            #print(f"Received message: ",x)
            if received_topic == TOPIC1:
                if received_message==b'ON':
                    LED1.value(1)
                    msg1 = "LED 1 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    #msg3=b'ON'
                    #mqttClient.publish(TOPIC11,msg3)
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
            elif received_topic == TOPIC2:
                if received_message==b'ON':
                    LED2.value(1)
                    msg1 = "LED 2 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    #msg3=b'ON'
                    #mqttClient.publish(TOPIC11,msg3)
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
            elif received_topic == TOPIC3:
                if received_message==b'ON':
                    LED3.value(1)
                    msg1 = "LED 3 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    #msg3=b'ON'
                    #mqttClient.publish(TOPIC11,msg3)
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
            elif received_topic == TOPIC4:
                if received_message==b'ON':
                    LED4.value(1)
                    msg1 = "LED 4 is ON"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    #msg3=b'ON'
                    #mqttClient.publish(TOPIC11,msg3)
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
                    #msg2=b'OFF'
                    msg1 = "All LEDs are OFF"
                    print(f"Publishing msg :: {msg1}")
                    mqttClient.publish(TOPIC5, str(msg1).encode())
                    #mqttClient.publish(TOPIC10,msg2)
                    msg3=b'OFF'
                    mqttClient.publish(TOPIC11,msg3)
                    mqttClient.publish(TOPIC1,msg3)
                    mqttClient.publish(TOPIC2,msg3)
                    mqttClient.publish(TOPIC3,msg3)
                    mqttClient.publish(TOPIC4,msg3)
            elif received_topic == TOPIC7:
                    # Read input from user for desired fan speed
                    speed_input = received_message
                    try:
                        # Convert input to integer and ensure it's within range
                        speed = int(speed_input)
                        if 0 <= speed <= 100:
                           set_fan_speed(speed)
                        else:
                           print("Speed must be between 0 and 100")
                    except ValueError:
                        print("Invalid input. Please enter a number between 0 and 100.")
                
            else:
                print("No such Topic Exists");
            # Reset the variable
            received_message = None
            received_topic = None
        # Non-blocking wait for message
        mqttClient.check_msg()
        
        
        
        #mqttClient.publish(TOPIC2, str(random_temp).encode())
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
            
    print("Disconnecting...")
    mqttClient.disconnect()


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()


