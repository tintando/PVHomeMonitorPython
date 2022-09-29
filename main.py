from socket import timeout
from apscheduler.schedulers.background import BlockingScheduler
import serial

# ser = serial.Serial('/dev/ttyUSB0')
requestValues = [170, 2, 0, 173]
requestBytes = bytes(requestValues)
store = ""


def request():
    ser.write(requestBytes)
#changes

def read():
    return ser.read(size=129, timeout=1)
    # responseBytearray = ser.read(size=129, timeout=1)


def extractConsProd(bytes):
    pass

def requestAndRead():
    ser.reset_input_buffer() #test whether it is needed
    request()
    response = read()


def scheduleTester():
    print("5 seconds have passed")


def startScheduler(interval):
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduleTester, 'interval', seconds=interval)
    scheduler.start()


def main():
    startScheduler(5)


if __name__ == "__main__":
    main()

 
