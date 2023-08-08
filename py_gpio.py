from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
leds = [26, 19, 13, 6, 5, 11, 9, 10]
for l in leds:
    GPIO.setup(l, GPIO.IN)
    if GPIO.input(l):
        print('Input was HIGH')
    else:
        print('Input was LOW')
for l in leds:
    GPIO.setup(l, GPIO.IN)
    print(GPIO.input(l))
    GPIO.setup(l, GPIO.OUT)
    GPIO.output(l, 0)
    sleep(0.1)
    GPIO.output(l, 1)
    sleep(0.1)
    GPIO.output(l, 0)
    sleep(0.3)
    GPIO.output(l, 1)
    sleep(0.1)
    GPIO.output(l, 0)
    sleep(0.4)
    GPIO.output(l, 1)
    sleep(0.2)
    GPIO.output(l, 0)
    sleep(0.2)
    GPIO.output(l, 1)
    sleep(0.3)
    GPIO.output(l, 0)
GPIO.cleanup()
#    led = LED(l)
#    led.off()
#    sleep(0.1)
#    led.on()
#    sleep(0.1)
#for l in leds:
#    led = LED(l)
#    led.off()
#    sleep(0.2)
#    led.on()
#    sleep(0.2)
