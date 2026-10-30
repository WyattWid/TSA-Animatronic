# TSA Animatronic

## Overview

This project was created for the Technology Student Association (TSA) Animatronics competition. Our team designed an interactive library exhibit intended to encourage younger students to read.

The exhibit features a talking duck that responds when students scan QR codes attached to books. Each QR code triggers corresponding dialogue from the duck, bringing the library display to life. The project combines programming, electronics, mechanical systems, and interactive elements.

## How It Works

A Raspberry Pi runs the main Python program, handling QR code scanning, audio playback, sensor input, and coordination of the animatronic mechanisms. An Arduino-compatible board communicates with the Raspberry Pi through Firmata to control physical inputs and outputs.

The exhibit includes several moving mechanisms:

- Talking duck: A servo controls the duck's mouth, with movement synchronized to its speech. Another motor controls its wings.
- Dragonfly: A motor moves a dragonfly around the exhibit to simulate flight.
- Hydraulic turtle: A motor pushes a plunger that operates the turtle's hydraulic mechanism.
- Frog: A pneumatic pump and valve cause the frog's tongue, made from a party blower, to extend.

The system also uses sensors and a camera to respond to activity around the exhibit.

## My Contributions

I was the primary programmer and electrical systems designer for the project. I developed the Python software that coordinated the exhibit's interactions, integrated the QR code scanning system, and worked on controlling the motors, sensors, audio, and other electrical components.

The project was a team effort. The dialogue was written collaboratively, and the duck's voice recordings were provided by someone outside the team.

## Hardware

- Raspberry Pi
- Arduino-compatible microcontroller
- Motors and servos
- Hydraulic mechanism
- Pneumatic pump and valve
- Camera and QR code scanning system
- Infrared and ultrasonic sensors
- Electrical components and wiring

## Software and Libraries

- Python
- OpenCV
- pyzbar
- NumPy
- pyFirmata
- RPi.GPIO
- Pydub
- Simpleaudio
- PySerial
- Threading

## System Architecture

The Raspberry Pi handles the main program and higher-level logic, including camera processing, QR code recognition, audio playback, and coordination of the different mechanisms. The Arduino-compatible board handles physical inputs and outputs through Firmata, allowing the Raspberry Pi to control the exhibit's hardware.

