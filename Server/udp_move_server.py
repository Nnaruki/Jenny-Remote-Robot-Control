
import socket
import time
import threading
import configparser


M_SIZE = 1024

path = "./"

config = configparser.ConfigParser()
config.read(f'{path}connection.ini', 'UTF-8')

# Connection Settings
SERVER_IP = config.get('server', 'ip')
SERVER_PORT = int(config.get('server', 'udp_move_port'))

locaddr = (SERVER_IP, SERVER_PORT)

# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
print('create socket')

# ②自ホストで使用するIPアドレスとポート番号を指定
sock.bind(locaddr)



while True:
    
    try :
        # ③Clientからのmessageの受付開始
        print('Waiting message')
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(f'Received message is [{message}]')

        # Clientが受信待ちになるまで待つため
        time.sleep(1)

        # messageを送信
        def send_message(message,cli_addr):

            num = 0
            judge_past = None

            try:

                while num<100*60*10: #10分操作がなかったら終了
                    with open(f"{path}Data/{message[1:5]}_move.txt", "r") as f:
                        judge = f.read()
                    # judge = "test"

                    if judge != judge_past and len(judge) > 0:
                        # message = input(f"{cli_addr}:")
                        # print(cli_addr)
                        sock.sendto(judge.encode(encoding='utf-8'), cli_addr)
                        judge_past = judge
                        print(judge)
                        num = 0

                    else:
                        time.sleep(0.01)
                        num += 1
                        # print(num)
                else:
                    print("break")

            except KeyboardInterrupt:
                print ('\n . . .\n')
                sock.close()
                

        send_picture = threading.Thread(target=send_message, args=(message,cli_addr,))
        send_picture.start()

    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
        break