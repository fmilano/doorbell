# Rings the Grundig doorbell by driving to zero volts one of the pushbuttons
# contacts.

# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
doorbell_pin = 23 # Broadcom pin 23 (P1 pin 16)


def init():
    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # use Broadcom numbering
    GPIO.setup(doorbell_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    print("Init: pin 23 as input (floating/high impedance)")


def term():
    GPIO.cleanup()    

def ring():

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # use Broadcom numbering
    GPIO.setup(doorbell_pin, GPIO.OUT) # doorbell pin set as output
    # Output to 3.3V
    GPIO.output(doorbell_pin, GPIO.HIGH)
    print("Ring: drive pin 23 to 3.3V")
    #Output to 0V
    GPIO.output(doorbell_pin, GPIO.LOW)
    print("Ring: drive pin 23 to 0V")
    time.sleep(1)
    GPIO.setup(doorbell_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    print("Ring: pin 23 as input (floating/high impedance)")

  
