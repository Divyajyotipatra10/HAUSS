import machine
import time
import ubluetooth

message = ""
reset_button_pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
long_press_duration = 4  # 5 seconds
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

#def buttons_irq(pin):
#    led.value(not led.value())
#    ble.send('LED state will be toggled.')
#    print('LED state will be toggled.')   
#but.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttons_irq)
y=0
x=[] #list to append variables
#ble.send('Enter the Credentials in following order:-\nUsername\nSSID\nSSID Password')
while True:
    #ble.send('Enter the Credentials in following order:-\nUsername\nSSID\nSSID Password')
    #taking credentials from the user and Generating a text file for the SAME
    while message:
        if message=="Credentials":
            ble.send('Enter the Credentials in following order:-\nUsername\nSSID\nSSID Password')
            message==""
        x.append(message)
        if len(x)==4:
            ble.send('Do you want to change anything\nPress 1 for username\nPress 2 for SSID\nPress 3 for SSID Password\Press 4 for okay with current data')     
            checkstatus=message        
            if checkstatus==1:
                ble.send('Enter Username')
                x[1]=message
            elif checkstatus==2:
                ble.send('Enter SSID')
                x[2]=message
            elif checkstatus==3:
                ble.send('Enter SSID Password')
                x[3]=message
            else:
                ble.send('Data Uploaded To the server')
            # Create a text file and store data
                with open('data.txt', 'w') as file:
                    file.write(x[1]+'\n')
                    file.write(x[2]+'\n')
                    file.write(x[3]+'\n')
                    y=len(x)
                    x=[]
            #file.write('Location: Home\n')
        message=""
    time.sleep_ms(100)
    if y==4:
        print("Program Terminated")
        ble.cleanup()
        break
# Open the file in write mode, which truncates the file
try:
    while True:
        # Check if the reset button is pressed for 5 seconds consecutively
        start_time = time.time()
        pressed_count = 0
        while time.time() - start_time < long_press_duration:
            if reset_button_pin.value() == 0:
                pressed_count += 1
                if pressed_count >= long_press_duration * 10:  # Sampling every 0.1 seconds
                    print("Reset button pressed for 5 seconds consecutively!")
                    with open('data.txt', 'w') as file:
                        pass  # Do nothing inside the block

                    break
            else:
                pressed_count = 0
            time.sleep(0.1)  # Sampling interval
except KeyboardInterrupt:
    print("Program terminated.")
# File content is now deleted

    
    
