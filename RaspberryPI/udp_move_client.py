#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import RPi.GPIO as GPIO
import time
import subprocess
import configparser

import socket


class Move_RasberryPI():

    def servo(t):
        if t<21:
            ton=float(0.0001*t)
            toff=0.02-ton
            print(ton)
            print(toff)
            for i in range(10):
                GPIO.output(33,1)
                time.sleep(ton)
                GPIO.output(33,0)
                time.sleep(toff)
            time.sleep(0.5)


         
    def back():
        # message = "maeni susumuyo"
        # subprocess.call(f'/home/pi/aquestalkpi/AquesTalkPi "{message}" | aplay',shell=True)
        GPIO.output(32,1)
        GPIO.output(36,0)
        GPIO.output(38,1)
        GPIO.output(40,0)
        print("BACK")
    

        
    def foreward():
        # message = "watasha segaru"
        # subprocess.call(f'/home/pi/aquestalkpi/AquesTalkPi "{message}" | aplay',shell=True)
        GPIO.output(32,0)
        GPIO.output(36,1)
        GPIO.output(38,0)
        GPIO.output(40,1)
        print("FORWARD")
    

    def right():
        # message = "hidari ikuyo"
        # subprocess.call(f'/home/pi/aquestalkpi/AquesTalkPi "{message}" | aplay',shell=True)

        GPIO.output(32,1)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,1)
        print("RIGHT")
    

    def left():
        # message = "migi ikuyo"
        # subprocess.call(f'/home/pi/aquestalkpi/AquesTalkPi "{message}" | aplay',shell=True)
        GPIO.output(32,0)
        GPIO.output(36,1)
        GPIO.output(38,1)
        GPIO.output(40,0)
        print("LEFT")


    def reset():
        for i in motor_pins:
            GPIO.output(i,0)
        time.sleep(1)
        print("STOP")



    def blink(t):
        for i in range(t):
            GPIO.output(24,1)
            GPIO.output(26,0)
            time.sleep(0.1)
            GPIO.output(24,0)
            GPIO.output(26,0)
            time.slee(0.1)
        print("BLINK")


    # カメラ画質を二倍にするコマンド
    def camera_quality_twice():

        with open(f"{path}/Data/connection.ini","r") as f:
            data = f.read()

        connection_list = data.split('\n')
        num = 0

        for key in connection_list:            
            if key == "image_width = 320":
                connection_list[num] = "image_width = 640"
            elif key == "image_width = 640":
                connection_list[num] = "image_width = 320"
            elif key == "image_height = 240":
                connection_list[num] = "image_height = 480"
            elif key == "image_height = 480":
                connection_list[num] = "image_height = 240"

            num += 1

        arrangement = '\n'.join(connection_list)

        with open(f"{path}/Data/connection.ini","w") as f:
            f.write(arrangement)

        # with open("connection.ini","r") as f:
        #     data = f.read()

        #     print(data)

# RaspberryPIを実際に動かすための関数
def recv_message(message):
    if message == 'front': 
        Move_RasberryPI.foreward()

    elif message == 'back': 
        Move_RasberryPI.back() 

    elif message == 'right':
        Move_RasberryPI.right() 

    elif message == 'left':
        Move_RasberryPI.left() 

    elif message == 'off': 
        Move_RasberryPI.reset()
        with open(f"{path}/Data/juge.txt", "w") as f:
            f.write("off")

    elif message == 'light_on': 
        GPIO.output(24,0)
        GPIO.output(26,1)

    elif message == 'light_off': 
        GPIO.output(24,0)
        GPIO.output(26,0)
    elif message == 'camera_center': 
        Move_RasberryPI.servo(12)

    elif message == 'camera_middle_up': 
        Move_RasberryPI.servo(9)

    elif message == 'camera_up': 
        Move_RasberryPI.servo(6)

    elif message == 'camera_down': 
        Move_RasberryPI.servo(17)

    elif message == 'power_off':
        os.system("sudo poweroff")

    elif message == 'p':
        GPIO.output(12,1)
        GPIO.output(16,1)
        subprocess.call(f"sudo mpg321 {path}/Data/hirameki.mp3",shell=True)
        GPIO.output(12,0)
        GPIO.output(16,0)

    elif message == 'camera_boot':
        os.system("sudo systemctl stop picture.service")

    elif message == 'camera_boot_off':
        os.system("sudo systemctl start picture.service")


    elif message == 'wake_up_camera':
        os.system("sudo systemctl restart picture.service")

    elif message == 'camera_twice':
        Move_RasberryPI.camera_quality_twice()

    else:
        #message="そだてみーる"
        # print(message.encode())
        #  print(mes.encode())
        #   print(f"Unknown Message: {message}")
        os.system(f'{path}/aquestalkpi/AquesTalkPi "{message}" | aplay')
        # print(message)

if __name__ == "__main__":

    M_SIZE = 1024

    path = "/home/pi/RaspberryPI/"

    config = configparser.ConfigParser()
    config.read(f'{path}connection.ini', 'UTF-8')

    # Connection Settings
    SERVER_IP = config.get('server', 'ip')
    SERVER_PORT = int(config.get('server', 'move_port'))
    PRODUCT_NUMBER = config.get('server', 'number')

    pins=[12,16,37,35,33,18,22,24,26,32,36,38,40]
    motor_pins=[18,22,24,26,32,36,38,40]
    url="https://dagri.jp/movebot/api/move.txt"
    GPIO.setmode(GPIO.BOARD)

    for i in pins:
        print(i)
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i,1)
    
    print("ok")
    for i in range (5):
        GPIO.output(12,0)
        GPIO.output(16,1)
        time.sleep(0.2)
        GPIO.output(16,0)
        GPIO.output(12,1)
        time.sleep(0.2)

    first_message="jenny kido shimashita"
    subprocess.call("sudo mpg321 "+path+"/Data/start_sound.mp3",shell=True)
    subprocess.call(f'{path}/AquesTalkPi "{first_message}" | aplay',shell=True)

    # Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
    serv_address = (SERVER_IP, SERVER_PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 最初に受信できるように情報を飛ばす
    send_len = sock.sendto(PRODUCT_NUMBER.encode('utf-8'), serv_address)


    while True:
        try:
            # Serverからのmessageを受付開始
            rx_message, addr = sock.recvfrom(M_SIZE)
            print(f"Server: {rx_message.decode(encoding='utf-8')}")
            recv_message(rx_message.decode(encoding='utf-8'))


        except KeyboardInterrupt:
            print('closing socket')
            sock.close()
            print('done')
            break
