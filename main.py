import os
import threading
from camera import Camera
from mouth import Mouth
from vex import Vex
from transistors import Transistors
from sensors import Sensors
import time
from pyfirmata import Arduino, util
import atexit
import serial.tools.list_ports

class Animatronic:

    def __init__(self):
        self.camera = Camera()
        self.vex = Vex()
        self.mouth = Mouth()
        self.transistors = Transistors()
        self.sensors = Sensors()
        self.board = Arduino(self.check_arduino())
        
        #wings
        self.vex.assign_motor('10', '8')
        #dragonfly
        self.vex.assign_motor('3', '2')
        #turtle
        self.vex.assign_motor('6', '7')
        #dragonfly
        self.vex.assign_motor('5', '4')
        self.cam_dif = True
        self.stop_all = False
        self.transistors.qr_light(1)
        thread7=threading.Thread(target=self.check_dif)
        thread7.start()
        self.pause_all()
        
        thread2=threading.Thread(target=self.check_ir)
        self.duck_line_thread=threading.Thread(target=self.duck_line)
        
        thread2.start()
        self.duck_line_thread.start()
        thread4=threading.Thread(target=self.turtle2)
        thread5=threading.Thread(target=self.background)
        thread4.start()
        thread5.start()
        thread6=threading.Thread(target=self.scan)
        thread6.start()
    def check_dif(self):
        self.last_frame = self.camera.get_frame()
        self.init_time = time.time()
        while True:
            frame = self.camera.get_frame()
            if self.last_frame is not None and frame is not None:
                if self.camera.get_difference(frame, self.last_frame):
                    if ((time.time() - self.init_time)>240) or self.cam_dif:
                        if self.cam_dif:
                            self.cam_dif = True
                            
                        else:
                            self.cam_dif = True
                            thread=threading.Thread(target=self.pause_all)
                            thread.start()

                else:
                    self.init_time = time.time()
                    self.cam_dif = False
            self.last_frame = frame
    def pause_all(self):
        print("paused")
        #pause duck
        self.mouth.audio_running = True
        #pause fish
        #pause turtle
        self.stop_all = True
        #pause dragonfly
        self.vex.stop_motor(1)
        #deactivate transistors
        self.transistors.pumping=True
        self.transistors.light(0)
        while self.cam_dif:
            self.mouth.audio_running = True
            time.sleep(.1)
            print("waiting")
        self.resume_all()
    def resume_all(self):
        print("unpause")
        #unpause duck
        self.mouth.audio_running = False
        #unpause fish
        #unpause turtle
        self.stop_all = False
        #unpause dragonfly
        thread1=threading.Thread(target=self.vex.run, args=(1, 1, 0.45, 210000, 0))
        thread1.start()
        #activate transistors
        self.transistors.pumping=False
        self.transistors.light(1)
    def scan(self):
        while True:
            scanned = self.camera.scan()
            if not scanned == None:
                try:
                    print("will talk")
                    thread1=threading.Thread(target=self.mouth.play_audio, args=("beep.mp3",))
                    thread2=threading.Thread(target=self.transistors.qr_light_flash)
                    thread1.start()
                    thread2.start()
                    thread1.join()
                    thread2.join()
                    
                    
                    self.mouth.talk(scanned)
                    print("done")
                    scanned = None
                    time.sleep(1)
                except Exception as e:
                    print("Book Doesn't Exist")
    def wings(self, motor_id: int, cycles: int, speed: float, delay: float, direct: int):
        if self.mouth.audio_running:
            time.sleep(.1)
        self.vex.run(motor_id, cycles, speed, delay, direct)
    def duck_line(self):
        self.wings(0, 1, 0.6, 2, 1)
        self.wings(0, 1, 0.6, 1.5, 1)
        self.wings(0, 3, 0.6, .5, 0)
        self.mouth.talk("QuacktasticToSeeYou.m4a")
        time.sleep(10)
        self.mouth.talk("ScanQRCode.m4a")
        time.sleep(2)
        self.mouth.talk("JokeLibraianSlip.m4a")
        self.wings(0, 4, 0.6, .5, 0)
        time.sleep(5)
        self.mouth.talk("Ugly Duckling.m4a")
        self.wings(0, 4, 0.6, .5, 0)
        time.sleep(5)
        self.mouth.talk("QuackstroidinaryQR.m4a")
        self.wings(0, 4, 0.6, .7, 0)
        time.sleep(2)
        self.mouth.talk("HungryCatepillar.m4a")
        time.sleep(10)
        self.mouth.talk("BooksSlowFast.m4a")
    def background(self):
        while True:
            if not self.stop_all:
                self.mouth.play_audio("latenight-pond-32011-fsclips-17295 - Copy (1).mp3")
    def check_arduino(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'ttyACM' in port.device:
                return port.device
        raise IOError("arduino not found")
    def turtle2(self):
        self.vex.run(2, 1, 0.5, 2.2, 1)
        time.sleep(10)
        while True:
            if not self.stop_all:
                self.vex.run(2, 1, 0.5, 1.8, 0)
                time.sleep(10)
                self.vex.run(2, 1, 0.5, 1.8, 1)
                time.sleep(10)
    def check_distance(self):
        
        if not self.transistors.pumping:
            self.previous_distance=self.sensors.previous_distance
            if self.sensors.previous_distance == 0:
                print("it is 0")
                thread1=threading.Thread(target=self.transistors.start_pump)
                thread2=threading.Thread(target=self.transistors.initial)
                thread1.start()
                thread2.start()
                thread1.join()
                thread2.join()
                self.sensors.get_distance()
            elif ((self.previous_distance - self.sensors.get_distance()))>(self.previous_distance/5):
                print("greater")
                if ((self.previous_distance - self.sensors.get_distance()))>(self.previous_distance/5):
                    print("greater again")
                    if ((self.previous_distance - self.sensors.get_distance()))>(self.previous_distance/5):
                        print("even greater again")

                        self.transistors.valve(1)
                        time.sleep(.8)
                        self.transistors.valve(0)
                        thread1=threading.Thread(target=self.transistors.start_pump)
                        thread1.start()
                        thread1.join()
                        self.sensors.get_distance()
                        print("greater_all_through")
    def check_ir(self):
        while True:
            time.sleep(15)
            if not self.stop_all:
                self.vex.run(3, 1, 0.4, 1.115, 0)
                state = self.sensors.get_ir()
                if state is None:
                    print("none")
                elif state:
                    g=1
                    #print(state)
                    
                else:
                    time.sleep(.01)
                    state = self.sensors.get_ir()
                    if not state:                
                        #beam broken
                        print(state)
                        #self.vex.stop_motor(3)
                        #time.sleep(15)
                        #self.vex.run(3, 1, 0.4, .7, 0) 
                        #thread1=threading.Thread(target=self.vex.run, args=(3, 1, 0.4, 1, 0))
                        #thread1.start()
    def cleanup(self):
        self.board.exit()
    def basic_functions(self):
        try: 
            while True:
                try:
                    self.check_distance()
                    time.sleep(0.1)
                    
                    
                except UnboundLocalError:
                    print("hi")
        except KeyboardInterrupt:
            self.transistors.pump(0)
            self.transistors.valve(0)
            self.transistors.light(0)
            self.transistors.qr_light(0)
            self.vex.stop()
            atexit.register(self.cleanup)
            

if __name__ == '__main__':
        an = Animatronic()
        an.basic_functions()
        