import time
import random
import ubinascii
from umqtt.simple import MQTTClient
import machine

# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = "IP address of your device"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC1 = b"LED_ON_OFF" #subscriber topic
TOPIC2 = b"Status" #Publisher topic

# Variable to store the received message
received_message = None

# Ping the MQTT broker since we are not publishing any message
last_ping = time.time()
ping_interval = 60

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    global received_message
    received_message = msg
    print((topic, msg)) #Here we print the name of topic and the message received while subscribing to the topic.

def reset(): #called when esp32 doesn't get connected to the broker for communication
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
def main():
    global received_message
    
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(TOPIC1) #subscribed to the topic we created above.
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")
    LED1= machine.Pin(2,machine.Pin.OUT) #Setting one of the digital pins of the ESP32 to Turn ON/OFF the LED. 
    while True:
        if received_message is not None: #
            # Process the received message
            x=received_message.decode('utf-8') 
            print(f"Received message: ",x)
            if received_message==b'ON': #we are receiving the message in this form, that is why we have kept it in this form only.
                LED1.value(1) #Turning on the digital pin
                msg1 = "LED is ON" #meanwhile publishing the message that shows if LED is on or not.
                print(f"Publishing msg :: {msg1}")
                mqttClient.publish(TOPIC2, str(msg1).encode()) #used the second TOPIC to publish the message on the panel of another device.
            elif received_message==b'OFF':
                LED1.value(0) #Turning off the digital pin. 
                msg1 = "LED is OFF"
                print(f"Publishing msg :: {msg1}")
                mqttClient.publish(TOPIC2, str(msg1).encode())
            else:
                print("Invalid Command")
            # Reset the variable
            received_message = None
            
        # Non-blocking wait for message
        mqttClient.check_msg()
        
        
        
        #mqttClient.publish(TOPIC2, str(random_temp).encode())
        time.sleep(0.5)#delay before going to the next part of the code
        
        # Then need to sleep to avoid 100% CPU usage (in a real
        # app other useful actions would be performed instead)
        global last_ping #basically checking the ping timing to know when was the last time it was accessed
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


