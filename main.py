from apscheduler.schedulers.background import BlockingScheduler
import serial

unaRisposta = bytearray(b'S01U\x10\x00\x002S02U\x10\x00\x002S03U\x10\x00\x002S04\x00\x00\x00\x002S05\x00\x00\x00\x002S06\x00\x00\x00\x002S07\x00\x00\x00\x002S08\x00\x00\x00\x002S09\x00\x00\x00\x002S10\x00\x00\x00\x002S11\x00\x00\x00\x002S12\x00\x00\x00\x002S13\x00\x00\x00\x002S14\x83p\xa7\x021S150\xd5\x00\x001S16\xff\xff\x00\x002e')
unaRisposta = bytearray(b'S01U\x10\x00\x002S02U\x10\x00\x002S03U\x10\x00\x002S04\x00\x00\x00\x002S05\x00\x00\x00\x002S06\x00\x00\x00\x002S07\x00\x00\x00\x002S08\x00\x00\x00\x002S09\x00\x00\x00\x002S10\x00\x00\x00\x002S11\x00\x00\x00\x002S12\x00\x00\x00\x002S13\x00\x00\x00\x002S14\x83p\x8f\x031S150\xd5%\x031S16\xff\xff\x00\x002v')
unaRisposta = bytearray(b'S01U\x10\x00\x002S02U\x10\x00\x002S03U\x10\x00\x002S04\x00\x00\x00\x002S05\x00\x00\x00\x002S06\x00\x00\x00\x002S07\x00\x00\x00\x002S08\x00\x00\x00\x002S09\x00\x00\x00\x002S10\x00\x00\x00\x002S11\x00\x00\x00\x002S12\x00\x00\x00\x002S13\x00\x00\x00\x002S14\x83p|\x031S150\xd5\x19\x041S16\xff\xff\x00\x002X')

requestValues = [170, 2, 0, 173]
requestBytes = bytes(requestValues)
store = ""


def request():
    ser.write(requestBytes)


def read():
    buffer = bytearray()
    while len(buffer)<129:
        buffer += bytearray(ser.read(size=129))
    return buffer
    # responseBytearray = ser.read(size=129, timeout=1)


def extractConsProd(bytes):
    pass


def requestAndRead():
    ser.reset_input_buffer() #test whether it is needed
    request()
    response = read()
    return response


def mainJob():
    unaRisposta = requestAndRead()
    consumo, produzione = capisciRisposta(unaRisposta)
    differenza = produzione - consumo
    print(f"Il consumo è {consumo}")
    print(f"La produzione è {produzione}")
    print(f"Netto: {'+' + str(differenza) if differenza >= 0 else differenza}")


def startScheduler(interval):
    scheduler = BlockingScheduler()
    scheduler.add_job(mainJob, 'interval', seconds=interval)
    scheduler.start()


def capisciRisposta(risposta):
    """_summary_

    Args:
        risposta (bytearray): risposta del monitor
    Returns (consumption, production)
    """    
    consumptionOffset = 13*8
    productionOffset = 14*8
    consLine = risposta[consumptionOffset:consumptionOffset+8]
    prodLine = risposta[productionOffset:productionOffset+8]
    return getValue(consLine), getValue(prodLine)


def getValue(line):
    return line[6] << 8 | line[5]


def main():
    global ser
    ser = serial.Serial('COM4')
    startScheduler(5)


if __name__ == "__main__":
    main()
