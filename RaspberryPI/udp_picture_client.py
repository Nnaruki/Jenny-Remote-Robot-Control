import socket
import configparser
import logging
import time
import cv2
import sys
import cv2




if __name__ == '__main__':

    path = "/home/pi/RaspberryPI/"

    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read(f'{path}connection.ini', 'UTF-8')

    # Connection Settings
    SERVER_IP = config.get('server', 'ip')
    SERVER_PORT = int(config.get('server', 'picture_port'))
    PRODUCT_NUMBER = config.get('server', 'number')

    # Image Settings
    IMAGE_WIDTH = int(config.get('packet', 'image_width'))
    IMAGE_HEIGHT = int(config.get('packet', 'image_height'))
    IMAGE_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT // 2
    logging.info(" IMAGE SIZE: " + str(IMAGE_SIZE))

    capture=cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,IMAGE_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,IMAGE_HEIGHT)


    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(PRODUCT_NUMBER.encode(), (SERVER_IP, SERVER_PORT))

        judge = True

        try:  
                  
            while (True):

                if judge is True:
                    retval, img = capture.read()
                    retval, jpg = cv2.imencode('.jpg',img,[int(cv2.IMWRITE_JPEG_QUALITY),90])                                 
                    data_size = sys.getsizeof(jpg)
                    # print(data_size)
                    s.sendto(jpg, (SERVER_IP, SERVER_PORT))
                else:
                    time.sleep(3)

        except KeyboardInterrupt:
            pass

        finally:
            capture.release()


