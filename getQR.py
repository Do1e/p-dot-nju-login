import requests
import time
import cv2
import numpy as np

import config

class QR:
    def __init__(self, session: requests.session) -> None:
        self.session = session

    def getQR(self) -> np.ndarray:
        self.ts = int(time.time()*1000)
        url = config.QRidURL % self.ts
        self.QRid = self.session.get(url, timeout=config.getTimeout).text
        url = config.QRURL % self.QRid
        QRdata = self.session.get(url, timeout=config.getTimeout).content
        self.QR =  cv2.imdecode(np.frombuffer(QRdata, np.uint8), cv2.IMREAD_COLOR)

    def printQR(self) -> None:
        self.getQR()
        char_full = '\u2588'
        char_up = '\u2580'
        char_down = '\u2584'
        QR = self.QR[6:-6, 6:-6]
        for i in range(0, QR.shape[0]-3, 6):
            for j in range(0, QR.shape[1], 3):
                if QR[i, j, 0] < 128 and QR[i+3, j, 0] < 128:
                    print(char_full, end='')
                elif QR[i, j, 0] < 128 and QR[i+3, j, 0] >= 128:
                    print(char_up, end='')
                elif QR[i, j, 0] >= 128 and QR[i+3, j, 0] < 128:
                    print(char_down, end='')
                else:
                    print(' ', end='')
            print('')
        for j in range(0, QR.shape[1], 3):
            if QR[-1, j, 0] < 128:
                print(char_up, end='')
            else:
                print(' ', end='')
        print('')

if __name__ == '__main__':
    session = requests.session()
    session.headers = config.headers
    qr = QR(session)
    qr.printQR()