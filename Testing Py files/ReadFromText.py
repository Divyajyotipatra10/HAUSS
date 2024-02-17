# Read from the text file and assign values to variables
temperature = None
humidity = None
pressure = None
location = None

with open('data.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(': ')
        if key == 'Temperature':
            temperature = float(value)
        elif key == 'Humidity':
            humidity = float(value)
        elif key == 'Pressure':
            pressure = float(value)
        elif key == 'Location':
            location = value

# Print the values
print('Temperature:', temperature)
print('Humidity:', humidity)
print('Pressure:', pressure)
print('Location:', location)

