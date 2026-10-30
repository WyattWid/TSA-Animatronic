from pyfirmata import Arduino, util
import time

class Transistors:
    def __init__(self):
        self.board = Arduino('/dev/ttyACM0')
        #self.light_pin = self.board.get_pin('d:13:o')
        #self.pump_pin = self.board.get_pin('d:12:o')
        #self.valve_pin = self.board.get_pin('d:11:o')
        #self.qr_light_pin = self.board.get_pin('d:9:o')
        self.pumping = False
    def qr_light(self, state):
        self.qr_light_pin.write(state)
        print("qr code is " + str(state))
    def qr_light_flash(self):
        for i in range(10):
            self.qr_light(1)
            time.sleep(.3)
            self.qr_light(0)
            time.sleep(.3)
            
    def light(self, state):
        self.light_pin.write(state)
    def pump(self, state):
        self.pump_pin.write(state)
    def start_pump(self):
        self.pumping = True
        print("started pumping")
        self.pump(1)
        time.sleep(15)
        print("stopped pumping")
        self.pump(0)
        self.pumping = False
    def valve(self, state):
        self.valve_pin.write(state)
    def initial(self):
        while self.pumping:
            time.sleep(.01)
        self.valve(1)
        time.sleep(1)
        self.valve(0)
        self.start_pump()