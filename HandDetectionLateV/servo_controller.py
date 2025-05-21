import RPi.GPIO as GPIO
import time

class ServoController:
    def __init__(self, pin=12):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0)

    def set_angle(self, angle):
        duty = 2.5 + (angle / 180.0) * 10
        self.servo.ChangeDutyCycle(duty)
        time.sleep(0.05)

    def stop(self):
        self.servo.ChangeDutyCycle(0)

    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup()
        