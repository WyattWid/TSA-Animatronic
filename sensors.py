from pyfirmata import Arduino, util
import time
import RPi.GPIO as GPIO

class Sensors:
    def __init__(self):
        self.board = Arduino('/dev/ttyACM0')
        
        util.Iterator(self.board).start()
        self.ir = self.board.get_pin('d:13:i')
        self.TRIG = 17  # GPIO pin connected to the Trig pin of the ultrasonic sensor
        self.ECHO = 27  # GPIO pin connected to the Echo pin of the ultrasonic sensor
       
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(self.TRIG, GPIO.OUT)  # Set the Trig pin as an output
        GPIO.setup(self.ECHO, GPIO.IN)
       
        self.previous_distance = 0
        self.distance = 0
    def get_ir(self):
        return (self.ir.read())
    def get_distance(self):
        print("point 1")
        list1 = []
        for i in range(10):
            print("1:point " + str(i+2))
            GPIO.output(self.TRIG, False)
            time.sleep(0.0001)  # Wait for the sensor to settle

    # Send a pulse to the Trig pin to start the measurement
            GPIO.output(self.TRIG, True)
            time.sleep(0.00001)  # Keep the pulse high for 10 microseconds
            GPIO.output(self.TRIG, False)
        
        # Measure the time it takes for the pulse to return to the Echo pin
            timeout = time.time() + .05
            while GPIO.input(self.ECHO) == 0 and time.time()  < timeout:
                pulse_start = time.time()
            if time.time()  >= timeout:
                return self.previous_distance
            timeout = time.time() + .05
            while GPIO.input(self.ECHO) == 1 and time.time()  < timeout:
                pulse_end = time.time()
            if time.time()  >= timeout:
                return self.previous_distance
            print("2:point " + str(i+2))
        # callablelculate the duration of the pulse
            pulse_duration = pulse_end - pulse_start
        
            # Calculate the distance using the speed of sound (34300 cm/s)
            self.distance = pulse_duration * 17150  # Divide by 2 because the signal travels to the object and back
            self.distance = round(self.distance, 2)  # Round the result to two decimal places
            self.previous_distance = self.distance
            list1.append(self.distance)
            print("3:point " + str(i+2))
        print("point 3")
        self.distance = sum(list1)/len(list1)
        self.previous_distance = self.distance
        print(self.distance)
        return self.distance
    
