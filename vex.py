import os
from pyfirmata import Arduino , util
import time

class Vex:
    def __init__(self):
        self.board = Arduino('/dev/ttyACM0')
        self.motors = []
        self.motor_states = []

    def assign_motor(self, in1, in2):
        IN1 = self.board.get_pin(f'd:{in1}:p')
        IN2 = self.board.get_pin(f'd:{in2}:o')
        self.motors.append([IN1, IN2])
        self.motor_states.append(0)

    def run(self, motor_id: int, cycles: int, speed: float, delay: float, direct: int):
        if self.motor_states[motor_id] == 0:
            self.motor_states[motor_id] = 1
        try:
            IN1, IN2 = self.motors[motor_id]
            for i in range(cycles):
                i = i + direct
                if i % 2 == 1:
                    temp = 1 - speed
                else:
                    temp = speed
                IN1.write(temp)
                IN2.write(i % 2)
                
                time.sleep(delay)
            IN1.write(0)
            IN2.write(0)
            self.motor_states[motor_id] = 1
        except Exception as e:
            print(f"Error: {e}")
        finally:
            IN1.write(0)
            IN2.write(0)
    def stop(self):
        for i in range(len(self.motors)):
            IN1, IN2 = self.motors[i]
            IN1.write(0)
            IN2.write(0)
    def stop_motor(self, i):
        IN1, IN2 = self.motors[i]
        IN1.write(0)
        IN2.write(0)
    def test(self, motor_id, speed, in1, in2):
        IN1 = self.board.get_pin(f'd:{in1}:p')
        IN2 = self.board.get_pin(f'd:{in2}:o')
        #self.motors.append([IN1, IN2])
        #IN1, IN2 = self.motors[motor_id]
        print("Testing forward direction...")
        IN1.write(speed)  # Set IN1 high
        IN2.write(0)  # Set IN2 low
        time.sleep(2)  # Run for 2 seconds
        IN1.write(0)  # Stop motor
        IN2.write(0)
        time.sleep(1)  # Pause for 1 second
        
        # Test Backward (direct = -1)
        print("Testing backward direction...")
        speed=1-speed
        IN1.write(speed)  # Set IN1 low
        IN2.write(1)  # Set IN2 high
        time.sleep(20000)  # Run for 2 seconds
        IN1.write(0)  # Stop motor
        IN2.write(0)
    

