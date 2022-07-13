import multiprocessing
import RPi.GPIO as GPIO
import time

from data.sensorInference import SensorInference

class SensorStream:

    # init and read one frame
    def __init__(self, tcp):
        self.GPIO_TRIGGER = 23
        self.GPIO_ECHO = 24
        self.distance = 0
        self.tcp = tcp

    def startAsProcess(self):
        print("Sensor Stream Process started")
        self.gpioSetup()

        #self.sensorProcess = multiprocessing.Process(target=self.distance)
        self.sensorProcess = multiprocessing.Process(target=self.dummyDistance, args=(self.tcp,))
        self.sensorProcess.start()
        return self

    def gpioSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    # Get distance from ultrasonic sensor
    def Distance(self, tcp):
        while True:
            GPIO.output(self.GPIO_TRIGGER, True)
            time.sleep(0.0001)
            GPIO.output(self.GPIO_TRIGGER, False)

            while not GPIO.input(self.GPIO_ECHO):
                pass

            StartTime = time.time()

            while GPIO.input(self.GPIO_ECHO):
                pass

            StopTime = time.time()

            TimeElapsed = StopTime - StartTime
            self.distance = (TimeElapsed * 0.034) / 2
            self.sensorInference = SensorInference("real ultrasonic sensor")
            self.sensorInference.addData(self.distance)
            tcp.sendData(self.sensorInference)

            print(f"sensor time: {TimeElapsed}")
            time.sleep(0.3)

    # Get dummy distance from ultrasonic sensor
    def dummyDistance(self, sensorQueue):
        while True:
            self.distance = 20
            if sensorQueue.empty():
                sensorQueue.put(self.distance)
            time.sleep(0.3)
