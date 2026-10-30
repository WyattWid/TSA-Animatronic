import os
import serial
import numpy as np
from pydub import AudioSegment
import simpleaudio as sa
import RPi.GPIO as GPIO
from threading import Thread
import time

class Mouth:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
        # Define the servo control pin (use pin 9 for the servo, or adjust as necessary)
        self.servo_pin = 22
        GPIO.setup(self.servo_pin, GPIO.OUT)
        
        # Initialize the PWM control for the servo pin
        self.servo_pwm = GPIO.PWM(self.servo_pin, 50)  # 50 Hz is typical for servos
        self.servo_pwm.start(12)
        self.audio_running = False
                
        self.dict={}
        self.make_audio("/home/wpwidows/Downloads/Fish1.m4a")
        self.make_audio("/home/wpwidows/Downloads/WelcomeToLibrary.m4a")
        self.make_audio("/home/wpwidows/Downloads/JokeDuckLibrary.m4a")
        self.make_audio("/home/wpwidows/Downloads/Ping1.m4a")
        self.make_audio("/home/wpwidows/Downloads/JokeLibraianSlip.m4a")
        self.make_audio("/home/wpwidows/Downloads/FrogBog1.m4a")
        self.make_audio("/home/wpwidows/Downloads/Yertle1.m4a")
        self.make_audio("/home/wpwidows/Downloads/WingsTricky.m4a")
        self.make_audio("/home/wpwidows/Downloads/LoveTheLibrary.m4a")
        self.make_audio("/home/wpwidows/Downloads/QuackstroidinaryQR.m4a")
        self.make_audio("/home/wpwidows/Downloads/Ugly Duckling.m4a")
        self.make_audio("/home/wpwidows/Downloads/BooksHome.m4a")
        self.make_audio("/home/wpwidows/Downloads/ScanQRCode.m4a")
        self.make_audio("/home/wpwidows/Downloads/HungryCatepillar.m4a")
        self.make_audio("/home/wpwidows/Downloads/BooksSlowFast.m4a")
        self.make_audio("/home/wpwidows/Downloads/Froggy.m4a")
        self.make_audio("/home/wpwidows/Downloads/QuacktasticToSeeYou.m4a")
        self.make_audio("/home/wpwidows/Downloads/latenight-pond-32011-fsclips-17295 - Copy (1).mp3", -1)
        self.make_audio("/home/wpwidows/Downloads/beep.mp3")
    def make_audio(self, link, volume_db=2):
        linkname = link.split("/")
        linkname = linkname[-1]
        audio = self.get_audio(link)
        audio = audio + volume_db  # Increase volume by 'volume_db' dB
        self.dict[linkname] = audio
    def control_servo(self, angle):
        """Move the servo to a specific angle (0 to 180 degrees)."""
        # Convert angle (0-180 degrees) to duty cycle (0-100%)
        duty_cycle = (angle / 18) + 2  # 0 degrees corresponds to 2%, 180 degrees corresponds to 12%
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        #print(f"Servo moved to {angle} degrees")

    def stop_servo(self):
        """Stop the servo by setting PWM duty cycle to 0%."""
        self.servo_pwm.ChangeDutyCycle(0)
        print("Servo stopped")

    def stop(self):
        """Cleanup GPIO when done."""
        self.servo_pwm.stop()
        GPIO.cleanup()
    def get_average_audio_volume(self, audio):
        # Step 1: Get the samples and calculate the overall average volume
        samples = np.array(audio.get_array_of_samples())
        overall_avg = np.mean(np.abs(samples))  # Calculate overall average volume
    
        # Step 2: Filter samples that have a volume greater than the overall average
        filtered_samples = samples[np.abs(samples) > overall_avg]
    
        # Step 3: Calculate the new average volume of the filtered samples
        if len(filtered_samples) > 0:
            avg_volume_above_average = np.mean(np.abs(filtered_samples))
        else:
            # In case no samples are above the overall average
            return 0
        filtered_samples = samples[np.abs(samples) > avg_volume_above_average]
    
        # Step 3: Calculate the new average volume of the filtered samples
        if len(filtered_samples) > 0:
            avg_volume_above_average = np.mean(np.abs(filtered_samples))
            return avg_volume_above_average
        else:
            # In case no samples are above the overall average
            return 0

    def get_audio(self, link):
        return(AudioSegment.from_file(link))

    def get_audio_volume(self, audio):
        samples = np.array(audio.get_array_of_samples())
        return np.max(np.abs(samples))
       
    def control_servo_based_on_audio(self, audio_name):
           
        audio = self.dict[audio_name]
        if not audio:
            print("No audio loaded!")
            return
        avg_volume = (self.get_average_audio_volume(audio))
        sample_rate = 85
        for i in range(0, len(audio), sample_rate):
            init = time.time()
            segment = audio[i:i+sample_rate]
            volume = self.get_audio_volume(segment)
           
            if volume > avg_volume:
                self.control_servo(150)
            else:
                self.control_servo(170)

            while (time.time() - init) < ((sample_rate-3)/1000):
                time.sleep(.001)
    def test(self):
        while True:
            self.servo_pin.write(int(input("angle: ")))
    def play_audio(self, audio_name):
        audio = self.dict[audio_name]
        if audio:
            play_obj = sa.play_buffer(
                audio.raw_data,
                num_channels=audio.channels,
                bytes_per_sample=audio.sample_width,
                sample_rate=audio.frame_rate
            )
            play_obj.wait_done()

   
    def talk(self, audio_name):
        while self.audio_running:
            time.sleep(1)
        self.audio_running = True
        audio_thread = Thread(target=lambda: self.play_audio(audio_name))
        thread = Thread(target=lambda: self.control_servo_based_on_audio(audio_name))
        thread.start()
        audio_thread.start()
        thread.join()
        audio_thread.join()
        self.audio_running = False