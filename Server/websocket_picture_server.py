from websocket_server import WebsocketServer
import logging
import base64
import threading
import configparser
import logging

class Websocket_Server():

    def __init__(self, host, port):
        self.server = WebsocketServer(port, host=host)

        self.connection_server_to_raspberrypi = {

            "TEST":None, # Global Server IP スマホとかで見たときに格納
            "SAMP":None
        }
        

    # クライアント接続時に呼ばれる関数
    def new_client(self, client, server):
        print("OK")


    # クライアント切断時に呼ばれる関数
    def client_left(self, client, server):

        # 辞書型のKeyのみを取り出す
        def get_keys_from_value(d, val):
            key = [k for k, v in d.items() if v == val][0]
            return str(key)

        # Client情報に送られてきたデータの送信先があれば実行
        if client in self.connection_server_to_raspberrypi.values():
            key = get_keys_from_value(self.connection_server_to_raspberrypi,client)
            with open(f"/Library/WebServer/Documents/Web2/{key}.txt","w") as f:
                f.write("STOP")


    # クライアントからメッセージを受信したときに呼ばれる関数
    def message_received(self, client, server, message):
        print("client({}) said: {}".format(client['id'], message))

        if message in self.connection_server_to_raspberrypi.keys():
            self.connection_server_to_raspberrypi[message] = client
            self.message = message
            with open(f"/Library/WebServer/Documents/Web2/{self.message}.txt","w") as f:
                f.write("START")
                

        # クライアントが追加されるごとに呼び出す
        def send_picture(user):

            while (True):

                with open(f"/Library/WebServer/Documents/Web2/{user}.txt","r") as f:
                    judge = f.read()

                if judge == "START":
                    with open(f"{path}Data/{user}.jpeg","rb") as f:
                        data = f.read()
                    lang_data = len(data)
                    # print("SEND")

                    if (lang_data != 0):
                        encode = base64.b64encode(data)
                        server.send_message(self.connection_server_to_raspberrypi[user],str(encode))

                else:
                    print("end")
                    break

        # マルチスレッドを立て指定のユーザーへ送る
        send_picture_web = threading.Thread(target=send_picture, args=(self.message,))
        send_picture_web.start()
    
    # サーバーを起動する
    def run(self):
        # クライアント接続時のコールバック関数にself.new_client関数をセット
        self.server.set_fn_new_client(self.new_client)
        # クライアント切断時のコールバック関数にself.client_left関数をセット
        self.server.set_fn_client_left(self.client_left)
    # メッセージ受信時のコールバック関数にself.message_received関数をセット
        self.server.set_fn_message_received(self.message_received) 
        self.server.run_forever()


if __name__ == "__main__":

    path = "./"

    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read(f'{path}connection.ini', 'UTF-8')

    SERVER_IP = config.get('server', 'ip')
    SERVER_PORT = int(config.get('server', 'picture_port'))

    ws_server = Websocket_Server(SERVER_IP, SERVER_PORT)
    ws_server.run()