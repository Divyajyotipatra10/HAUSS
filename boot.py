import machine
import time
import ubluetooth

message = ""
EN_PIN = 0  # Define the pin number for the reset pin
reset_pin = machine.Pin(EN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
interrupt_flag = False

# Define the interrupt handler function
def reset_interrupt_handler(pin):
    global interrupt_flag
    interrupt_flag = True
#long_press_duration = 4  # 5 seconds    
class ESP32_BLE():
    def __init__(self, name):
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.timer1 = machine.Timer(0)
        
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.timer1.init(period=2000, mode=machine.Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))
        #self.timer1.deinit()

    def disconnected(self):        
        self.timer1.init(period=100, mode=machine.Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        global message
        
        if event == 1: #_IRQ_CENTRAL_CONNECT:
            self.connected()
        elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
            self.advertiser()
            self.disconnected()
        elif event == 3: #_IRQ_GATTS_WRITE:
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)
            
    def register(self):        
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        try:
            self.ble.gatts_notify(0, self.tx, data + '\n')
        except OSError as e:
            print("Bluetooth error:", e)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray(b'\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")
    def cleanup(self):
        self.ble.active(False)
        self.timer1.init(period=100, mode=machine.Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

led = machine.Pin(2, machine.Pin.OUT)
#but = machine.Pin(0, machine.Pin.IN)
ble = ESP32_BLE("ESP32")
reset_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=reset_interrupt_handler)

# Main loop
start_time = time.ticks_ms()
y=0
topicdetails=0
z=[]#list for topics
x=[] #list to append credentials
# we will take 4 Topics from the User and storing it in a text file
#ble.send('Enter the Credentials in following order:-\nUsername\nSSID\nSSID Password')
while True:
    #ble.send('Enter the Credentials in following order:-\nUsername\nSSID\nSSID Password')
    #taking credentials from the user and Generating a text file for the SAME
    while message:
        if message=="Start":
            ble.send('Enter the Credentials in following order:-\nUsername\nSSID\nSSID Password')
            message==""
        x.append(message)
        seen=set()
        x = [p for p in x if p not in seen and not seen.add(p)]
        if len(x)==9:
            ble.send('Do you want to change anything\nPress 1 for username\nPress 2 for SSID\nPress 3 for SSID Password\nPress 4 for Appliance Name-1:\n5 for 2:\n6 for 3:\n7 for 4:\n8for 5\n9 if okay with current data')
        if len(x)==4:
            ble.send('Enter the Appliance Names in order.Last one should be fan if it is there.')
        if len(x)>=9:
            #ble.send('Do you want to change anything\nPress 1 for username\nPress 2 for SSID\nPress 3 for SSID Password\Press 4 for okay with current data')     
            checkstatus=message
            #print(checkstatus)
            #print(rep)
            if checkstatus=="1":
                message=""
                ble.send('Enter Username')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[1]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="2":
                message=""
                ble.send('Enter SSID')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[2]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="3":
                message=""
                ble.send('Enter SSID Password')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[3]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="4":
                message=""
                ble.send('Enter 1st Application')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[4]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="5":
                message=""
                ble.send('Enter 2nd Application')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[5]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="6":
                message=""
                ble.send('Rename 3rd Application')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[6]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="7":
                message=""
                ble.send('Enter 4th Application')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[7]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="8":
                message=""
                ble.send('Enter 5th Application')
                while message=="":
                    time.sleep(3)
                    #print("Enter Username")
                x[8]=message
                ble.send('Press 9 to Confirm')
            elif checkstatus=="9":
                ble.send('Data Uploaded To the server')
            # Create a text file and store data
                with open('data.txt', 'w') as file:
                    file.write(x[1]+'\n')
                    file.write(x[2]+'\n')
                    file.write(x[3]+'\n')
                    file.write(x[4]+'\n')
                    file.write(x[5]+'\n')
                    file.write(x[6]+'\n')
                    file.write(x[7]+'\n')
                    file.write(x[8]+'\n')
                    y=checkstatus
                    checkstatus=0
            #file.write('Location: Home\n')
        message=""
    time.sleep_ms(100)
    if y=="9":
        print("Program Terminated")
        ble.cleanup()
        break
    if not reset_pin.value():
        if time.ticks_diff(time.ticks_ms(), start_time) >= 5000:
            if interrupt_flag:
                print("Reset pin pressed for 5 seconds. Generating interrupt request.")
                x=[]
                with open('data.txt', 'w') as file:
                    pass  # Do nothing inside the block
                    print("Program Terminated")
                    ble.cleanup()
                    break
                # Perform action for generating interrupt request
                # For example: machine.reset()
            else:
                print("Reset pin not continuously pressed for 5 seconds.")
            # Reset interrupt flag and start time
            interrupt_flag = False
            start_time = time.ticks_ms()
    else:
        #print("Pressed for less than 5 seconds")
        start_time = time.ticks_ms()
# Open the file in write mode, which truncates the file

# File content is now deleted

    #x[len(x)]
    
